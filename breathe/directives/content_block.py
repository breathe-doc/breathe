from __future__ import annotations

from breathe.directives import BaseDirective
from breathe.file_state_cache import MTimeError
from breathe.project import ProjectError
from breathe.renderer import RenderContext
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler
from breathe import parser

from docutils.nodes import Node
from docutils.parsers.rst.directives import unchanged_required, flag

from typing import cast, ClassVar, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import NotRequired, TypedDict
    else:
        from typing_extensions import NotRequired, TypedDict
    from breathe.renderer import TaggedNode
    from breathe.finder.factory import FinderRoot

    DoxContentBlockOptions = TypedDict(
        "DoxContentBlockOptions",
        {
            "path": str,
            "project": str,
            "content-only": NotRequired[None],
            "members": NotRequired[str],
            "protected-members": NotRequired[None],
            "private-members": NotRequired[None],
            "undoc-members": NotRequired[None],
            "show": str,
            "outline": NotRequired[None],
            "no-link": NotRequired[None],
            "desc-only": NotRequired[None],
            "sort": NotRequired[None],
        },
    )
else:
    DoxContentBlockOptions = None
    FinderRoot = None


class _DoxygenContentBlockDirective(BaseDirective):
    """Base class for namespace and group directives which have very similar behaviours"""

    kind: ClassVar[Literal["group", "page", "namespace"]]

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "content-only": flag,
        "outline": flag,
        "members": flag,
        "protected-members": flag,
        "private-members": flag,
        "undoc-members": flag,
        "no-link": flag,
        "desc-only": flag,
        "sort": flag,
    }
    has_content = False

    def run(self) -> list[Node]:
        name = self.arguments[0]
        options = cast(DoxContentBlockOptions, self.options)

        try:
            project_info = self.project_info_factory.create_project_info(options)
        except ProjectError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimeError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        finder_filter = self.filter_factory.create_finder_filter(self.kind, name)

        matches: list[list[TaggedNode]] = []
        finder.filter_(finder_filter, matches)

        # It shouldn't be possible to have too many matches as namespaces & groups in their nature
        # are merged together if there are multiple declarations, so we only check for no matches
        if not matches:
            warning = self.create_warning(project_info, name=name, kind=self.kind)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{name}" {tail}')

        if "content-only" in options and self.kind != "page":
            # Unpack the single entry in the matches list
            (node_stack,) = matches

            filter_ = self.filter_factory.create_content_filter(self.kind, options)
            # Having found the compound node for the namespace or group in the index we want to grab
            # the contents of it which match the filter
            contents_finder = self.finder_factory.create_finder_from_root(
                cast(FinderRoot, node_stack[0].value), project_info
            )

            contents: list[list[TaggedNode]] = []
            contents_finder.filter_(filter_, contents)

            # Replaces matches with our new starting points
            matches = contents

        target_handler = create_target_handler(options, project_info, self.state.document)
        filter_ = self.filter_factory.create_render_filter(self.kind, options)

        node_list: list[Node] = []
        for node_stack in matches:
            object_renderer = SphinxRenderer(
                self.parser_factory.app,
                project_info,
                [item.value for item in node_stack],
                self.state,
                self.state.document,
                target_handler,
                self.parser_factory.create_compound_parser(project_info),
                filter_,
            )

            mask_factory = NullMaskFactory()
            context = RenderContext(node_stack, mask_factory, self.directive_args)
            value = context.node_stack[0].value
            assert isinstance(value, parser.Node)
            node_list.extend(object_renderer.render(value, context))

        return node_list


class DoxygenNamespaceDirective(_DoxygenContentBlockDirective):
    kind = "namespace"


class DoxygenGroupDirective(_DoxygenContentBlockDirective):
    kind = "group"
    option_spec = _DoxygenContentBlockDirective.option_spec.copy()
    option_spec.update({"inner": flag})


class DoxygenPageDirective(_DoxygenContentBlockDirective):
    kind = "page"
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "content-only": flag,
    }
