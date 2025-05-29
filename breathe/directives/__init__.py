from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.directives import SphinxDirective

from breathe import parser
from breathe.finder import factory
from breathe.renderer import RenderContext, format_parser_error
from breathe.renderer.sphinxrenderer import SphinxRenderer

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from sphinx.application import Sphinx

    from breathe.parser import DoxygenParser
    from breathe.project import ProjectInfo, ProjectInfoFactory
    from breathe.renderer import TaggedNode
    from breathe.renderer.filter import DoxFilter
    from breathe.renderer.mask import MaskFactoryBase
    from breathe.renderer.target import TargetHandler


class _WarningHandler:
    def __init__(self, state, context: dict[str, Any]) -> None:
        self.state = state
        self.context = context

    def warn(
        self,
        raw_text: str,
        *,
        rendered_nodes: Sequence[nodes.Node] | None = None,
        unformatted_suffix: str = "",
    ) -> list[nodes.Node]:
        raw_text = self.format(raw_text) + unformatted_suffix
        if rendered_nodes is None:
            rendered_nodes = [nodes.paragraph("", "", nodes.Text(raw_text))]
        return [
            nodes.warning("", *rendered_nodes),
            self.state.document.reporter.warning(raw_text, line=self.context["lineno"]),
        ]

    def format(self, text: str) -> str:
        return text.format(**self.context)


class BaseDirective(SphinxDirective):
    @property
    def directive_args(self) -> list:
        # the order must be the same as in docutils.parsers.rst.Directive.__init__
        return [
            self.name,
            self.arguments,
            self.options,
            self.content,
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine,
        ]

    @property
    def project_info_factory(self) -> ProjectInfoFactory:
        return self.env.temp_data["breathe_project_info_factory"]

    @property
    def dox_parser(self) -> DoxygenParser:
        return self.env.temp_data["breathe_dox_parser"]

    @property
    def app(self) -> Sphinx:
        return self.env.app

    def get_doxygen_index(self, project_info: ProjectInfo) -> parser.DoxygenIndex:
        return self.dox_parser.parse_index(project_info)

    def create_finder_from_root(
        self, root: factory.FinderRoot, project_info: ProjectInfo
    ) -> factory.Finder:
        return factory.create_finder_from_root(self.env.app, self.dox_parser, root, project_info)

    def create_warning(self, project_info: ProjectInfo | None, **kwargs) -> _WarningHandler:
        if project_info:
            proj_name = project_info.name()
            proj_path = project_info.project_path()
            tail = f'in doxygen xml output for project "{proj_name}" from directory: {proj_path}'
        else:
            tail = ""

        context = dict(lineno=self.lineno, tail=tail, **kwargs)
        return _WarningHandler(self.state, context)

    def render(
        self,
        node_stack: list[TaggedNode],
        project_info: ProjectInfo,
        filter_: DoxFilter,
        target_handler: TargetHandler,
        mask_factory: MaskFactoryBase,
        directive_args,
    ) -> list[nodes.Node]:
        "Standard render process used by subclasses"

        try:
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
        except parser.ParserError as e:
            return format_parser_error(
                "doxygenclass", e.message, e.filename, self.state, self.lineno, True
            )
        except parser.FileIOError as e:
            return format_parser_error(
                "doxygenclass", e.error, e.filename, self.state, self.lineno, True
            )

        context = RenderContext(node_stack, mask_factory, directive_args)
        node = node_stack[0].value
        assert isinstance(node, parser.Node)
        return object_renderer.render(node, context)
