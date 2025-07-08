from __future__ import annotations

from typing import TYPE_CHECKING

from docutils.parsers.rst.directives import flag, unchanged_required

from breathe import parser
from breathe.directives import BaseDirective
from breathe.project import ProjectError
from breathe.renderer import RenderContext, TaggedNode, filter, format_parser_error
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from docutils.nodes import Node


class RootDataObject:
    pass


def create_index_filter(options: Mapping[str, Any]) -> filter.DoxFilter:
    outline_filter = filter.create_outline_filter(options)

    def filter_(nstack: filter.NodeStack) -> bool:
        if not outline_filter(nstack):
            return False

        node = nstack.node
        parent = nstack.parent
        return not (
            isinstance(parent, parser.Node_compounddefType)
            and (
                (
                    isinstance(node, parser.Node_refType)
                    and nstack.tag in ("innerclass", "innernamespace")
                )
                or (
                    parent.kind == parser.DoxCompoundKind.group
                    and isinstance(node, parser.Node_sectiondefType)
                    and node.kind == parser.DoxSectionKind.func
                )
            )
        )

    return filter_


class _BaseIndexDirective(BaseDirective):
    """Base class handle the main work when given the appropriate project info to work from."""

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, project_info) -> list[Node]:
        try:
            d_index = self.get_doxygen_index(project_info)
        except parser.ParserError as e:
            return format_parser_error(
                self.name, e.message, e.filename, self.state, self.lineno, True
            )
        except parser.FileIOError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        target_handler = create_target_handler(self.options, self.env)
        filter_ = create_index_filter(self.options)

        object_renderer = SphinxRenderer(
            self.dox_parser.app,
            project_info,
            [d_index.root],
            self.state,
            self.state.document,
            target_handler,
            self.dox_parser,
            filter_,
        )

        mask_factory = NullMaskFactory()
        context = RenderContext(
            [TaggedNode(None, d_index.root), TaggedNode(None, RootDataObject())],
            mask_factory,
            self.directive_args,
        )

        value = context.node_stack[0].value
        assert isinstance(value, parser.Node)
        try:
            node_list = object_renderer.render(value, context)
        except parser.ParserError as e:
            return format_parser_error(
                self.name, e.message, e.filename, self.state, self.lineno, True
            )
        except parser.FileIOError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        return node_list


class DoxygenIndexDirective(_BaseIndexDirective):
    required_arguments = 0
    optional_arguments = 2
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
    }
    has_content = False

    def run(self):
        """Extract the project info and pass it to the helper method"""

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("doxygenindex: %s" % e)

        return self.handle_contents(project_info)


class AutoDoxygenIndexDirective(_BaseIndexDirective):
    required_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
    }
    has_content = False

    def run(self) -> list[Node]:
        """Extract the project info from the auto project info store and pass it to the helper
        method.
        """

        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("autodoxygenindex: %s" % e)

        return self.handle_contents(project_info)
