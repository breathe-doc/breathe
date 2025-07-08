from __future__ import annotations

import re
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    Literal,
    TypeVar,
    Union,
    cast,
)

from docutils import nodes
from docutils.parsers.rst.states import Text
from docutils.statemachine import StringList, UnexpectedIndentationError
from sphinx import addnodes
from sphinx.domains import c, cpp, python
from sphinx.ext.graphviz import graphviz
from sphinx.util import url_re
from sphinx.util.nodes import nested_parse_with_titles

from breathe import filetypes, parser
from breathe._parser import DoxCompoundKind
from breathe.cpp_util import split_name
from breathe.renderer.filter import NodeStack

php: Any
try:
    from sphinxcontrib import phpdomain as php  # type: ignore[import-untyped, no-redef]
except ImportError:
    php = None

cs: Any
try:
    # The only valid types for sphinx_csharp are in a git repo so we can't easily rely
    # on them as we can't publish with a git repo dependency so we tell mypy to ignore
    # an import failure here
    from sphinx_csharp import csharp as cs  # type: ignore[import-not-found, no-redef]
except ImportError:
    cs = None


T = TypeVar("T")

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from typing import (
        Any,
        ClassVar,
        Protocol,
    )

    from sphinx.application import Sphinx
    from sphinx.directives import ObjectDescription

    from breathe.project import ProjectInfo
    from breathe.renderer import DataObject, RenderContext
    from breathe.renderer.filter import DoxFilter
    from breathe.renderer.target import TargetHandler

    class HasRefID(Protocol):
        @property
        def refid(self) -> str: ...

    class HasTemplateParamList(Protocol):
        @property
        def templateparamlist(self) -> parser.Node_templateparamlistType | None: ...

    class HasDescriptions(Protocol):
        @property
        def briefdescription(self) -> parser.Node_descriptionType | None: ...

        @property
        def detaileddescription(self) -> parser.Node_descriptionType | None: ...


ContentCallback = Callable[[addnodes.desc_content], None]
Declarator = Union[addnodes.desc_signature, addnodes.desc_signature_line]
DeclaratorCallback = Callable[[Declarator], None]

_debug_indent = 0

_findall_compat = cast(
    "Callable", getattr(nodes.Node, "findall", getattr(nodes.Node, "traverse", None))
)


# Doxygen sometimes leaves 'static' in the type, e.g., for "constexpr static
# auto f()"
# In Doxygen up to somewhere between 1.8.17 to exclusive 1.9.1 the 'friend' part
# is also left in the type. See also #767.
# Until version 1.11, Doxygen left constexpr (I haven't checked consteval or
# constinit) in the type.
QUALIFIERS_TO_REMOVE = re.compile(r"\b(static|friend|constexpr|consteval|constinit) ")


def strip_legacy_qualifiers(x):
    return QUALIFIERS_TO_REMOVE.sub("", x)


class WithContext:
    def __init__(self, parent: SphinxRenderer, context: RenderContext):
        self.context = context
        self.parent = parent
        self.previous = None

    def __enter__(self):
        assert self.previous is None
        self.previous = self.parent.context
        self.parent.set_context(self.context)
        return self

    def __exit__(self, et, ev, bt):
        self.parent.context = self.previous
        self.previous = None


class BaseObject:
    # Use this class as the first base class to make sure the overrides are used.
    # Set the content_callback attribute to a function taking a docutils node.
    breathe_content_callback: ContentCallback | None = None

    def transform_content(self, contentnode: addnodes.desc_content) -> None:
        super().transform_content(contentnode)  # type: ignore[misc]
        if self.breathe_content_callback is None:
            return
        self.breathe_content_callback(contentnode)


# ----------------------------------------------------------------------------


class CPPClassObject(BaseObject, cpp.CPPClassObject):
    pass


class CPPUnionObject(BaseObject, cpp.CPPUnionObject):
    pass


class CPPFunctionObject(BaseObject, cpp.CPPFunctionObject):
    pass


class CPPMemberObject(BaseObject, cpp.CPPMemberObject):
    pass


class CPPTypeObject(BaseObject, cpp.CPPTypeObject):
    pass


class CPPConceptObject(BaseObject, cpp.CPPConceptObject):
    pass


class CPPEnumObject(BaseObject, cpp.CPPEnumObject):
    pass


class CPPEnumeratorObject(BaseObject, cpp.CPPEnumeratorObject):
    pass


# ----------------------------------------------------------------------------


class CStructObject(BaseObject, c.CStructObject):
    pass


class CUnionObject(BaseObject, c.CUnionObject):
    pass


class CFunctionObject(BaseObject, c.CFunctionObject):
    pass


class CMemberObject(BaseObject, c.CMemberObject):
    pass


class CTypeObject(BaseObject, c.CTypeObject):
    pass


class CEnumObject(BaseObject, c.CEnumObject):
    pass


class CEnumeratorObject(BaseObject, c.CEnumeratorObject):
    pass


class CMacroObject(BaseObject, c.CMacroObject):
    pass


# ----------------------------------------------------------------------------


class PyFunction(BaseObject, python.PyFunction):
    pass


class PyAttribute(BaseObject, python.PyAttribute):
    pass


class PyClasslike(BaseObject, python.PyClasslike):
    pass


# ----------------------------------------------------------------------------

# Create multi-inheritance classes to merge BaseObject from Breathe with
# classes from phpdomain.
# We use capitalization (and the namespace) to differentiate between the two

if php is not None or TYPE_CHECKING:

    class PHPNamespaceLevel(BaseObject, php.PhpNamespacelevel):
        """Description of a PHP item *in* a namespace (not the space itself)."""

        pass

    class PHPClassLike(BaseObject, php.PhpClasslike):
        pass

    class PHPClassMember(BaseObject, php.PhpClassmember):
        pass

    class PHPGlobalLevel(BaseObject, php.PhpGloballevel):
        pass


# ----------------------------------------------------------------------------

if cs is not None or TYPE_CHECKING:

    class CSharpCurrentNamespace(BaseObject, cs.CSharpCurrentNamespace):
        pass

    class CSharpNamespacePlain(BaseObject, cs.CSharpNamespacePlain):
        pass

    class CSharpClass(BaseObject, cs.CSharpClass):
        pass

    class CSharpStruct(BaseObject, cs.CSharpStruct):
        pass

    class CSharpInterface(BaseObject, cs.CSharpInterface):
        pass

    class CSharpInherits(BaseObject, cs.CSharpInherits):
        pass

    class CSharpMethod(BaseObject, cs.CSharpMethod):
        pass

    class CSharpVariable(BaseObject, cs.CSharpVariable):
        pass

    class CSharpProperty(BaseObject, cs.CSharpProperty):
        pass

    class CSharpEvent(BaseObject, cs.CSharpEvent):
        pass

    class CSharpEnum(BaseObject, cs.CSharpEnum):
        pass

    class CSharpEnumValue(BaseObject, cs.CSharpEnumValue):
        pass

    class CSharpAttribute(BaseObject, cs.CSharpAttribute):
        pass

    class CSharpIndexer(BaseObject, cs.CSharpIndexer):
        pass

    class CSharpXRefRole(BaseObject, cs.CSharpXRefRole):
        pass


# ----------------------------------------------------------------------------


class DomainDirectiveFactory:
    # A mapping from node kinds to domain directives and their names.
    cpp_classes: dict[str, tuple[type[ObjectDescription], str]] = {
        "variable": (CPPMemberObject, "var"),
        "class": (CPPClassObject, "class"),
        "struct": (CPPClassObject, "struct"),
        "interface": (CPPClassObject, "class"),
        "function": (CPPFunctionObject, "function"),
        "friend": (CPPFunctionObject, "function"),
        "signal": (CPPFunctionObject, "function"),
        "slot": (CPPFunctionObject, "function"),
        "concept": (CPPConceptObject, "concept"),
        "enum": (CPPEnumObject, "enum"),
        "enum-class": (CPPEnumObject, "enum-class"),
        "typedef": (CPPTypeObject, "type"),
        "using": (CPPTypeObject, "type"),
        "union": (CPPUnionObject, "union"),
        "namespace": (CPPTypeObject, "type"),
        "enumvalue": (CPPEnumeratorObject, "enumerator"),
        "define": (CMacroObject, "macro"),
    }
    c_classes: dict[str, tuple[type[ObjectDescription], str]] = {
        "variable": (CMemberObject, "var"),
        "function": (CFunctionObject, "function"),
        "define": (CMacroObject, "macro"),
        "struct": (CStructObject, "struct"),
        "union": (CUnionObject, "union"),
        "enum": (CEnumObject, "enum"),
        "enumvalue": (CEnumeratorObject, "enumerator"),
        "typedef": (CTypeObject, "type"),
    }
    python_classes: dict[str, tuple[type[ObjectDescription], str]] = {
        # TODO: PyFunction is meant for module-level functions
        #       and PyAttribute is meant for class attributes, not module-level variables.
        #       Somehow there should be made a distinction at some point to get the correct
        #       index-text and whatever other things are different.
        "function": (PyFunction, "function"),
        "variable": (PyAttribute, "attribute"),
        "class": (PyClasslike, "class"),
        "namespace": (PyClasslike, "class"),
    }

    php_classes: dict[str, tuple[type[ObjectDescription], str]]
    if php is not None:
        php_classes = {
            "function": (PHPNamespaceLevel, "function"),
            "class": (PHPClassLike, "class"),
            "attr": (PHPClassMember, "attr"),
            "method": (PHPClassMember, "method"),
            "global": (PHPGlobalLevel, "global"),
        }
        php_classes_default = php_classes["class"]  # Directive when no matching ones were found

    cs_classes: dict[str, tuple[type[ObjectDescription], str]]
    if cs is not None:
        cs_classes = {
            # 'doxygen-name': (CSharp class, key in CSharpDomain.object_types)
            "namespace": (CSharpNamespacePlain, "namespace"),
            "class": (CSharpClass, "class"),
            "struct": (CSharpStruct, "struct"),
            "interface": (CSharpInterface, "interface"),
            "function": (CSharpMethod, "function"),
            "method": (CSharpMethod, "method"),
            "variable": (CSharpVariable, "var"),
            "property": (CSharpProperty, "property"),
            "event": (CSharpEvent, "event"),
            "enum": (CSharpEnum, "enum"),
            "enumvalue": (CSharpEnumValue, "enumerator"),
            "attribute": (CSharpAttribute, "attr"),
            # Fallback to cpp domain
            "typedef": (CPPTypeObject, "type"),
        }

    @staticmethod
    def create(domain: str, args) -> ObjectDescription:
        cls: type[ObjectDescription]
        name: str
        if domain == "c":
            cls, name = DomainDirectiveFactory.c_classes[args[0]]
        elif domain == "py":
            cls, name = DomainDirectiveFactory.python_classes[args[0]]
        elif php is not None and domain == "php":
            separators = php.separators
            arg_0 = args[0]
            if any(separators["method"] in n for n in args[1]):
                if any(separators["attr"] in n for n in args[1]):
                    arg_0 = "attr"
                else:
                    arg_0 = "method"
            else:
                if arg_0 == "variable":
                    arg_0 = "global"

            if arg_0 in DomainDirectiveFactory.php_classes:
                cls, name = DomainDirectiveFactory.php_classes[arg_0]
            else:
                cls, name = DomainDirectiveFactory.php_classes_default

        elif cs is not None and domain == "cs":
            cls, name = DomainDirectiveFactory.cs_classes[args[0]]
        else:
            domain = "cpp"
            cls, name = DomainDirectiveFactory.cpp_classes[args[0]]
        # Replace the directive name because domain directives don't know how to handle
        # Breathe's "doxygen" directives.
        assert ":" not in name
        args = [domain + ":" + name] + args[1:]
        return cls(*args)


class NodeFinder(nodes.SparseNodeVisitor):
    """Find the Docutils desc_signature declarator and desc_content nodes."""

    def __init__(self, document: nodes.document):
        super().__init__(document)
        self.declarator: Declarator | None = None
        self.content: addnodes.desc_content | None = None

    def visit_desc_signature(self, node: addnodes.desc_signature):
        # Find the last signature node because it contains the actual declarator
        # rather than "template <...>". In Sphinx 1.4.1 we'll be able to use sphinx_cpp_tagname:
        # https://github.com/breathe-doc/breathe/issues/242
        self.declarator = node

    def visit_desc_signature_line(self, node: addnodes.desc_signature_line):
        # In sphinx 1.5, there is now a desc_signature_line node within the desc_signature
        # This should be used instead
        self.declarator = node

    def visit_desc_content(self, node: addnodes.desc_content):
        self.content = node
        # The SparseNodeVisitor seems to not actually be universally Sparse,
        # but only for nodes known to Docutils.
        # So if there are extensions with new node types in the content,
        # then the visitation will fail.
        # We anyway don't need to visit the actual content, so skip it.
        raise nodes.SkipChildren


def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x


def get_param_decl(param: parser.Node_paramType) -> str:
    def to_string(node: parser.Node_linkedTextType | None) -> str:
        """Convert Doxygen node content to a string."""
        result: list[str] = []
        if node is not None:
            for p in node:
                if isinstance(p, str):
                    result.append(p)
                else:
                    result.append(p.value[0])
        return " ".join(result)

    param_type = to_string(param.type)
    param_name = param.declname or param.defname
    if not param_name:
        param_decl = param_type
    else:
        param_decl, number_of_subs = re.subn(
            r"(\((?:\w+::)*[*&]+)(\))", r"\g<1>" + param_name + r"\g<2>", param_type
        )
        if number_of_subs == 0:
            param_decl = param_type + " " + param_name
    if param.array:
        param_decl += param.array
    if param.defval:
        param_decl += " = " + to_string(param.defval)

    return param_decl


def get_definition_without_template_args(data_object):
    """
    Return data_object.definition removing any template arguments from the class name in the member
    function.  Otherwise links to classes defined in the same template are not generated correctly.

    For example in 'Result<T> A< B<C> >::f' we want to remove the '< B<C> >' part.
    """
    definition = data_object.definition
    if len(data_object.bitfield) > 0:
        definition += " : " + data_object.bitfield
    qual_name = "::" + data_object.name
    if definition.endswith(qual_name):
        qual_name_start = len(definition) - len(qual_name)
        pos = qual_name_start - 1
        if definition[pos] == ">":
            bracket_count = 0
            # Iterate back through the characters of the definition counting matching braces and
            # then remove all braces and everything between
            while pos > 0:
                if definition[pos] == ">":
                    bracket_count += 1
                elif definition[pos] == "<":
                    bracket_count -= 1
                    if bracket_count == 0:
                        definition = definition[:pos] + definition[qual_name_start:]
                        break
                pos -= 1
    return definition


class InlineText(Text):
    """
    Add a custom docutils class to allow parsing inline text. This is to be
    used inside a @verbatim/@endverbatim block but only the first line is
    consumed and a inline element is generated as the parent, instead of the
    paragraph used by Text.
    """

    patterns = {"inlinetext": r""}
    initial_transitions = [("inlinetext", "text")]

    def indent(self, match, context, next_state):
        """
        Avoid Text's indent from detecting space prefixed text and
        doing "funny" stuff; always rely on inlinetext for parsing.
        """
        return self.inlinetext(match, context, next_state)

    def eof(self, context):
        """
        Text.eof() inserts a paragraph, so override it to skip adding elements.
        """
        return []

    def inlinetext(self, match, context, next_state):
        """
        Called by the StateMachine when an inline element is found (which is
        any text when this class is added as the single transition.
        """
        startline = self.state_machine.abs_line_number() - 1
        msg = None
        try:
            block = self.state_machine.get_text_block()
        except UnexpectedIndentationError as err:
            block, src, srcline = err.args
            msg = self.reporter.error("Unexpected indentation.", source=src, line=srcline)
        lines = context + list(block)
        text, _ = self.inline_text(lines[0], startline)
        self.parent += text
        self.parent += msg
        return [], next_state, []


def get_content(node: parser.Node_docParaType):
    # Add programlisting nodes to content rather than a separate list,
    # because programlisting and content nodes can interleave as shown in
    # https://www.stack.nl/~dimitri/doxygen/manual/examples/include/html/example.html.

    return (
        item
        for item in node
        if parser.tag_name_value(item)[0] not in {"parameterlist", "simplesect", "image"}
    )


def get_parameterlists(node: parser.Node_docParaType) -> Iterable[parser.Node_docParamListType]:
    pairs = map(parser.tag_name_value, node)  # type: ignore[arg-type]
    return (value for name, value in pairs if name == "parameterlist")  # type: ignore[misc]


def get_simplesects(node: parser.Node_docParaType) -> Iterable[parser.Node_docSimpleSectType]:
    pairs = map(parser.tag_name_value, node)  # type: ignore[arg-type]
    return (value for name, value in pairs if name == "simplesect")  # type: ignore[misc]


def get_images(node: parser.Node_docParaType) -> Iterable[parser.Node_docImageType]:
    pairs = map(parser.tag_name_value, node)  # type: ignore[arg-type]
    return (value for name, value in pairs if name == "image")  # type: ignore[misc]


def namespace_strip(config, nodes_: list[nodes.Node]):
    # In some cases of errors with a declaration there are no nodes
    # (e.g., variable in function), so perhaps skip (see #671).
    # If there are nodes, there should be at least 2.
    if len(nodes_) != 0:
        assert len(nodes_) >= 2
        rst_node = nodes_[1]
        doc = rst_node.document
        assert doc is not None
        finder = NodeFinder(doc)
        rst_node.walk(finder)

        assert finder.declarator
        # the type is set to "Any" to get around missing typing info in
        # docutils 0.20.1
        signode: Any = finder.declarator
        signode.children = [n for n in signode.children if n.tagname != "desc_addname"]


T_sphinxrenderer = TypeVar("T_sphinxrenderer", bound="SphinxRenderer")


class NodeHandler(Generic[T_sphinxrenderer, T]):
    """Dummy callable that associates a set of nodes to a function. This gets
    unwrapped by NodeVisitor and is never actually called."""

    def __init__(self, handler: Callable[[T_sphinxrenderer, T], list[nodes.Node]]):
        self.handler = handler
        self.nodes: set[type[parser.NodeOrValue]] = set()

    def __call__(self, r: T_sphinxrenderer, node: T, /) -> list[nodes.Node]:  # pragma: no cover
        raise TypeError()


class TaggedNodeHandler(Generic[T_sphinxrenderer, T]):
    """Dummy callable that associates a set of nodes to a function. This gets
    unwrapped by NodeVisitor and is never actually called."""

    def __init__(self, handler: Callable[[T_sphinxrenderer, str, T], list[nodes.Node]]):
        self.handler = handler
        self.nodes: set[type[parser.NodeOrValue]] = set()

    def __call__(
        self, r: T_sphinxrenderer, tag: str, node: T, /
    ) -> list[nodes.Node]:  # pragma: no cover
        raise TypeError()


def node_handler(node: type[parser.NodeOrValue]):
    def inner(
        f: Callable[[T_sphinxrenderer, T], list[nodes.Node]],
    ) -> Callable[[T_sphinxrenderer, T], list[nodes.Node]]:
        handler: NodeHandler = f if isinstance(f, NodeHandler) else NodeHandler(f)
        handler.nodes.add(node)
        return handler

    return inner


def tagged_node_handler(node: type[parser.NodeOrValue]):
    def inner(
        f: Callable[[T_sphinxrenderer, str, T], list[nodes.Node]],
    ) -> Callable[[T_sphinxrenderer, str, T], list[nodes.Node]]:
        handler: TaggedNodeHandler = f if isinstance(f, TaggedNodeHandler) else TaggedNodeHandler(f)
        handler.nodes.add(node)
        return handler

    return inner


class NodeVisitor(type):
    """Metaclass that collects all methods marked as @node_handler and
    @tagged_node_handler into the dicts 'node_handlers' and
    'tagged_node_handlers' respectively, and assigns the dicts to the class"""

    def __new__(cls, name, bases, members):
        handlers = {}
        tagged_handlers = {}

        for key, value in members.items():
            if isinstance(value, NodeHandler):
                for n in value.nodes:
                    handlers[n] = value.handler
                members[key] = value.handler
            elif isinstance(value, TaggedNodeHandler):
                for n in value.nodes:
                    tagged_handlers[n] = value.handler
                members[key] = value.handler

        members["node_handlers"] = handlers
        members["tagged_node_handlers"] = tagged_handlers

        return type.__new__(cls, name, bases, members)


# class RenderDebugPrint:
#     def __init__(self,renderer,node):
#         self.renderer = renderer
#         renderer._debug_print_depth = 1 + getattr(renderer,'_debug_print_depth',0)
#         print('  '*renderer._debug_print_depth,type(node))
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self,*args):
#         self.renderer._debug_print_depth -= 1


class SphinxRenderer(metaclass=NodeVisitor):
    """
    Doxygen node visitor that converts input into Sphinx/RST representation.
    Each visit method takes a Doxygen node as an argument and returns a list of RST nodes.
    """

    node_handlers: ClassVar[
        dict[
            type[parser.NodeOrValue],
            Callable[[SphinxRenderer, parser.NodeOrValue], list[nodes.Node]],
        ]
    ]
    tagged_node_handlers: ClassVar[
        dict[
            type[parser.NodeOrValue],
            Callable[[SphinxRenderer, str, parser.NodeOrValue], list[nodes.Node]],
        ]
    ]

    def __init__(
        self,
        app: Sphinx,
        project_info: ProjectInfo,
        node_stack: list[DataObject],
        state,
        document: nodes.document,
        target_handler: TargetHandler,
        dox_parser: parser.DoxygenParser,
        filter_: DoxFilter,
    ):
        self.app = app

        self.project_info = project_info
        self.qualification_stack = node_stack
        self.nesting_level = 0
        self.state = state
        self.document = document
        self.target_handler = target_handler
        self.dox_parser = dox_parser
        self.filter_ = filter_

        self.context: RenderContext | None = None
        self.output_defname = True
        # Nesting level for lists.
        self.nesting_level = 0

    def set_context(self, context: RenderContext) -> None:
        self.context = context
        if self.context.domain == "":
            self.context.domain = self.get_domain()

    # XXX: fix broken links in XML generated by Doxygen when Doxygen's
    # SEPARATE_MEMBER_PAGES is set to YES; this function should be harmless
    # when SEPARATE_MEMBER_PAGES is NO!
    #
    # The issue was discussed here: https://github.com/doxygen/doxygen/pull/7971
    #
    # A Doxygen anchor consists of a 32-byte string version of the results of
    # passing in the stringified identifier or prototype that is being "hashed".
    # An "a" character is then prefixed to mark it as an anchor. Depending on how
    # the identifier is linked, it can also get a "g" prefix to mean it is part
    # of a Doxygen group. This results in an id having either 33 or 34 bytes
    # (containing a "g" or not). Some identifiers, eg enumerators, get twice that
    # length to have both a unique enum + unique enumerator, and sometimes they
    # get two "g" characters as prefix instead of one.
    def _fixup_separate_member_pages(self, refid: str) -> str:
        if refid:
            parts = refid.rsplit("_", 1)
            if len(parts) == 2 and parts[1].startswith("1"):
                anchorid = parts[1][1:]
                if len(anchorid) in {33, 34} and parts[0].endswith(anchorid):
                    return parts[0][: -len(anchorid)] + parts[1]
                elif len(anchorid) > 34:
                    index = 0
                    if anchorid.startswith("gg"):
                        index = 1
                        _len = 35
                    elif anchorid.startswith("g"):
                        _len = 34
                    else:
                        _len = 33
                    if parts[0].endswith(anchorid[index:_len]):
                        return parts[0][: -(_len - index)] + parts[1]

        return refid

    def get_refid(self, refid: str) -> str:
        if self.app.config.breathe_separate_member_pages:
            refid = self._fixup_separate_member_pages(refid)
        if self.app.config.breathe_use_project_refids:
            return "%s%s" % (self.project_info.name(), refid)
        else:
            return refid

    def parse_compound(self, refid: str) -> parser.Node_DoxygenType:
        return self.dox_parser.parse_compound(refid, self.project_info).root

    def get_domain(self) -> str:
        """Returns the domain for the current node."""

        def get_filename(node) -> str | None:
            """Returns the name of a file where the declaration represented by node is located."""
            try:
                return node.location.file
            except AttributeError:
                return None

        assert self.context is not None

        node_stack = self.context.node_stack
        node = node_stack[0].value
        # An enumvalueType node doesn't have location, so use its parent node
        # for detecting the domain instead.
        if isinstance(node, (str, parser.Node_enumvalueType)):
            node = node_stack[1].value
        filename = get_filename(node)
        if not filename and isinstance(node, parser.Node_CompoundType):
            file_data = self.parse_compound(node.refid)
            filename = get_filename(file_data.compounddef)
        return self.project_info.domain_for_file(filename) if filename else ""

    def join_nested_name(self, names: list[str]) -> str:
        dom = self.get_domain()
        sep = "::" if not dom or dom == "cpp" else "."
        return sep.join(names)

    def run_directive(
        self, obj_type: str, declaration: str, contentCallback: ContentCallback, options={}
    ) -> list[nodes.Node]:
        assert self.context is not None
        args = [obj_type, [declaration]] + self.context.directive_args[2:]
        directive = DomainDirectiveFactory.create(self.context.domain, args)

        assert isinstance(directive, BaseObject)
        directive.breathe_content_callback = contentCallback

        # Translate Breathe's no-link option into the standard noindex option.
        if "no-link" in self.context.directive_args[2]:
            directive.options["noindex"] = True
        for k, v in options.items():
            directive.options[k] = v

        assert self.app.env is not None
        config = self.app.env.config

        if config.breathe_debug_trace_directives:  # pragma: no cover
            global _debug_indent
            print(
                "{}Running directive: .. {}:: {}".format(
                    "  " * _debug_indent, directive.name, declaration
                )
            )
            _debug_indent += 1

        self.nesting_level += 1
        nodes_ = directive.run()
        self.nesting_level -= 1

        # TODO: the directive_args seems to be reused between different run_directives
        #       so for now, reset the options.
        #       Remove this once the args are given in a different manner.
        for k, v in options.items():
            del directive.options[k]

        if config.breathe_debug_trace_directives:  # pragma: no cover
            _debug_indent -= 1

        # Filter out outer class names if we are rendering a member as a part of a class content.
        if self.context.child:
            namespace_strip(config, nodes_)
        return nodes_

    def handle_compounddef_declaration(
        self,
        node: parser.Node_compounddefType,
        obj_type: str,
        declaration: str,
        file_data,
        new_context,
        parent_context,
        display_obj_type: str | None = None,
    ) -> list[nodes.Node]:
        def content(contentnode) -> None:
            if node.includes:
                for include in node.includes:
                    contentnode.extend(
                        self.render(include, new_context.create_child_context(include))
                    )
            rendered_data = self.render(file_data, parent_context)
            contentnode.extend(rendered_data)

        return self.handle_declaration(
            node, obj_type, declaration, content_callback=content, display_obj_type=display_obj_type
        )

    def handle_declaration(
        self,
        node: parser.Node_compounddefType | parser.Node_memberdefType | parser.Node_enumvalueType,
        obj_type: str,
        declaration: str,
        *,
        content_callback: ContentCallback | None = None,
        display_obj_type: str | None = None,
        declarator_callback: DeclaratorCallback | None = None,
        options={},
    ) -> list[nodes.Node]:
        if content_callback is None:

            def content(contentnode: addnodes.desc_content):
                contentnode.extend(self.description(node))

            content_callback = content
        declaration = declaration.replace("\n", " ")
        nodes_ = self.run_directive(obj_type, declaration, content_callback, options)

        assert self.app.env is not None
        target = None
        if self.app.env.config.breathe_debug_trace_doxygen_ids:
            target = self.create_doxygen_target(node)
            if len(target) == 0:
                print("{}Doxygen target: (none)".format("  " * _debug_indent))
            else:
                print("{}Doxygen target: {}".format("  " * _debug_indent, target[0]["ids"]))

        # <desc><desc_signature> and then one or more <desc_signature_line>
        # each <desc_signature_line> has a sphinx_line_type which hints what is present in that line
        # In some cases of errors with a declaration there are no nodes
        # (e.g., variable in function), so perhaps skip (see #671).
        if len(nodes_) == 0:
            return []
        assert len(nodes_) >= 2, nodes_
        desc = nodes_[1]
        assert isinstance(desc, addnodes.desc)
        assert len(desc) >= 1
        sig = desc[0]
        assert isinstance(sig, addnodes.desc_signature)

        # Insert the member name for use in Sphinx-generated table of contents.
        if isinstance(node, parser.Node_compounddefType):
            member_name = node.compoundname
        else:
            member_name = node.name
        if obj_type == "function":
            member_name += "()"
        sig.attributes["_toc_name"] = member_name
        sig.attributes["_toc_parts"] = member_name

        # if may or may not be a multiline signature
        isMultiline = sig.get("is_multiline", False)
        declarator: Declarator | None = None
        if isMultiline:
            for line in sig:
                assert isinstance(line, addnodes.desc_signature_line)
                if line.sphinx_line_type == "declarator":
                    declarator = line
        else:
            declarator = sig
        assert declarator is not None
        if display_obj_type is not None:
            n = declarator[0]
            if self.get_domain() and self.get_domain() not in ("c", "cpp"):
                assert isinstance(n, addnodes.desc_annotation)
                assert n.astext()[-1] == " "
                txt = display_obj_type + " "
                declarator[0] = addnodes.desc_annotation(txt, txt)
            else:
                assert isinstance(n, addnodes.desc_sig_keyword)
                declarator[0] = addnodes.desc_sig_keyword(display_obj_type, display_obj_type)
        if target is None:
            target = self.create_doxygen_target(node)
        declarator.insert(0, target)
        if declarator_callback:
            declarator_callback(declarator)
        return nodes_

    def get_qualification(self) -> list[str]:
        if self.nesting_level > 0:
            return []

        assert self.app.env is not None
        config = self.app.env.config
        if config.breathe_debug_trace_qualification:

            def debug_print_node(n):
                return f"node_type={n.node_type}"

            global _debug_indent
            print(
                "{}{}".format(_debug_indent * "  ", debug_print_node(self.qualification_stack[0]))
            )
            _debug_indent += 1

        names: list[str] = []
        for node in self.qualification_stack[1:]:
            if config.breathe_debug_trace_qualification:
                print("{}{}".format(_debug_indent * "  ", debug_print_node(node)))
            if isinstance(node, parser.Node_refType) and len(names) == 0:
                if config.breathe_debug_trace_qualification:
                    print("{}{}".format(_debug_indent * "  ", "res="))
                return []
            if (
                isinstance(node, parser.Node_CompoundType)
                and node.kind
                not in [
                    parser.CompoundKind.file,
                    parser.CompoundKind.namespace,
                    parser.CompoundKind.group,
                ]
            ) or isinstance(node, parser.Node_memberdefType):
                # We skip the 'file' entries because the file name doesn't form part of the
                # qualified name for the identifier. We skip the 'namespace' entries because if we
                # find an object through the namespace 'compound' entry in the index.xml then we'll
                # also have the 'compounddef' entry in our node stack and we'll get it from that. We
                # need the 'compounddef' entry because if we find the object through the 'file'
                # entry in the index.xml file then we need to get the namespace name from somewhere
                names.append(node.name)
            if (
                isinstance(node, parser.Node_compounddefType)
                and node.kind == parser.DoxCompoundKind.namespace
            ):
                # Nested namespaces include their parent namespace(s) in compoundname. ie,
                # compoundname is 'foo::bar' instead of just 'bar' for namespace 'bar' nested in
                # namespace 'foo'. We need full compoundname because node_stack doesn't necessarily
                # include parent namespaces and we stop here in case it does.
                names.extend(reversed(node.compoundname.split("::")))
                break

        names.reverse()

        if config.breathe_debug_trace_qualification:
            print("{}res={}".format(_debug_indent * "  ", names))
            _debug_indent -= 1
        return names

    # ===================================================================================

    def get_fully_qualified_name(self):
        assert self.context
        names = []
        node_stack = self.context.node_stack
        node = node_stack[0]

        # If the node is a namespace, use its name because namespaces are skipped in the main loop.
        if (
            isinstance(node.value, parser.Node_CompoundType)
            and node.value.kind == parser.CompoundKind.namespace
        ):
            names.append(node.value.name)

        for tval in node_stack:
            node = tval.value
            if isinstance(node, parser.Node_refType) and len(names) == 0:
                return "".join(node)
            if (
                isinstance(node, parser.Node_CompoundType)
                and node.kind
                not in [
                    parser.CompoundKind.file,
                    parser.CompoundKind.namespace,
                    parser.CompoundKind.group,
                ]
            ) or isinstance(node, parser.Node_memberdefType):
                # We skip the 'file' entries because the file name doesn't form part of the
                # qualified name for the identifier. We skip the 'namespace' entries because if we
                # find an object through the namespace 'compound' entry in the index.xml then we'll
                # also have the 'compounddef' entry in our node stack and we'll get it from that. We
                # need the 'compounddef' entry because if we find the object through the 'file'
                # entry in the index.xml file then we need to get the namespace name from somewhere
                names.insert(0, node.name)
            if (
                isinstance(node, parser.Node_compounddefType)
                and node.kind == parser.DoxCompoundKind.namespace
            ):
                # Nested namespaces include their parent namespace(s) in compoundname. ie,
                # compoundname is 'foo::bar' instead of just 'bar' for namespace 'bar' nested in
                # namespace 'foo'. We need full compoundname because node_stack doesn't necessarily
                # include parent namespaces and we stop here in case it does.
                names.insert(0, node.compoundname)
                break

        return "::".join(names)

    def create_template_prefix(self, decl: HasTemplateParamList) -> str:
        if not decl.templateparamlist:
            return ""
        nodes_ = self.render(decl.templateparamlist)
        return "template<" + "".join(n.astext() for n in nodes_) + ">"

    def run_domain_directive(self, kind, names):
        assert self.context

        domain_directive = DomainDirectiveFactory.create(
            self.context.domain, [kind, names] + self.context.directive_args[2:]
        )

        # Translate Breathe's no-link option into the standard noindex option.
        if "no-link" in self.context.directive_args[2]:
            domain_directive.options["noindex"] = True

        config = self.app.env.config
        if config.breathe_debug_trace_directives:  # pragma: no cover
            global _debug_indent
            print(
                "{}Running directive (old): .. {}:: {}".format(
                    "  " * _debug_indent, domain_directive.name, "".join(names)
                )
            )
            _debug_indent += 1

        nodes_ = domain_directive.run()

        if config.breathe_debug_trace_directives:  # pragma: no cover
            _debug_indent -= 1

        # Filter out outer class names if we are rendering a member as a part of a class content.
        if self.context.child:
            namespace_strip(config, nodes_)
        return nodes_

    def create_doxygen_target(self, node):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = self.get_refid(node.id)
        return self.target_handler(self.document, refid)

    def title(self, node) -> list[nodes.Node]:
        nodes_ = []

        # Variable type or function return type
        nodes_.extend(self.render_optional(node.type_))
        if nodes_:
            nodes_.append(nodes.Text(" "))
        nodes_.append(addnodes.desc_name(text=node.name))
        return nodes_

    def description(self, node: HasDescriptions) -> list[nodes.Node]:
        brief = self.render_optional(node.briefdescription)
        descr = node.detaileddescription
        if isinstance(node, parser.Node_memberdefType):
            params = [
                parser.Node_docParamListItem(
                    parameterdescription=p.briefdescription,
                    parameternamelist=[
                        parser.Node_docParamNameList(
                            parametername=[parser.Node_docParamName([p.declname or ""])]
                        )
                    ],
                )
                for p in node.param
                if p.briefdescription
            ]

            if params:
                content: list[parser.ListItem_descriptionType] = []
                content.append(
                    parser.TaggedValue[Literal["para"], parser.Node_docParaType](
                        "para",
                        parser.Node_docParaType([
                            parser.TaggedValue[
                                Literal["parameterlist"], parser.Node_docParamListType
                            ](
                                "parameterlist",
                                parser.Node_docParamListType(
                                    params, kind=parser.DoxParamListKind.param
                                ),
                            )
                        ]),
                    )
                )
                title = None
                if descr is not None:
                    content.extend(descr)
                    title = descr.title
                descr = parser.Node_descriptionType(content, title=title)
        detailed = self.detaileddescription(descr)
        return brief + detailed

    def detaileddescription(self, descr: parser.Node_descriptionType | None) -> list[nodes.Node]:
        detailedCand = self.render_optional(descr)
        # all field_lists must be at the top-level of the desc_content, so pull them up
        fieldLists: list[nodes.field_list] = []
        admonitions: list[nodes.Node] = []

        def pullup(node, typ, dest):
            for n in list(_findall_compat(node, typ)):
                del n.parent[n.parent.index(n)]
                dest.append(n)

        detailed: list[nodes.Node] = []
        for candNode in detailedCand:
            pullup(candNode, nodes.field_list, fieldLists)
            pullup(candNode, nodes.note, admonitions)
            pullup(candNode, nodes.warning, admonitions)
            # and collapse paragraphs
            for para in _findall_compat(candNode, nodes.paragraph):
                parent = para.parent
                assert parent is None or isinstance(parent, nodes.Element)
                if parent and len(parent) == 1 and isinstance(parent, nodes.paragraph):
                    para.replace_self(para.children)

            # and remove empty top-level paragraphs
            if isinstance(candNode, nodes.paragraph) and len(candNode) == 0:
                continue
            detailed.append(candNode)

        # make one big field list instead to the Sphinx transformer can make it pretty
        if len(fieldLists) > 1:
            fieldList = nodes.field_list()
            for fl in fieldLists:
                fieldList.extend(fl)
            fieldLists = [fieldList]

        # using "extend" instead of addition is slightly more verbose but is
        # needed to get around the mypy issue
        # https://github.com/python/mypy/issues/3933
        if self.app.config.breathe_order_parameters_first:
            detailed.extend(fieldLists)
            detailed.extend(admonitions)
        else:
            detailed.extend(admonitions)
            detailed.extend(fieldLists)
        return detailed

    def update_signature(self, signature, obj_type):
        """Update the signature node if necessary, e.g. add qualifiers."""
        prefix = obj_type + " "
        annotation = addnodes.desc_annotation(prefix, prefix)
        if signature[0].tagname != "desc_name":
            signature[0] = annotation
        else:
            signature.insert(0, annotation)

    def render_declaration(
        self, node: parser.Node_memberdefType, declaration=None, description=None, **kwargs
    ):
        if declaration is None:
            declaration = self.get_fully_qualified_name()
        obj_type = kwargs.get("objtype", None)
        if obj_type is None:
            obj_type = node.kind.value
        nodes_ = self.run_domain_directive(obj_type, [declaration.replace("\n", " ")])
        target = None
        if self.app.env.config.breathe_debug_trace_doxygen_ids:
            target = self.create_doxygen_target(node)
            if len(target) == 0:
                print("{}Doxygen target (old): (none)".format("  " * _debug_indent))
            else:
                print("{}Doxygen target (old): {}".format("  " * _debug_indent, target[0]["ids"]))

        rst_node = nodes_[1]
        doc = rst_node.document
        assert doc is not None
        finder = NodeFinder(doc)
        rst_node.walk(finder)

        assert finder.declarator is not None
        assert finder.content is not None
        signode = finder.declarator
        contentnode = finder.content

        update_signature = kwargs.get("update_signature", None)
        if update_signature is not None:
            update_signature(signode, obj_type)
        if description is None:
            description = self.description(node)
        if not self.app.env.config.breathe_debug_trace_doxygen_ids:
            target = self.create_doxygen_target(node)
        assert target is not None
        signode.insert(0, target)
        contentnode.extend(description)
        return nodes_

    @node_handler(parser.Node_DoxygenTypeIndex)
    def visit_doxygen(self, node: parser.Node_DoxygenTypeIndex) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = []

        # Process all the compound children
        for n in node.compound:
            nodelist.extend(self.render(n))
        return nodelist

    @node_handler(parser.Node_DoxygenType)
    def visit_doxygendef(self, node: parser.Node_DoxygenType) -> list[nodes.Node]:
        assert len(node.compounddef) == 1
        return self.render(node.compounddef[0])

    def visit_union(self, node: HasRefID) -> list[nodes.Node]:
        # Read in the corresponding xml file and process
        file_data = self.parse_compound(node.refid)
        assert len(file_data.compounddef) == 1
        nodeDef = file_data.compounddef[0]

        assert self.context is not None
        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(nodeDef)

        with WithContext(self, new_context):
            names = self.get_qualification()
            if self.nesting_level == 0:
                names.extend(nodeDef.compoundname.split("::"))
            else:
                names.append(nodeDef.compoundname.split("::")[-1])
            declaration = self.join_nested_name(names)

            nodes_ = self.handle_compounddef_declaration(
                nodeDef, nodeDef.kind.value, declaration, file_data, new_context, parent_context
            )
        return nodes_

    def visit_class(self, node: HasRefID) -> list[nodes.Node]:
        # Read in the corresponding xml file and process
        file_data = self.parse_compound(node.refid)
        assert len(file_data.compounddef) == 1
        nodeDef = file_data.compounddef[0]

        assert self.context is not None
        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(nodeDef)

        domain = self.get_domain()

        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            kind = nodeDef.kind
            # Defer to domains specific directive.

            names = self.get_qualification()
            # strip out any template arguments before splitting on '::', to
            # avoid errors if a template specialization has qualified arguments
            # (see examples/specific/cpp_ns_template_specialization)
            cleaned_name, _sep, _rest = nodeDef.compoundname.partition("<")
            cname = split_name(cleaned_name)
            if self.nesting_level == 0:
                names.extend(cname)
            else:
                names.append(cname[-1])
            decls = [
                self.create_template_prefix(nodeDef),
                self.join_nested_name(names),
            ]
            # add base classes
            if len(nodeDef.basecompoundref) != 0:
                decls.append(":")
            first = True
            for base in nodeDef.basecompoundref:
                if not first:
                    decls.append(",")
                else:
                    first = False
                if base.prot is not None and domain != "cs":
                    decls.append(base.prot.value)
                if base.virt == parser.DoxVirtualKind.virtual:
                    decls.append("virtual")
                decls.append(base[0])
            declaration = " ".join(decls)

            assert kind in (
                parser.DoxCompoundKind.class_,
                parser.DoxCompoundKind.struct,
                parser.DoxCompoundKind.interface,
            )
            display_obj_type = "interface" if kind == parser.DoxCompoundKind.interface else None
            nodes_ = self.handle_compounddef_declaration(
                nodeDef,
                nodeDef.kind.value,
                declaration,
                file_data,
                new_context,
                parent_context,
                display_obj_type,
            )
            if "members-only" in self.context.directive_args[2]:
                assert len(nodes_) >= 2
                assert isinstance(nodes_[1], addnodes.desc)
                assert len(nodes_[1]) >= 2
                assert isinstance(nodes_[1][1], addnodes.desc_content)
                return list(nodes_[1][1].children)
        return nodes_

    def visit_namespace(self, node: HasRefID) -> list[nodes.Node]:
        # Read in the corresponding xml file and process
        file_data = self.parse_compound(node.refid)
        assert len(file_data.compounddef) == 1
        nodeDef = file_data.compounddef[0]

        assert self.context is not None

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(nodeDef)

        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            names = self.get_qualification()
            if self.nesting_level == 0:
                names.extend(nodeDef.compoundname.split("::"))
            else:
                names.append(nodeDef.compoundname.split("::")[-1])
            declaration = self.join_nested_name(names)

            display_obj_type = "namespace" if self.get_domain() != "py" else "module"
            nodes_ = self.handle_compounddef_declaration(
                nodeDef,
                nodeDef.kind.value,
                declaration,
                file_data,
                new_context,
                parent_context,
                display_obj_type,
            )
        return nodes_

    def visit_compound(
        self,
        node: HasRefID,
        render_empty_node=True,
        *,
        get_node_info: Callable[[parser.Node_DoxygenType], tuple[str, parser.DoxCompoundKind]]
        | None = None,
        render_signature: Callable[
            [parser.Node_DoxygenType, Sequence[nodes.Element], str, parser.DoxCompoundKind],
            tuple[list[nodes.Node], addnodes.desc_content],
        ]
        | None = None,
    ) -> list[nodes.Node]:
        # Read in the corresponding xml file and process
        file_data = self.parse_compound(node.refid)
        assert len(file_data.compounddef) == 1

        def def_get_node_info(file_data) -> tuple[str, parser.DoxCompoundKind]:
            assert isinstance(node, parser.Node_CompoundType)
            return node.name, parser.DoxCompoundKind(node.kind.value)

        if get_node_info is None:
            get_node_info = def_get_node_info

        name, kind = get_node_info(file_data)
        if kind == parser.DoxCompoundKind.union:
            dom = self.get_domain()
            assert not dom or dom in ("c", "cpp")
            return self.visit_union(node)
        elif kind in (
            parser.DoxCompoundKind.struct,
            parser.DoxCompoundKind.class_,
            parser.DoxCompoundKind.interface,
        ):
            dom = self.get_domain()
            if not dom or dom in ("c", "cpp", "py", "cs"):
                return self.visit_class(node)
        elif kind == parser.DoxCompoundKind.namespace:
            dom = self.get_domain()
            if not dom or dom in ("c", "cpp", "py", "cs"):
                return self.visit_namespace(node)

        assert self.context is not None

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(file_data.compounddef[0])
        rendered_data = self.render(file_data, parent_context)

        if not rendered_data and not render_empty_node:
            return []

        def def_render_signature(
            file_data: parser.Node_DoxygenType, doxygen_target, name, kind: parser.DoxCompoundKind
        ) -> tuple[list[nodes.Node], addnodes.desc_content]:
            # Defer to domains specific directive.

            assert len(file_data.compounddef) == 1
            templatePrefix = self.create_template_prefix(file_data.compounddef[0])
            arg = "%s %s" % (templatePrefix, self.get_fully_qualified_name())

            # add base classes
            if kind in (parser.DoxCompoundKind.class_, parser.DoxCompoundKind.struct):
                bs: list[str] = []
                for base in file_data.compounddef[0].basecompoundref:
                    b: list[str] = []
                    if base.prot is not None:
                        b.append(base.prot.value)
                    if base.virt == parser.DoxVirtualKind.virtual:
                        b.append("virtual")
                    b.append(base[0])
                    bs.append(" ".join(b))
                if len(bs) != 0:
                    arg += " : "
                    arg += ", ".join(bs)

            assert self.context is not None
            self.context.directive_args[1] = [arg]

            nodes_ = self.run_domain_directive(kind.value, self.context.directive_args[1])
            rst_node = nodes_[1]

            doc = rst_node.document
            assert doc is not None
            finder = NodeFinder(doc)
            rst_node.walk(finder)
            assert finder.declarator is not None
            assert finder.content is not None

            if kind in (parser.CompoundKind.interface, parser.CompoundKind.namespace):
                # This is not a real C++ declaration type that Sphinx supports,
                # so we hax the replacement of it.
                finder.declarator[0] = addnodes.desc_annotation(kind.value + " ", kind.value + " ")

            rst_node.children[0].insert(0, doxygen_target)
            return nodes_, finder.content

        if render_signature is None:
            render_signature = def_render_signature

        refid = self.get_refid(node.refid)
        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            nodes_, contentnode = render_signature(
                file_data, self.target_handler(self.document, refid), name, kind
            )

        if file_data.compounddef[0].includes:
            for include in file_data.compounddef[0].includes:
                contentnode.extend(self.render(include, new_context.create_child_context(include)))

        contentnode.extend(rendered_data)
        return nodes_

    def visit_file(self, node: parser.Node_CompoundType) -> list[nodes.Node]:
        def render_signature(
            file_data, doxygen_target, name, kind
        ) -> tuple[list[nodes.Node], addnodes.desc_content]:
            assert self.context is not None
            options = self.context.directive_args[2]
            rst_node: nodes.container | addnodes.desc

            if "content-only" in options:
                rst_node = nodes.container()
            else:
                rst_node = addnodes.desc()

                # Build targets for linking
                targets = []
                targets.extend(doxygen_target)

                title_signode = addnodes.desc_signature()
                title_signode.extend(targets)

                # Set up the title
                #
                # For groups & pages we render the 'title' instead of the 'name'
                # as it more human friendly
                if kind in [DoxCompoundKind.group, DoxCompoundKind.page] and file_data.compounddef:
                    if "no-title" not in options:
                        title_signode.append(nodes.emphasis(text=kind.value))
                        title_signode.append(nodes.Text(" "))
                        title_signode.append(
                            addnodes.desc_name(text=file_data.compounddef[0].title)
                        )
                else:
                    title_signode.append(nodes.emphasis(text=kind.value))
                    title_signode.append(nodes.Text(" "))
                    title_signode.append(addnodes.desc_name(text=name))

                rst_node.append(title_signode)

            rst_node.document = self.state.document
            rst_node["objtype"] = kind.value
            rst_node["domain"] = self.get_domain() or "cpp"

            contentnode = addnodes.desc_content()
            rst_node.append(contentnode)

            return [rst_node], contentnode

        return self.visit_compound(node, render_signature=render_signature)

    # We store both the identified and appropriate title text here as we want to define the order
    # here and the titles for the SectionDefTypeSubRenderer but we don't want the repetition of
    # having two lists in case they fall out of sync
    #
    # If this list is edited, also change the sections option documentation for
    # the doxygen(auto)file directive in documentation/source/file.rst.
    sections = [
        (parser.DoxSectionKind.user_defined, "User Defined"),
        (parser.DoxSectionKind.public_type, "Public Types"),
        (parser.DoxSectionKind.public_func, "Public Functions"),
        (parser.DoxSectionKind.public_attrib, "Public Members"),
        (parser.DoxSectionKind.public_slot, "Public Slots"),
        (parser.DoxSectionKind.signal, "Signals"),
        (parser.DoxSectionKind.dcop_func, "DCOP Function"),
        (parser.DoxSectionKind.property, "Properties"),
        (parser.DoxSectionKind.event, "Events"),
        (parser.DoxSectionKind.public_static_func, "Public Static Functions"),
        (parser.DoxSectionKind.public_static_attrib, "Public Static Attributes"),
        (parser.DoxSectionKind.protected_type, "Protected Types"),
        (parser.DoxSectionKind.protected_func, "Protected Functions"),
        (parser.DoxSectionKind.protected_attrib, "Protected Attributes"),
        (parser.DoxSectionKind.protected_slot, "Protected Slots"),
        (parser.DoxSectionKind.protected_static_func, "Protected Static Functions"),
        (parser.DoxSectionKind.protected_static_attrib, "Protected Static Attributes"),
        (parser.DoxSectionKind.package_type, "Package Types"),
        (parser.DoxSectionKind.package_func, "Package Functions"),
        (parser.DoxSectionKind.package_attrib, "Package Attributes"),
        (parser.DoxSectionKind.package_static_func, "Package Static Functions"),
        (parser.DoxSectionKind.package_static_attrib, "Package Static Attributes"),
        (parser.DoxSectionKind.private_type, "Private Types"),
        (parser.DoxSectionKind.private_func, "Private Functions"),
        (parser.DoxSectionKind.private_attrib, "Private Members"),
        (parser.DoxSectionKind.private_slot, "Private Slots"),
        (parser.DoxSectionKind.private_static_func, "Private Static Functions"),
        (parser.DoxSectionKind.private_static_attrib, "Private Static Attributes"),
        (parser.DoxSectionKind.friend, "Friends"),
        (parser.DoxSectionKind.related, "Related"),
        (parser.DoxSectionKind.define, "Defines"),
        (parser.DoxSectionKind.prototype, "Prototypes"),
        (parser.DoxSectionKind.typedef, "Typedefs"),
        # (parser.DoxSectionKind.concept, "Concepts"),
        (parser.DoxSectionKind.enum, "Enums"),
        (parser.DoxSectionKind.func, "Functions"),
        (parser.DoxSectionKind.var, "Variables"),
    ]

    def render_iterable(
        self, iterable: Iterable[parser.NodeOrValue], tag: str | None = None
    ) -> list[nodes.Node]:
        output: list[nodes.Node] = []
        for entry in iterable:
            output.extend(self.render(entry, tag=tag))
        return output

    def render_tagged_iterable(
        self, iterable: Iterable[parser.TaggedValue[str, parser.NodeOrValue] | str]
    ) -> list[nodes.Node]:
        output: list[nodes.Node] = []
        for entry in iterable:
            output.extend(self.render_tagged(entry))
        return output

    @node_handler(parser.Node_compounddefType)
    def visit_compounddef(self, node: parser.Node_compounddefType) -> list[nodes.Node]:
        assert self.context is not None
        options = self.context.directive_args[2]
        section_order = None
        if "sections" in options:
            section_order = {sec: i for i, sec in enumerate(options["sections"].split(" "))}
        membergroup_order = None
        if "membergroups" in options:
            membergroup_order = {sec: i for i, sec in enumerate(options["membergroups"].split(" "))}
        nodemap: dict[int, list[nodes.Node]] = {}

        def addnode(kind: str, lam):
            if section_order is None:
                nodemap[len(nodemap)] = lam()
            elif kind in section_order:
                nodemap.setdefault(section_order[kind], []).extend(lam())

        if "members-only" not in options:
            if "allow-dot-graphs" in options:
                addnode(
                    "incdepgraph", lambda: self.render_optional(node.incdepgraph, "incdepgraph")
                )
                addnode(
                    "invincdepgraph",
                    lambda: self.render_optional(node.invincdepgraph, "invincdepgraph"),
                )
                addnode(
                    "inheritancegraph",
                    lambda: self.render_optional(node.inheritancegraph, "inheritancegraph"),
                )
                addnode(
                    "collaborationgraph",
                    lambda: self.render_optional(node.collaborationgraph, "collaborationgraph"),
                )

            addnode("briefdescription", lambda: self.render_optional(node.briefdescription))
            addnode(
                "detaileddescription", lambda: self.detaileddescription(node.detaileddescription)
            )

            def render_derivedcompoundref(node):
                if node is None:
                    return []
                output = self.render_iterable(node)
                if not output:
                    return []
                return [
                    nodes.paragraph(
                        "", "", nodes.Text("Subclassed by "), *intersperse(output, nodes.Text(", "))
                    )
                ]

            addnode(
                "derivedcompoundref", lambda: render_derivedcompoundref(node.derivedcompoundref)
            )

        section_nodelists: dict[str, list[nodes.Node]] = {}

        # Get all sub sections
        for sectiondef in node.sectiondef:
            kind = sectiondef.kind
            if section_order is not None and kind.value not in section_order:
                continue
            header = sectiondef.header
            if membergroup_order is not None and header not in membergroup_order:
                continue
            child_nodes = self.render(sectiondef)
            if not child_nodes:
                # Skip empty section
                continue
            rst_node = nodes.container(classes=["breathe-sectiondef"])
            rst_node.document = self.state.document
            rst_node["objtype"] = kind.value
            rst_node.extend(child_nodes)
            # We store the nodes as a list against the kind in a dictionary as the kind can be
            # 'user-edited' and that can repeat so this allows us to collect all the 'user-edited'
            # entries together
            section_nodelists.setdefault(kind.value, []).append(rst_node)

        # Order the results in an appropriate manner
        for kind, _ in self.sections:
            addnode(kind.value, lambda: section_nodelists.get(kind.value, []))

        # Take care of innerclasses
        addnode("innerclass", lambda: self.render_iterable(node.innerclass, "innerclass"))
        addnode(
            "innernamespace", lambda: self.render_iterable(node.innernamespace, "innernamespace")
        )

        if "inner" in options:
            for cnode in node.innergroup:
                file_data = self.parse_compound(cnode.refid)
                assert len(file_data.compounddef) == 1
                inner = file_data.compounddef[0]
                addnode("innergroup", lambda: self.visit_compounddef(inner))

        nodelist = []
        for _, nodes_ in sorted(nodemap.items()):
            nodelist += nodes_

        return nodelist

    section_titles = dict(sections)

    @node_handler(parser.Node_sectiondefType)
    def visit_sectiondef(self, node: parser.Node_sectiondefType) -> list[nodes.Node]:
        assert self.context is not None
        options = self.context.directive_args[2]
        node_list = []
        node_list.extend(self.render_optional(node.description))

        # Get all the memberdef info
        member_def: Iterable[parser.Node_memberdefType]
        if "sort" in options:
            member_def = sorted(node.memberdef, key=lambda x: x.name)
        else:
            member_def = node.memberdef

        node_list.extend(self.render_iterable(member_def))

        if node_list:
            if "members-only" in options:
                return node_list

            text = self.section_titles[node.kind]
            # Override default name for user-defined sections. Use "Unnamed
            # Group" if the user didn't name the section
            # This is different to Doxygen which will track the groups and name
            # them Group1, Group2, Group3, etc.
            if node.kind == parser.DoxSectionKind.user_defined:
                if node.header:
                    text = node.header
                else:
                    text = "Unnamed Group"

            # Use rubric for the title because, unlike the docutils element "section",
            # it doesn't interfere with the document structure.
            idtext = text.replace(" ", "-").lower()
            rubric = nodes.rubric(
                text=text,
                classes=["breathe-sectiondef-title"],
                ids=["breathe-section-title-" + idtext],
            )
            res: list[nodes.Node] = [rubric]
            return res + node_list
        return []

    @node_handler(parser.Node_docRefTextType)
    @node_handler(parser.Node_refTextType)
    def visit_docreftext(
        self, node: parser.Node_docRefTextType | parser.Node_incType | parser.Node_refTextType
    ) -> list[nodes.Node]:
        nodelist: list[nodes.Node]

        if isinstance(node, parser.Node_incType):
            nodelist = self.render_iterable(node)
        else:
            nodelist = self.render_tagged_iterable(node)

            # TODO: "para" in compound.xsd is an empty tag; figure out what this
            # is supposed to do
            # for name, value in map(parser.tag_name_value, node):
            #     if name == "para":
            #         nodelist.extend(self.render(value))

        refid = self.get_refid(node.refid or "")

        assert nodelist
        nodelist = [
            addnodes.pending_xref(
                "",
                reftype="ref",
                refdomain="std",
                refexplicit=True,
                refid=refid,
                reftarget=refid,
                *nodelist,
            )
        ]
        return nodelist

    @node_handler(parser.Node_docHeadingType)
    def visit_docheading(self, node: parser.Node_docHeadingType) -> list[nodes.Node]:
        """Heading renderer.

        Renders embedded headlines as emphasized text. Different heading levels
        are not supported.
        """
        nodelist = self.render_tagged_iterable(node)
        return [nodes.emphasis("", "", *nodelist)]

    @node_handler(parser.Node_docParaType)
    def visit_docpara(self, node: parser.Node_docParaType) -> list[nodes.Node]:
        """
        <para> tags in the Doxygen output tend to contain either text or a single other tag of
        interest. So whilst it looks like we're combined descriptions and program listings and
        other things, in the end we generally only deal with one per para tag. Multiple
        neighbouring instances of these things tend to each be in a separate neighbouring para tag.
        """

        nodelist = []

        if self.context and self.context.directive_args[0] == "doxygenpage":
            nodelist.extend(self.render_tagged_iterable(node))
        else:
            contentNodeCands = []
            for item in get_content(node):
                contentNodeCands.extend(self.render_tagged(item))
            # if there are consecutive nodes.Text we should collapse them
            # and rerender them to ensure the right paragraphifaction
            contentNodes: list[nodes.Node] = []
            for n in contentNodeCands:
                if len(contentNodes) != 0 and isinstance(contentNodes[-1], nodes.Text):
                    if isinstance(n, nodes.Text):
                        prev = contentNodes.pop()
                        contentNodes.extend(self.render_string(prev.astext() + n.astext()))
                        continue  # we have handled this node
                contentNodes.append(n)
            nodelist.extend(contentNodes)
            nodelist.extend(self.render_iterable(get_images(node)))

            paramList = self.render_iterable(get_parameterlists(node))
            defs = []
            fields = []
            for n in self.render_iterable(get_simplesects(node)):
                if isinstance(n, nodes.definition_list_item):
                    defs.append(n)
                elif isinstance(n, nodes.field_list):
                    fields.append(n)
                else:
                    nodelist.append(n)

            # note: all these gets pulled up and reordered in description()
            if len(defs) != 0:
                deflist = nodes.definition_list("", *defs)
                nodelist.append(deflist)
            nodelist.extend(paramList)
            nodelist.extend(fields)

        # And now all kinds of cleanup steps
        # ----------------------------------

        # trim trailing whitespace
        while len(nodelist) != 0:
            last = nodelist[-1]
            if not isinstance(last, nodes.Text):
                break
            if last.astext().strip() != "":
                break
            nodelist.pop()

        # https://github.com/breathe-doc/breathe/issues/827
        # verbatim nodes should not be in a paragraph:
        if len(nodelist) == 1 and isinstance(nodelist[0], nodes.literal_block):
            return nodelist

        return [nodes.paragraph("", "", *nodelist)]

    visit_docparblock = node_handler(parser.Node_docParBlockType)(render_iterable)

    @node_handler(parser.Node_docBlockQuoteType)
    def visit_docblockquote(self, node: parser.Node_docBlockQuoteType) -> list[nodes.Node]:
        nodelist = self.render_iterable(node)
        # catch block quote attributions here; the <ndash/> tag is the only identifier,
        # and it is nested within a subsequent <para> tag
        if nodelist and nodelist[-1].astext().startswith("&#8212;"):
            # nodes.attribution prepends the author with an emphasized dash.
            # replace the &#8212; placeholder and strip any leading whitespace.
            text = nodelist[-1].astext().replace("&#8212;", "").lstrip()
            nodelist[-1] = nodes.attribution("", text)
        return [nodes.block_quote("", classes=[], *nodelist)]

    @node_handler(parser.Node_docImageType)
    def visit_docimage(self, node: parser.Node_docImageType) -> list[nodes.Node]:
        """Output docutils image node using name attribute from xml as the uri"""

        path_to_image = node.name
        if path_to_image is None:
            path_to_image = ""
        elif not url_re.match(path_to_image):
            path_to_image = self.project_info.sphinx_abs_path_to_file(path_to_image)

        options = {"uri": path_to_image}
        return [nodes.image("", **options)]

    @node_handler(parser.Node_docURLLink)
    def visit_docurllink(self, node: parser.Node_docURLLink) -> list[nodes.Node]:
        """Url Link Renderer"""

        nodelist = self.render_tagged_iterable(node)
        return [nodes.reference("", "", refuri=node.url, *nodelist)]

    @tagged_node_handler(parser.Node_docMarkupType)
    def visit_docmarkup(self, tag: str, node: parser.Node_docMarkupType) -> list[nodes.Node]:
        nodelist = self.render_tagged_iterable(node)
        creator: type[nodes.TextElement] = nodes.inline
        if tag == "emphasis":
            creator = nodes.emphasis
        elif tag == "computeroutput":
            creator = nodes.literal
        elif tag == "bold":
            creator = nodes.strong
        elif tag == "superscript":
            creator = nodes.superscript
        elif tag == "subscript":
            creator = nodes.subscript
        elif tag == "center":
            print("Warning: does not currently handle 'center' text display")
        elif tag == "small":
            print("Warning: does not currently handle 'small' text display")
        return [creator("", "", *nodelist)]

    @node_handler(parser.Node_docSect1Type)
    def visit_docsect1(self, node: parser.Node_docSect1Type) -> list[nodes.Node]:
        return self.visit_docsectN(node, 0)

    @node_handler(parser.Node_docSect2Type)
    def visit_docsect2(self, node: parser.Node_docSect2Type) -> list[nodes.Node]:
        return self.visit_docsectN(node, 1)

    @node_handler(parser.Node_docSect3Type)
    def visit_docsect3(self, node: parser.Node_docSect3Type) -> list[nodes.Node]:
        return self.visit_docsectN(node, 2)

    def visit_docsectN(
        self,
        node: parser.Node_docSect1Type | parser.Node_docSect2Type | parser.Node_docSect3Type,
        depth: int,
    ) -> list[nodes.Node]:
        """
        Docutils titles are defined by their level inside the document.

        Doxygen command mapping to XML element name:
        @section == sect1, @subsection == sect2, @subsubsection == sect3
        """
        # sect2 and sect3 elements can appear outside of sect1/sect2 elements so
        # we need to check how deep we actually are
        actual_d = 0
        assert self.context
        for n in self.context.node_stack[1:]:
            if isinstance(
                n.value,
                (parser.Node_docSect1Type, parser.Node_docSect2Type, parser.Node_docSect3Type),
            ):
                actual_d += 1

        title_nodes = self.render_tagged_iterable(node.title) if node.title else []
        if actual_d == depth:
            section = nodes.section()
            section["ids"].append(self.get_refid(node.id))
            section += nodes.title("", "", *title_nodes)
            section += self.create_doxygen_target(node)
            section += self.render_tagged_iterable(node)
            return [section]
        else:
            # If the actual depth doesn't match the specified depth, don't
            # create a section element, just use an emphasis element as the
            # title.
            #
            # This is probably not the best way to handle such a case. I chose
            # it because it's what visit_docheading does. It shouldn't come up
            # often, anyway.
            #     -- Rouslan
            content: list[nodes.Node] = [nodes.emphasis("", "", *title_nodes)]
            content.extend(self.create_doxygen_target(node))
            content.extend(self.render_tagged_iterable(node))
            return content

    @node_handler(parser.Node_docSimpleSectType)
    def visit_docsimplesect(self, node: parser.Node_docSimpleSectType) -> list[nodes.Node]:
        """Other Type documentation such as Warning, Note, Returns, etc"""

        # for those that should go into a field list, just render them as that,
        # and it will be pulled up later
        nodelist = self.render_iterable(node.para)

        if node.kind in (
            parser.DoxSimpleSectKind.pre,
            parser.DoxSimpleSectKind.post,
            parser.DoxSimpleSectKind.return_,
        ):
            return [
                nodes.field_list(
                    "",
                    nodes.field(
                        "",
                        nodes.field_name("", nodes.Text(node.kind.value)),
                        nodes.field_body("", *nodelist),
                    ),
                )
            ]
        elif node.kind == parser.DoxSimpleSectKind.warning:
            return [nodes.warning("", *nodelist)]
        elif node.kind == parser.DoxSimpleSectKind.note:
            return [nodes.note("", *nodelist)]
        elif node.kind == parser.DoxSimpleSectKind.see:
            return [addnodes.seealso("", *nodelist)]
        elif node.kind == parser.DoxSimpleSectKind.remark:
            nodelist.insert(0, nodes.title("", nodes.Text(node.kind.value.capitalize())))
            return [nodes.admonition("", classes=[node.kind.value], *nodelist)]

        if node.kind == parser.DoxSimpleSectKind.par:
            text = self.render(node.title)
        else:
            text = [nodes.Text(node.kind.value.capitalize())]
        # TODO: is this working as intended? there is something strange with the types
        title = nodes.strong("", "", *text)

        term = nodes.term("", "", title)
        definition = nodes.definition("", *nodelist)

        return [nodes.definition_list_item("", term, definition)]

    visit_doctitle = node_handler(parser.Node_docTitleType)(render_tagged_iterable)

    @node_handler(parser.Node_docFormulaType)
    def visit_docformula(self, node: parser.Node_docFormulaType) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = []
        for latex in node:
            docname = self.state.document.settings.env.docname
            # Strip out the doxygen markup that slips through
            # Either inline
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1]
                nodelist.append(
                    nodes.math(text=latex, label=None, nowrap=False, docname=docname, number=None)
                )
            # Else we're multiline
            else:
                if latex.startswith("\\[") and latex.endswith("\\]"):
                    latex = latex[2:-2:]

                nodelist.append(
                    nodes.math_block(
                        text=latex, label=None, nowrap=False, docname=docname, number=None
                    )
                )
        return nodelist

    @node_handler(parser.Node_listingType)
    def visit_listing(self, node: parser.Node_listingType) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = []
        for i, item in enumerate(node.codeline):
            # Put new lines between the lines
            if i:
                nodelist.append(nodes.Text("\n"))
            nodelist.extend(self.render(item))

        # Add blank string at the start otherwise for some reason it renders
        # the pending_xref tags around the kind in plain text
        block = nodes.literal_block("", "", *nodelist)
        domain = filetypes.get_pygments_alias(node.filename or "") or filetypes.get_extension(
            node.filename or ""
        )
        if domain:
            block["language"] = domain
        return [block]

    @node_handler(parser.Node_codelineType)
    def visit_codeline(self, node: parser.Node_codelineType) -> list[nodes.Node]:
        return self.render_iterable(node.highlight)

    visit_highlight = node_handler(parser.Node_highlightType)(render_tagged_iterable)

    def _nested_inline_parse_with_titles(self, content, node) -> str:
        """
        This code is basically a customized nested_parse_with_titles from
        docutils, using the InlineText class on the statemachine.
        """
        surrounding_title_styles = self.state.memo.title_styles
        surrounding_section_level = self.state.memo.section_level
        self.state.memo.title_styles = []
        self.state.memo.section_level = 0
        try:
            return self.state.nested_parse(
                content,
                0,
                node,
                match_titles=1,
                state_machine_kwargs={
                    "state_classes": (InlineText,),
                    "initial_state": "InlineText",
                },
            )
        finally:
            self.state.memo.title_styles = surrounding_title_styles
            self.state.memo.section_level = surrounding_section_level

    def visit_verbatim(self, node: str) -> list[nodes.Node]:
        if not node.strip().startswith("embed:rst"):
            # Remove trailing new lines. Purely subjective call from viewing results
            text = node.rstrip()

            # Handle has a preformatted text
            return [nodes.literal_block(text, text)]

        is_inline = False

        # do we need to strip leading asterisks?
        # NOTE: We could choose to guess this based on every line starting with '*'.
        #   However This would have a side-effect for any users who have an rst-block
        #   consisting of a simple bullet list.
        #   For now we just look for an extended embed tag
        if node.strip().startswith("embed:rst:leading-asterisk"):
            lines: Iterable[str] = node.splitlines()
            # Replace the first * on each line with a blank space
            lines = [text.replace("*", " ", 1) for text in lines]
            node = "\n".join(lines)

        # do we need to strip leading ///?
        elif node.strip().startswith("embed:rst:leading-slashes"):
            lines = node.splitlines()
            # Replace the /// on each line with three blank spaces
            lines = [text.replace("///", "   ", 1) for text in lines]
            node = "\n".join(lines)

        elif node.strip().startswith("embed:rst:inline"):
            # Inline all text inside the verbatim
            node = "".join(node.splitlines())
            is_inline = True

        if is_inline:
            node = node.replace("embed:rst:inline", "", 1)
        else:
            # Remove the first line which is "embed:rst[:leading-asterisk]"
            node = "\n".join(node.split("\n")[1:])

            # Remove starting whitespace
            node = textwrap.dedent(node)

        # Inspired by autodoc.py in Sphinx
        rst = StringList()
        for line in node.split("\n"):
            rst.append(line, "<breathe>")

        # Parent node for the generated node subtree
        rst_node: nodes.Node
        if is_inline:
            rst_node = nodes.inline()
        else:
            rst_node = nodes.paragraph()
        rst_node.document = self.state.document

        # Generate node subtree
        if is_inline:
            self._nested_inline_parse_with_titles(rst, rst_node)
        else:
            nested_parse_with_titles(self.state, rst, rst_node)

        return [rst_node]

    @node_handler(parser.Node_incType)
    def visit_inc(self, node: parser.Node_incType) -> list[nodes.Node]:
        if not self.app.config.breathe_show_include:
            return []

        compound_link: list[nodes.Node] = [nodes.Text("".join(node))]
        if node.refid:
            compound_link = self.visit_docreftext(node)
        if node.local:
            text = [nodes.Text('#include "'), *compound_link, nodes.Text('"')]
        else:
            text = [nodes.Text("#include <"), *compound_link, nodes.Text(">")]

        return [nodes.container("", nodes.emphasis("", "", *text))]

    @node_handler(parser.Node_refType)
    def visit_ref(self, node: parser.Node_refType) -> list[nodes.Node]:
        def get_node_info(file_data: parser.Node_DoxygenType):
            name = "".join(node)
            name = name.rsplit("::", 1)[-1]
            assert len(file_data.compounddef) == 1
            return name, file_data.compounddef[0].kind

        return self.visit_compound(node, False, get_node_info=get_node_info)

    @node_handler(parser.Node_docListItemType)
    def visit_doclistitem(self, node: parser.Node_docListItemType) -> list[nodes.Node]:
        """List item renderer. Render all the children depth-first.
        Upon return expand the children node list into a docutils list-item.
        """
        nodelist = self.render_iterable(node)
        return [nodes.list_item("", *nodelist)]

    numeral_kind = ["arabic", "loweralpha", "lowerroman", "upperalpha", "upperroman"]

    def render_unordered(self, children) -> list[nodes.Node]:
        nodelist_list = nodes.bullet_list("", *children)
        return [nodelist_list]

    def render_enumerated(self, children, nesting_level) -> list[nodes.Node]:
        nodelist_list = nodes.enumerated_list("", *children)
        idx = nesting_level % len(SphinxRenderer.numeral_kind)
        nodelist_list["enumtype"] = SphinxRenderer.numeral_kind[idx]
        nodelist_list["prefix"] = ""
        nodelist_list["suffix"] = "."
        return [nodelist_list]

    @tagged_node_handler(parser.Node_docListType)
    def visit_doclist(self, tag: str, node: parser.Node_docListType) -> list[nodes.Node]:
        """List renderer

        The specifics of the actual list rendering are handled by the
        decorator around the generic render function.
        Render all the children depth-first."""
        """ Call the wrapped render function. Update the nesting level for the enumerated lists. """
        if tag == "itemizedlist":
            val = self.render_iterable(node)
            return self.render_unordered(children=val)
        elif tag == "orderedlist":
            self.nesting_level += 1
            val = self.render_iterable(node)
            self.nesting_level -= 1
            return self.render_enumerated(children=val, nesting_level=self.nesting_level)
        return []

    @node_handler(parser.Node_compoundRefType)
    def visit_compoundref(self, node: parser.Node_compoundRefType) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = self.render_iterable(node)
        refid = None
        if node.refid is not None:
            refid = self.get_refid(node.refid)
        if refid is not None:
            assert nodelist
            nodelist = [
                addnodes.pending_xref(
                    "",
                    reftype="ref",
                    refdomain="std",
                    refexplicit=True,
                    refid=refid,
                    reftarget=refid,
                    *nodelist,
                )
            ]
        return nodelist

    @node_handler(parser.Node_docXRefSectType)
    def visit_docxrefsect(self, node: parser.Node_docXRefSectType) -> list[nodes.Node]:
        assert self.app.env is not None

        signode = addnodes.desc_signature()
        title = node.xreftitle[0] + ":"
        titlenode = nodes.emphasis(text=title)
        ref = addnodes.pending_xref(
            "",
            reftype="ref",
            refdomain="std",
            refexplicit=True,
            reftarget=node.id,
            refdoc=self.app.env.docname,
            *[titlenode],
        )
        signode += ref

        nodelist = self.render(node.xrefdescription)
        contentnode = addnodes.desc_content()
        contentnode += nodelist

        descnode = addnodes.desc()
        descnode["objtype"] = "xrefsect"
        descnode["domain"] = self.get_domain() or "cpp"
        descnode += signode
        descnode += contentnode

        return [descnode]

    @node_handler(parser.Node_docVariableListType)
    def visit_docvariablelist(self, node: parser.Node_docVariableListType) -> list[nodes.Node]:
        output: list[nodes.Node] = []
        for n in node:
            descnode = addnodes.desc()
            descnode["objtype"] = "varentry"
            descnode["domain"] = self.get_domain() or "cpp"
            signode = addnodes.desc_signature()
            signode += self.render_optional(n.varlistentry)
            descnode += signode
            contentnode = addnodes.desc_content()
            contentnode += self.render_iterable(n.listitem)
            descnode += contentnode
            output.append(descnode)
        return output

    @node_handler(parser.Node_docVarListEntryType)
    def visit_docvarlistentry(self, node: parser.Node_docVarListEntryType) -> list[nodes.Node]:
        return self.render_tagged_iterable(node.term)

    @node_handler(parser.Node_docAnchorType)
    def visit_docanchor(self, node: parser.Node_docAnchorType) -> list[nodes.Node]:
        return list(self.create_doxygen_target(node))

    @node_handler(parser.Node_docEntryType)
    def visit_docentry(self, node: parser.Node_docEntryType) -> list[nodes.Node]:
        col = nodes.entry()
        col += self.render_iterable(node.para)
        if node.thead:
            col["heading"] = True
        if node.rowspan:
            col["morerows"] = int(node.rowspan) - 1
        if node.colspan:
            col["morecols"] = int(node.colspan) - 1
        return [col]

    @node_handler(parser.Node_docRowType)
    def visit_docrow(self, node: parser.Node_docRowType) -> list[nodes.Node]:
        row = nodes.row()
        cols = self.render_iterable(node.entry)
        elem: nodes.thead | nodes.tbody
        if all(cast("nodes.Element", col).get("heading", False) for col in cols):
            elem = nodes.thead()
        else:
            elem = nodes.tbody()
        row += cols
        elem.append(row)
        return [elem]

    @node_handler(parser.Node_docTableType)
    def visit_doctable(self, node: parser.Node_docTableType) -> list[nodes.Node]:
        table = nodes.table()
        table["classes"] += ["colwidths-auto"]
        tgroup = nodes.tgroup(cols=node.cols)
        for _ in range(node.cols):
            colspec = nodes.colspec()
            colspec.attributes["colwidth"] = "auto"
            tgroup += colspec
        table += tgroup
        rows = self.render_iterable(node.row)

        # this code depends on visit_docrow(), and expects the same elements used to
        # "envelop" rows there, namely thead and tbody (eg it will need to be updated
        # if Doxygen one day adds support for tfoot)

        tags: defaultdict[str, list] = defaultdict(list)
        for row in rows:
            assert isinstance(row, nodes.Element)
            tags[row.starttag()].append(row.next_node())

        def merge_row_types(root, elem, elems):
            for node in elems:
                elem += node
            root += elem

        for klass in [nodes.thead, nodes.tbody]:
            obj = klass()
            if obj.starttag() in tags:
                merge_row_types(tgroup, obj, tags[obj.starttag()])

        return [table]

    visit_description = node_handler(parser.Node_descriptionType)(render_tagged_iterable)

    visit_linkedtext = node_handler(parser.Node_linkedTextType)(render_tagged_iterable)

    def visit_function(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        dom = self.get_domain()
        if not dom or dom in ("c", "cpp", "py", "cs"):
            names = self.get_qualification()
            names.append(node.name)
            name = self.join_nested_name(names)
            if dom == "py":
                declaration = name + (node.argsstring or "")
            elif dom == "cs":
                declaration = " ".join([
                    self.create_template_prefix(node),
                    "".join(n.astext() for n in self.render(node.type)),
                    name,
                    node.argsstring or "",
                ])
            else:
                elements = [self.create_template_prefix(node)]
                if node.static:
                    elements.append("static")
                if node.inline:
                    elements.append("inline")
                if node.kind == parser.DoxMemberKind.friend:
                    elements.append("friend")
                if node.virt in (parser.DoxVirtualKind.virtual, parser.DoxVirtualKind.pure_virtual):
                    elements.append("virtual")
                if node.explicit:
                    elements.append("explicit")
                if node.constexpr:
                    elements.append("constexpr")
                if node.consteval:
                    elements.append("consteval")

                typ = strip_legacy_qualifiers("".join(n.astext() for n in self.render(node.type)))
                elements.extend((typ, name, node.argsstring or ""))
                declaration = " ".join(elements)
            return self.handle_declaration(node, node.kind.value, declaration)
        else:
            # Get full function signature for the domain directive.
            param_list = []
            for param in node.param:
                assert self.context is not None
                param = self.context.mask_factory.mask(param)
                param_decl = get_param_decl(param)
                param_list.append(param_decl)
            templatePrefix = self.create_template_prefix(node)
            sig_def = get_definition_without_template_args(node)
            signature = f"{templatePrefix}{sig_def}({', '.join(param_list)})"

            # Add CV-qualifiers.
            if node.const:
                signature += " const"
            # The doxygen xml output doesn't register 'volatile' as the xml attribute for functions
            # until version 1.8.8 so we also check argsstring:
            #     https://bugzilla.gnome.org/show_bug.cgi?id=733451
            if node.volatile or (node.argsstring and node.argsstring.endswith("volatile")):
                signature += " volatile"

            if node.refqual == parser.DoxRefQualifierKind.lvalue:
                signature += "&"
            elif node.refqual == parser.DoxRefQualifierKind.rvalue:
                signature += "&&"

            # Add `= 0` for pure virtual members.
            if node.virt == parser.DoxVirtualKind.pure_virtual:
                signature += "= 0"

            assert self.context is not None
            self.context.directive_args[1] = [signature]

            nodes_ = self.run_domain_directive(node.kind, self.context.directive_args[1])

            assert self.app.env is not None
            target = None
            if self.app.env.config.breathe_debug_trace_doxygen_ids:
                target = self.create_doxygen_target(node)
                if len(target) == 0:
                    print("{}Doxygen target (old): (none)".format("  " * _debug_indent))
                else:
                    print(
                        "{}Doxygen target (old): {}".format("  " * _debug_indent, target[0]["ids"])
                    )

            rst_node = nodes_[1]
            assert isinstance(rst_node, nodes.Element)
            doc = rst_node.document
            assert doc is not None
            finder = NodeFinder(doc)
            rst_node.walk(finder)
            assert finder.content is not None

            # Templates have multiple signature nodes in recent versions of Sphinx.
            # Insert Doxygen target into the first signature node.
            if not self.app.env.config.breathe_debug_trace_doxygen_ids:
                target = self.create_doxygen_target(node)
            assert target is not None

            # the type is cast to "Any" to get around missing typing info in
            # docutils 0.20.1
            cast("Any", rst_node.children[0]).insert(0, target)

            finder.content.extend(self.description(node))
            return nodes_

    def visit_define(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        declaration = node.name
        if node.param:
            declaration += "("
            for i, parameter in enumerate(node.param):
                if i:
                    declaration += ", "
                if parameter.defname:
                    declaration += parameter.defname
            declaration += ")"

        # TODO: remove this once Sphinx supports definitions for macros
        def add_definition(declarator: Declarator) -> None:
            if node.initializer and self.app.config.breathe_show_define_initializer:
                declarator.append(nodes.Text(" "))
                declarator.extend(self.render(node.initializer))

        return self.handle_declaration(
            node, node.kind.value, declaration, declarator_callback=add_definition
        )

    def visit_enum(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        def content(contentnode):
            contentnode.extend(self.description(node))
            values = nodes.emphasis("", nodes.Text("Values:"))
            title = nodes.paragraph("", "", values)
            contentnode += title
            enums = self.render_iterable(node.enumvalue)
            contentnode.extend(enums)

        names = self.get_qualification()
        names.append(node.name)
        declaration = self.join_nested_name(names)
        dom = self.get_domain()
        if (not dom or dom == "cpp") and node.strong:
            # It looks like Doxygen does not make a difference
            # between 'enum class' and 'enum struct',
            # so render them both as 'enum class'.
            obj_type = "enum-class"
            underlying_type = "".join(n.astext() for n in self.render(node.type))
            if len(underlying_type.strip()) != 0:
                declaration += " : "
                declaration += underlying_type
        else:
            obj_type = "enum"
        return self.handle_declaration(node, obj_type, declaration, content_callback=content)

    @node_handler(parser.Node_enumvalueType)
    def visit_enumvalue(self, node: parser.Node_enumvalueType) -> list[nodes.Node]:
        if self.app.config.breathe_show_enumvalue_initializer:
            declaration = node.name + self.make_initializer(node)
        else:
            declaration = node.name

        def content(contentnode: addnodes.desc_content):
            contentnode.extend(self.description(node))

        return self.handle_declaration(node, "enumvalue", declaration, content_callback=content)

    def visit_typedef(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        type_ = "".join(n.astext() for n in self.render(node.type))
        names = self.get_qualification()
        names.append(node.name)
        name = self.join_nested_name(names)
        if node.definition and node.definition.startswith("using "):
            # TODO: looks like Doxygen does not generate the proper XML
            #       for the template parameter list
            declaration = self.create_template_prefix(node)
            declaration += " " + name + " = " + type_
        else:
            # TODO: Both "using" and "typedef" keywords get into this function,
            #   and if no @typedef comment was added, the definition should
            #   contain the full text. If a @typedef was used instead, the
            #   definition has only the typename, which makes it impossible to
            #   distinguish between them so fallback to "typedef" behavior here.
            declaration = " ".join([type_, name, node.argsstring or ""])
        return self.handle_declaration(node, node.kind.value, declaration)

    def make_initializer(self, node) -> str:
        initializer = node.initializer
        signature: list[nodes.Node] = []
        if initializer:
            render_nodes = self.render(initializer)
            # Do not append separators for paragraphs.
            if not isinstance(render_nodes[0], nodes.paragraph):
                separator = " "
                assert isinstance(render_nodes[0], nodes.Text)
                if not render_nodes[0].startswith("="):
                    separator += "= "
                signature.append(nodes.Text(separator))
            signature.extend(render_nodes)
        return "".join(n.astext() for n in signature)

    def visit_variable(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        names = self.get_qualification()
        names.append(node.name)
        name = self.join_nested_name(names)
        dom = self.get_domain()
        options = {}
        if dom == "py":
            declaration = name
            initializer = self.make_initializer(node).strip().lstrip("=").strip()
            if len(initializer) != 0:
                options["value"] = initializer
        elif dom == "cs":
            declaration = " ".join([
                self.create_template_prefix(node),
                "".join(n.astext() for n in self.render(node.type)),
                name,
                node.argsstring or "",
            ])
            if node.gettable or node.settable:
                declaration += "{"
                if node.gettable:
                    declaration += "get;"
                if node.settable:
                    declaration += "set;"
                declaration += "}"
            declaration += self.make_initializer(node)
        else:
            elements = [self.create_template_prefix(node)]
            if node.static:
                elements.append("static")
            if node.mutable:
                elements.append("mutable")
            if node.constexpr:
                elements.append("constexpr")
            if node.consteval:
                elements.append("consteval")
            if node.constinit:
                elements.append("constinit")
            typename = strip_legacy_qualifiers("".join(n.astext() for n in self.render(node.type)))
            if dom == "c" and "::" in typename:
                typename = typename.replace("::", ".")
            elements.extend((typename, name, node.argsstring or "", self.make_initializer(node)))
            declaration = " ".join(elements)
        if not dom or dom in ("c", "cpp", "py", "cs"):
            return self.handle_declaration(node, node.kind.value, declaration, options=options)
        else:
            return self.render_declaration(node, declaration)

    def visit_friendclass(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        dom = self.get_domain()
        assert not dom or dom == "cpp"

        desc = addnodes.desc()
        desc["objtype"] = "friendclass"
        desc["domain"] = self.get_domain() or "cpp"
        signode = addnodes.desc_signature()
        desc += signode

        typ = "".join(n.astext() for n in self.render(node.type))
        # in Doxygen < 1.9 the 'friend' part is there, but afterwards not
        # https://github.com/breathe-doc/breathe/issues/616
        assert typ in ("friend class", "friend struct", "class", "struct")
        if not typ.startswith("friend "):
            typ = "friend " + typ
        signode += addnodes.desc_annotation(typ, typ)
        signode += nodes.Text(" ")
        # expr = cpp.CPPExprRole(asCode=False)
        # expr.text = node.name
        # TODO: set most of the things that SphinxRole.__call__ sets
        # signode.extend(expr.run())
        signode += nodes.Text(node.name)
        return [desc]

    def visit_templateparam(
        self, node: parser.Node_paramType, *, insertDeclNameByParsing: bool = False
    ) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = []

        # Parameter type
        if node.type:
            type_nodes = self.render(node.type)
            # Render keywords as annotations for consistency with the cpp domain.
            if len(type_nodes) > 0 and isinstance(type_nodes[0], str):
                first_node = type_nodes[0]
                for keyword in ["typename", "class"]:
                    if first_node.startswith(keyword + " "):
                        type_nodes[0] = nodes.Text(first_node.replace(keyword, "", 1))
                        type_nodes.insert(0, addnodes.desc_annotation(keyword, keyword))
                        break
            nodelist.extend(type_nodes)

        # Parameter name
        if node.declname:
            dom = self.get_domain()
            if not dom:
                dom = "cpp"
            appendDeclName = True
            if insertDeclNameByParsing:
                if dom == "cpp":
                    parser = cpp.DefinitionParser(
                        "".join(n.astext() for n in nodelist),
                        location=self.state.state_machine.get_source_and_line(),
                        config=self.app.config,
                    )
                    try:
                        # we really should use _parse_template_parameter()
                        # but setting a name there is non-trivial, so we use type
                        ast = parser._parse_type(named="single", outer="templateParam")
                        assert ast.name is None
                        nn = cpp.ASTNestedName(
                            names=[
                                cpp.ASTNestedNameElement(cpp.ASTIdentifier(node.declname), None)
                            ],
                            templates=[False],
                            rooted=False,
                        )
                        ast.name = nn
                        # the actual nodes don't matter, as it is astext()-ed later
                        nodelist = [nodes.Text(str(ast))]
                        appendDeclName = False
                    except cpp.DefinitionError:
                        # happens with "typename ...Args", so for now, just append
                        pass

            if appendDeclName:
                if nodelist:
                    nodelist.append(nodes.Text(" "))
                nodelist.append(nodes.emphasis(text=node.declname))
        elif self.output_defname and node.defname:
            # We only want to output the definition name (from the cpp file) if the declaration name
            # (from header file) isn't present
            if nodelist:
                nodelist.append(nodes.Text(" "))
            nodelist.append(nodes.emphasis(text=node.defname))

        # array information
        if node.array:
            nodelist.append(nodes.Text(node.array))

        # Default value
        if node.defval:
            nodelist.append(nodes.Text(" = "))
            nodelist.extend(self.render(node.defval))

        return nodelist

    @node_handler(parser.Node_templateparamlistType)
    def visit_templateparamlist(self, node: parser.Node_templateparamlistType) -> list[nodes.Node]:
        nodelist: list[nodes.Node] = []
        self.output_defname = False
        for i, item in enumerate(node.param):
            if i:
                nodelist.append(nodes.Text(", "))
            nodelist.extend(self.visit_templateparam(item, insertDeclNameByParsing=True))
        self.output_defname = True
        return nodelist

    @node_handler(parser.Node_docParamListType)
    def visit_docparamlist(self, node: parser.Node_docParamListType) -> list[nodes.Node]:
        """Parameter/Exception/TemplateParameter documentation"""

        fieldListName = {
            parser.DoxParamListKind.param: "param",
            parser.DoxParamListKind.exception: "throws",
            parser.DoxParamListKind.templateparam: "tparam",
            parser.DoxParamListKind.retval: "retval",
        }

        # https://docutils.sourceforge.io/docs/ref/doctree.html#field-list
        fieldList = nodes.field_list()
        for item in node:
            # TODO: does item.parameternamelist really have more than 1 parametername?
            assert len(item.parameternamelist) <= 1, item.parameternamelist
            nameNodes: list[nodes.Node] = []
            parameterDirectionNodes = []
            if len(item.parameternamelist) != 0:
                paramNameNodes = item.parameternamelist[0].parametername
                if len(paramNameNodes) != 0:
                    nameNodes = []
                    for paramName in paramNameNodes:
                        assert len(paramName) == 1
                        thisName = self.render_tagged(paramName[0])
                        if len(nameNodes) != 0:
                            if node.kind == parser.DoxParamListKind.exception:
                                msg = "Doxygen \\exception commands with multiple names can not be"
                                msg += " converted to a single :throws: field in Sphinx."
                                msg += " Exception '{}' suppressed from output.".format(
                                    "".join(n.astext() for n in thisName)
                                )
                                self.state.document.reporter.warning(msg)
                                continue
                            nameNodes.append(nodes.Text(", "))
                        nameNodes.extend(thisName)
                        if paramName.direction is not None:
                            # note, each paramName node seems to have the same direction,
                            # so just use the last one
                            dir = {
                                parser.DoxParamDir.in_: "[in]",
                                parser.DoxParamDir.out: "[out]",
                                parser.DoxParamDir.inout: "[inout]",
                            }[paramName.direction]
                            parameterDirectionNodes = [nodes.strong(dir, dir), nodes.Text(" ")]
            # it seems that Sphinx expects the name to be a single node,
            # so let's make it that
            txt = fieldListName[node.kind] + " "
            for n in nameNodes:
                txt += n.astext()
            name = nodes.field_name("", nodes.Text(txt))
            bodyNodes = self.render_optional(item.parameterdescription)
            # TODO: is it correct that bodyNodes is either empty or a single paragraph?
            assert len(bodyNodes) <= 1, bodyNodes
            if len(bodyNodes) == 1:
                assert isinstance(bodyNodes[0], nodes.paragraph)
                bodyNodes = [
                    nodes.paragraph("", "", *(parameterDirectionNodes + bodyNodes[0].children))
                ]
            body = nodes.field_body("", *bodyNodes)
            field = nodes.field("", name, body)
            fieldList += field
        return [fieldList]

    @node_handler(parser.Node_docDotMscType)
    def visit_docdot(self, node: parser.Node_docDotMscType) -> list[nodes.Node]:
        """Translate node from doxygen's dot command to sphinx's graphviz directive."""
        graph_node = graphviz()
        str_value = ""
        if len(node):
            val = node[0]
            assert isinstance(val, str)
            str_value = val
        if str_value.rstrip("\n"):
            graph_node["code"] = str_value
        else:
            graph_node["code"] = ""  # triggers another warning from sphinx.ext.graphviz
            self.state.document.reporter.warning(
                # would be better if this output includes the parent node's
                # name/reference, but that would always be a <para> element.
                "no content provided for generating DOT graph."
            )
        graph_node["options"] = {}
        if node.caption:
            caption_node = nodes.caption(node.caption, "")
            caption_node += nodes.Text(node.caption)
            return [nodes.figure("", graph_node, caption_node)]
        return [graph_node]

    @node_handler(parser.Node_docImageFileType)
    def visit_docdotfile(self, node: parser.Node_docImageFileType) -> list[nodes.Node]:
        """Translate node from doxygen's dotfile command to sphinx's graphviz directive."""
        dotcode = ""
        dot_file_path = Path(node.name or "")
        # Doxygen v1.9.3+ uses a relative path to specify the dot file.
        # Previously, Doxygen used an absolute path.
        # This relative path is with respect to the XML_OUTPUT path.
        # Furthermore, Doxygen v1.9.3+ will copy the dot file into the XML_OUTPUT
        if not dot_file_path.is_absolute():
            # Use self.project_info.project_path as the XML_OUTPUT path, and
            # make it absolute with consideration to the conf.py path
            project_path = self.project_info.project_path()
            dot_file_path = Path(self.app.confdir, project_path, dot_file_path).resolve()
        try:
            dotcode = dot_file_path.read_text(encoding="utf-8")
            if not dotcode.rstrip("\n"):
                raise RuntimeError("%s found but without any content" % dot_file_path)
        except OSError as exc:
            # doxygen seems to prevent this from triggering as a non-existent file
            # generates no XML output for the corresponding `\dotfile` cmd
            self.state.document.reporter.warning(exc)  # better safe than sorry
        except RuntimeError as exc:
            self.state.document.reporter.warning(exc)
        graph_node = graphviz()
        graph_node["code"] = dotcode
        graph_node["options"] = {"docname": dot_file_path}
        caption = "" if len(node) == 0 else parser.tag_name_value(node[0])[1]
        if caption:
            assert isinstance(caption, str)
            caption_node = nodes.caption(caption, "")
            caption_node += nodes.Text(caption)
            return [nodes.figure("", graph_node, caption_node)]
        return [graph_node]

    @tagged_node_handler(parser.Node_graphType)
    def visit_docgraph(self, tag: str, node: parser.Node_graphType) -> list[nodes.Node]:
        """Create a graph (generated by doxygen - not user-defined) from XML using dot
        syntax."""

        assert self.context
        parent = self.context.node_stack[1].value
        assert isinstance(parent, parser.Node_compounddefType)

        direction = "forward"
        if tag == "incdepgraph":
            caption = f"Include dependency graph for {parent.compoundname}:"
        elif tag == "invincdepgraph":
            direction = "back"
            caption = (
                "This graph shows which files directly or indirectly "
                + f"include {parent.compoundname}:"
            )
        elif tag == "inheritancegraph":
            caption = f"Inheritance diagram for {parent.compoundname}:"
        else:
            assert tag == "collaborationgraph"
            caption = f"Collaboration diagram for {parent.compoundname}:"

        # use graphs' legend from doxygen (v1.9.1)
        # most colors can be changed via `graphviz_dot_args` in conf.py
        edge_colors = {
            # blue (#1414CE) doesn't contrast well in dark mode.
            # "public-inheritance": "1414CE",  # allow user to customize this one
            "private-inheritance": "8B1A1A",  # hardcoded
            "protected-inheritance": "006400",  # hardcoded
            # the following are demonstrated in the doxygen graphs' legend, but
            # these don't show in XML properly (bug?); these keys are fiction.
            "used-internal": "9C35CE",  # should also be dashed
            "template-instantiated-inheritance": "FFA500",  # should also be dashed
        }

        # assemble the dot syntax we'll pass to the graphviz directive
        dot = "digraph {\n"
        dot += '    graph [bgcolor="#00000000"]\n'  # transparent color for graph's bg
        dot += '    node [shape=rectangle style=filled fillcolor="#FFFFFF"'
        dot += " font=Helvetica padding=2]\n"
        dot += '    edge [color="#1414CE"]\n'
        relations = []
        for g_node in node.node:
            dot += '    "%s" [label="%s"' % (g_node.id, g_node.label)
            dot += ' tooltip="%s"' % g_node.label
            if g_node.id == "1":
                # the disabled grey color is used in doxygen to indicate that the URL is
                # not set (for the compound in focus). Setting this here doesn't allow
                # further customization. Maybe remove this since URL is not used?
                #
                dot += ' fillcolor="#BFBFBF"'  # hardcoded
            # URLs from a doxygen refid won't work in sphinx graphviz; we can't convert
            # the refid until all docs are built, and pending references are un-noticed
            # within graphviz directives. Maybe someone wiser will find a way to do it.
            #
            # dot += ' URL="%s"' % g_node.get_link().get_refid()
            dot += "]\n"
            for child_node in g_node.childnode:
                edge = f'    "{g_node.id}"'
                edge += f' -> "{child_node.refid}" ['
                edge += f"dir={direction} "
                # edge labels don't appear in XML (bug?); use tooltip in meantime
                edge += 'tooltip="%s"' % child_node.relation.value
                if child_node.relation.value in edge_colors.keys():
                    edge += ' color="#%s"' % edge_colors.get(child_node.relation.value)
                edge += "]\n"
                relations.append(edge)
        for relation in relations:
            dot += relation
        dot += "}"

        # use generated dot syntax to create a graphviz node
        graph_node = graphviz()
        graph_node["code"] = dot
        graph_node["align"] = "center"
        graph_node["options"] = {}
        # if caption is first node in a figure, then everything that follows is
        # considered a caption. Use a paragraph followed by a figure to center the
        # graph. This may have illegible side effects for very large graphs.
        caption_node = nodes.paragraph("", nodes.Text(caption))
        return [caption_node, nodes.figure("", graph_node)]

    def visit_unknown(self, node) -> list[nodes.Node]:
        """Visit a node of unknown type."""
        return []

    @node_handler(parser.Node_CompoundType)
    def dispatch_compound(self, node: parser.Node_CompoundType) -> list[nodes.Node]:
        """Dispatch handling of a compound node to a suitable visit method."""
        if node.kind in [
            parser.CompoundKind.file,
            parser.CompoundKind.dir,
            parser.CompoundKind.page,
            parser.CompoundKind.example,
            parser.CompoundKind.group,
        ]:
            return self.visit_file(node)
        return self.visit_compound(node)

    @node_handler(parser.Node_memberdefType)
    def dispatch_memberdef(self, node: parser.Node_memberdefType) -> list[nodes.Node]:
        """Dispatch handling of a memberdef node to a suitable visit method."""
        if node.kind in (
            parser.DoxMemberKind.function,
            parser.DoxMemberKind.signal,
            parser.DoxMemberKind.slot,
        ) or (node.kind == parser.DoxMemberKind.friend and node.argsstring):
            return self.visit_function(node)
        if node.kind == parser.DoxMemberKind.enum:
            return self.visit_enum(node)
        if node.kind == parser.DoxMemberKind.typedef:
            return self.visit_typedef(node)
        if node.kind == parser.DoxMemberKind.variable:
            return self.visit_variable(node)
        if node.kind == parser.DoxMemberKind.property:
            # Note: visit like variable for now
            return self.visit_variable(node)
        if node.kind == parser.DoxMemberKind.event:
            # Note: visit like variable for now
            return self.visit_variable(node)
        if node.kind == parser.DoxMemberKind.define:
            return self.visit_define(node)
        if node.kind == parser.DoxMemberKind.friend:
            # note, friend functions should be dispatched further up
            return self.visit_friendclass(node)
        return self.render_declaration(node, update_signature=self.update_signature)

    @tagged_node_handler(str)
    def visit_string(self, tag: str, node: str) -> list[nodes.Node]:
        if tag == "verbatim":
            return self.visit_verbatim(node)
        return self.render_string(node)

    @node_handler(str)
    def render_string(self, node: str) -> list[nodes.Node]:
        # Skip any nodes that are pure whitespace
        # Probably need a better way to do this as currently we're only doing
        # it skip whitespace between higher-level nodes, but this will also
        # skip any pure whitespace entries in actual content nodes
        #
        # We counter that second issue slightly by allowing through single white spaces
        #
        stripped = node.strip()
        if stripped:
            delimiter = None
            if "<linebreak>" in stripped:
                delimiter = "<linebreak>"
            elif "\n" in stripped:
                delimiter = "\n"
            if delimiter:
                # Render lines as paragraphs because RST doesn't have line breaks.
                return [
                    nodes.paragraph("", "", nodes.Text(line.strip()))
                    for line in node.split(delimiter)
                    if line.strip()
                ]
            # importantly, don't strip whitespace as visit_docpara uses it to collapse
            # consecutive nodes.Text and rerender them with this function.
            return [nodes.Text(node)]
        if node == " ":
            return [nodes.Text(node)]
        return []

    def render_tagged(
        self, item: parser.TaggedValue[str, parser.NodeOrValue] | str
    ) -> list[nodes.Node]:
        if isinstance(item, str):
            return self.render_string(item)
        return self.render(item.value, None, item.name)

    def render(
        self, node: parser.NodeOrValue, context: RenderContext | None = None, tag: str | None = None
    ) -> list[nodes.Node]:
        if context is None:
            assert self.context is not None
            context = self.context.create_child_context(node, tag)
        with WithContext(self, context):
            assert self.context is not None
            result: list[nodes.Node] = []
            if self.filter_(NodeStack(self.context.node_stack)):
                tmethod = self.tagged_node_handlers.get(type(node))
                if tmethod is None:
                    method = self.node_handlers.get(type(node))
                    if method is None:
                        method = SphinxRenderer.visit_unknown
                    result = method(self, node)
                elif tag is None:
                    assert isinstance(node, str)
                    result = self.render_string(node)
                else:
                    result = tmethod(self, tag, node)
        return result

    def render_optional(self, node, tag: str | None = None) -> list[nodes.Node]:
        """Render a node that can be None."""
        return self.render(node, None, tag) if node is not None else []


def setup(app: Sphinx) -> None:
    app.add_config_value("breathe_debug_trace_directives", False, "")
    app.add_config_value("breathe_debug_trace_doxygen_ids", False, "")
    app.add_config_value("breathe_debug_trace_qualification", False, "")
