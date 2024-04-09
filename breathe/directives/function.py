from __future__ import annotations

import re
from breathe.directives import BaseDirective
from breathe.exception import BreatheError
from breathe.file_state_cache import MTimeError
from breathe import parser
from breathe.project import ProjectError
from breathe.renderer import RenderContext, mask, TaggedNode, filter
from breathe.renderer.sphinxrenderer import WithContext
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler

from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes
from sphinx.domains import cpp

from typing import Any, cast, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    cppast: Any
else:
    try:
        from sphinx.domains.cpp import _ast as cppast
    except ImportError:
        cppast = cpp


if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import NotRequired, TypedDict
    else:
        from typing_extensions import NotRequired, TypedDict
    from breathe import project
    from docutils.nodes import Node
    from sphinx.application import Sphinx

    DoxFunctionOptions = TypedDict(
        "DoxFunctionOptions",
        {"path": str, "project": str, "outline": NotRequired[None], "no-link": NotRequired[None]},
    )
else:
    DoxFunctionOptions = None


class _NoMatchingFunctionError(BreatheError):
    pass


class _UnableToResolveFunctionError(BreatheError):
    def __init__(self, signatures: List[str]) -> None:
        self.signatures = signatures


def function_and_all_friend_finder_filter(
    app: Sphinx,
    namespace: str,
    name: str,
    d_parser: parser.DoxygenParser,
    project_info: project.ProjectInfo,
    index: parser.DoxygenIndex,
    matches: list[filter.FinderMatch],
) -> None:
    for f_match in filter.member_finder_filter(
        app,
        namespace,
        name,
        d_parser,
        project_info,
        (parser.MemberKind.function, parser.MemberKind.friend),
        index,
    ):
        cd = f_match[2].value
        assert isinstance(cd, parser.Node_compounddefType)
        matches.append(f_match)


class DoxygenFunctionDirective(BaseDirective):
    required_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
    }
    has_content = False
    final_argument_whitespace = True

    def run(self) -> List[Node]:
        # Extract namespace, function name, and parameters
        # Regex explanation:
        # 1. (?:<something>::)?
        #    Optional namespace prefix, including template arguments if a specialization.
        #    The <something> is group 1:
        #    1. [^:(<]+, basically an identifier
        #       definitely not a scope operator, ::, or template argument list, <
        #    2. (?:::[^:(<]+)*, (?:<stuff>) for anon match group,
        #       so a namespace delimiter and then another identifier
        #    3. ::, another namespace delimiter before the function name
        # 2. ([^(]+), group 2, the function name, whatever remains after the optional prefix,
        #    until a (.
        # 3. (.*), group 3, the parameters.
        # Note: for template argument lists, the spacing is important for the Doxygen lookup.
        # TODO: we should really do this parsing differently, e.g., using the Sphinx C++ domain.
        # TODO: the Doxygen lookup should not be whitespace sensitive.
        match = re.match(r"(?:([^:(<]+(?:::[^:(<]+)*)::)?([^(]+)(.*)", self.arguments[0])
        assert match is not None  # TODO: this is probably not appropriate, for now it fixes typing
        namespace = (match.group(1) or "").strip()
        function_name = match.group(2).strip()
        argsStr = match.group(3)

        options = cast(DoxFunctionOptions, self.options)

        try:
            project_info = self.project_info_factory.create_project_info(options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("doxygenfunction: %s" % e)

        try:
            d_index = self.get_doxygen_index(project_info)
        except MTimeError as e:
            warning = self.create_warning(None)
            return warning.warn("doxygenfunction: %s" % e)

        # Extract arguments from the function name.
        try:
            args = self._parse_args(argsStr)
        except cpp.DefinitionError as e:  # pyright: ignore
            return self.create_warning(
                project_info,
                namespace="%s::" % namespace if namespace else "",
                function=function_name,
                args=argsStr,
                cpperror=str(e),
            ).warn(
                "doxygenfunction: Unable to resolve function "
                '"{namespace}{function}" with arguments "{args}".\n'
                "Could not parse arguments. Parsing error is\n{cpperror}"
            )

        matchesAll: list[filter.FinderMatch] = []
        function_and_all_friend_finder_filter(
            self.app, namespace, function_name, self.dox_parser, project_info, d_index, matchesAll
        )

        matches: list[filter.FinderMatch] = []
        for m in matchesAll:
            # only take functions and friend functions
            # ignore friend classes
            node = m[0].value
            assert isinstance(node, parser.Node_memberdefType)
            if node.kind == "friend" and not node.argsstring:
                continue
            matches.append(m)

        # Create it ahead of time as it is cheap and it is ugly to declare it for both exception
        # clauses below
        warning = self.create_warning(
            project_info,
            namespace="%s::" % namespace if namespace else "",
            function=function_name,
            args=str(args),
        )

        try:
            node_stack = self._resolve_function(matches, args, project_info)
        except _NoMatchingFunctionError:
            return warning.warn(
                'doxygenfunction: Cannot find function "{namespace}{function}" ' "{tail}"
            )
        except _UnableToResolveFunctionError as error:
            message = (
                "doxygenfunction: Unable to resolve function "
                '"{namespace}{function}" with arguments {args} {tail}.\n'
                "Potential matches:\n"
            )

            text = ""
            for i, entry in enumerate(sorted(error.signatures)):
                text += "- %s\n" % entry
            block = nodes.literal_block("", "", nodes.Text(text))
            formatted_message = warning.format(message)
            warning_nodes = [nodes.paragraph("", "", nodes.Text(formatted_message)), block]
            result = warning.warn(message, rendered_nodes=warning_nodes, unformatted_suffix=text)
            return result
        except cpp.DefinitionError as error:  # pyright: ignore
            warning.context["cpperror"] = str(error)
            return warning.warn(
                "doxygenfunction: Unable to resolve function "
                '"{namespace}{function}" with arguments "{args}".\n'
                "Candidate function could not be parsed. Parsing error is\n{cpperror}"
            )

        target_handler = create_target_handler(options, project_info, self.state.document)
        filter_ = filter.create_outline_filter(options)

        return self.render(
            node_stack,
            project_info,
            filter_,
            target_handler,
            mask.NullMaskFactory(),
            self.directive_args,
        )

    def _parse_args(self, function_description: str) -> Optional[cppast.ASTParametersQualifiers]:
        # Note: the caller must catch cpp.DefinitionError
        if function_description == "":
            return None

        parser = cpp.DefinitionParser(
            function_description, location=self.get_source_info(), config=self.config
        )
        paramQual = parser._parse_parameters_and_qualifiers(paramMode="function")
        # strip everything that doesn't contribute to overloading

        def stripParamQual(paramQual):
            paramQual.exceptionSpec = None
            paramQual.final = None
            paramQual.override = None
            # TODO: strip attrs when Doxygen handles them
            paramQual.initializer = None
            paramQual.trailingReturn = None
            for p in paramQual.args:
                if p.arg is None:
                    assert p.ellipsis
                    continue
                p.arg.init = None
                declarator = p.arg.type.decl

                def stripDeclarator(declarator):
                    if hasattr(declarator, "next"):
                        stripDeclarator(declarator.next)
                        if isinstance(declarator, cppast.ASTDeclaratorParen):
                            assert hasattr(declarator, "inner")
                            stripDeclarator(declarator.inner)
                    else:
                        assert isinstance(declarator, cppast.ASTDeclaratorNameParamQual)
                        assert hasattr(declarator, "declId")
                        declarator.declId = None
                        if declarator.paramQual is not None:
                            stripParamQual(declarator.paramQual)

                stripDeclarator(declarator)

        stripParamQual(paramQual)
        return paramQual

    def _create_function_signature(
        self,
        node_stack: list[TaggedNode],
        project_info,
        filter_,
        target_handler,
        mask_factory,
        directive_args,
    ) -> str:
        "Standard render process used by subclasses"

        object_renderer = SphinxRenderer(
            self.dox_parser.app,
            project_info,
            [tn.value for tn in node_stack],
            self.state,
            self.state.document,
            target_handler,
            self.dox_parser,
            filter_,
        )

        context = RenderContext(node_stack, mask_factory, directive_args)
        node = node_stack[0].value
        with WithContext(object_renderer, context):
            assert isinstance(node, parser.Node_memberdefType)
            # this part should be kept in sync with visit_function in sphinxrenderer
            name = node.name
            # assume we are only doing this for C++ declarations
            declaration = " ".join(
                [
                    object_renderer.create_template_prefix(node),
                    "".join(n.astext() for n in object_renderer.render(node.type)),
                    name,
                    node.argsstring or "",
                ]
            )
        cpp_parser = cpp.DefinitionParser(
            declaration, location=self.get_source_info(), config=self.config
        )
        ast = cpp_parser.parse_declaration("function", "function")
        return str(ast)

    def _resolve_function(
        self,
        matches: list[filter.FinderMatch],
        args: cppast.ASTParametersQualifiers | None,
        project_info: project.ProjectInfo,
    ):
        if not matches:
            raise _NoMatchingFunctionError()

        res = []
        candSignatures = []
        for entry in matches:
            text_options = {"no-link": "", "outline": ""}

            # Render the matches to docutils nodes
            target_handler = create_target_handler(
                {"no-link": ""}, project_info, self.state.document
            )
            filter_ = filter.create_outline_filter(text_options)
            mask_factory = mask.MaskFactory({parser.Node_paramType: mask.no_parameter_names})

            # Override the directive args for this render
            directive_args = self.directive_args[:]
            directive_args[2] = text_options

            signature = self._create_function_signature(
                entry, project_info, filter_, target_handler, mask_factory, directive_args
            )
            candSignatures.append(signature)

            if args is not None:
                match = re.match(r"([^(]*)(.*)", signature)
                assert match
                _match_args = match.group(2)

                # Parse the text to find the arguments
                # This one should succeed as it came from _create_function_signature
                match_args = self._parse_args(_match_args)

                # Match them against the arg spec
                if args != match_args:
                    continue

            res.append((entry, signature))

        if len(res) == 1 or (len(res) > 1 and all(x[1] == res[0][1] for x in res)):
            return res[0][0]
        else:
            raise _UnableToResolveFunctionError(candSignatures)
