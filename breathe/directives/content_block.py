from __future__ import annotations

from typing import TYPE_CHECKING, cast

from docutils.parsers.rst.directives import flag, unchanged_required

from breathe import parser
from breathe.directives import BaseDirective
from breathe.file_state_cache import MTimeError
from breathe.project import ProjectError
from breathe.renderer import RenderContext, filter
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler

if TYPE_CHECKING:
    import sys
    from typing import ClassVar, Literal

    if sys.version_info >= (3, 11):
        from typing import NotRequired, TypedDict
    else:
        from typing_extensions import NotRequired, TypedDict

    from docutils.nodes import Node
    from sphinx.application import Sphinx

    from breathe.finder.factory import FinderRoot
    from breathe.project import ProjectOptions

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
    ProjectOptions = None
    FinderRoot = None


def create_render_filter(
    app: Sphinx, kind: Literal["group", "page", "namespace"], options: DoxContentBlockOptions
) -> filter.DoxFilter:
    """Render filter for group & namespace blocks"""

    filter_options = filter.set_defaults(app, options)

    if "desc-only" in filter_options:
        return filter.create_description_filter(True, parser.Node_compounddefType)

    cm_filter = filter.create_class_member_filter(filter_options)
    ic_filter = filter.create_innerclass_filter(filter_options)
    o_filter = filter.create_outline_filter(filter_options)

    def filter_(nstack: filter.NodeStack) -> bool:
        grandparent = nstack.ancestor(2)
        return (
            (
                cm_filter(nstack)
                or (
                    isinstance(grandparent, parser.Node_compounddefType)
                    and grandparent.kind not in filter.CLASS_LIKE_COMPOUNDDEF
                    and isinstance(nstack.node, parser.Node_memberdefType)
                )
            )
            and ic_filter(nstack)
            and o_filter(nstack)
        )

    return filter_


def create_content_filter(kind: Literal["group", "page", "namespace"]) -> filter.DoxFilter:
    """Returns a filter which matches the contents of the or namespace but not the group or
    namepace name or description.

    This allows the groups to be used to structure sections of the documentation rather than to
    structure and further document groups of documentation

    As a finder/content filter we only need to match exactly what we're interested in.
    """

    def filter_(nstack: filter.NodeStack) -> bool:
        node = nstack.node
        parent = nstack.parent

        if isinstance(node, parser.Node_memberdefType):
            return node.prot == parser.DoxProtectionKind.public

        return (
            isinstance(node, parser.Node_refType)
            and isinstance(parent, parser.Node_compounddefType)
            and parent.kind.value == kind
            and nstack.tag == "innerclass"
            and node.prot == parser.DoxProtectionKind.public
        )

    return filter_


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
        options = cast("DoxContentBlockOptions", self.options)

        try:
            project_info = self.project_info_factory.create_project_info(
                cast("ProjectOptions", options)
            )
        except ProjectError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        try:
            d_index = self.get_doxygen_index(project_info)
        except MTimeError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        matches: list[filter.FinderMatch] = list(
            filter.compound_finder_filter(name, self.kind, d_index)
        )

        # It shouldn't be possible to have too many matches as namespaces & groups in their nature
        # are merged together if there are multiple declarations, so we only check for no matches
        if not matches:
            warning = self.create_warning(project_info, name=name, kind=self.kind)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{name}" {tail}')

        if "content-only" in options and self.kind != "page":
            # Unpack the single entry in the matches list
            (node_stack,) = matches

            filter_ = create_content_filter(self.kind)
            # Having found the compound node for the namespace or group in the index we want to grab
            # the contents of it which match the filter
            contents_finder = self.create_finder_from_root(
                cast("FinderRoot", node_stack[0].value), project_info
            )

            contents: list[filter.FinderMatch] = []
            contents_finder.filter_(filter_, contents)

            # Replaces matches with our new starting points
            matches = contents

        target_handler = create_target_handler(options, self.env)
        filter_ = create_render_filter(self.app, self.kind, options)

        node_list: list[Node] = []
        for node_stack in matches:
            object_renderer = SphinxRenderer(
                self.dox_parser.app,
                project_info,
                [item.value for item in node_stack],
                self.state,
                self.state.document,
                target_handler,
                self.dox_parser,
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
    option_spec.update({
        "inner": flag,
        "no-title": flag,
    })


class DoxygenPageDirective(_DoxygenContentBlockDirective):
    kind = "page"
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "content-only": flag,
        "no-title": flag,
    }
