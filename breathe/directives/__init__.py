from breathe.finder.factory import FinderFactory
from breathe.parser import DoxygenParserFactory
from breathe.parser import FileIOError, ParserError
from breathe.project import ProjectInfoFactory, ProjectInfo
from breathe.renderer import format_parser_error, RenderContext
from breathe.renderer.filter import Filter, FilterFactory
from breathe.renderer.mask import MaskFactoryBase
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import TargetHandler

from sphinx.directives import SphinxDirective

from docutils import nodes

from typing import Any, Dict, List, Optional, Sequence


class _WarningHandler:
    def __init__(self, state, context: Dict[str, Any]) -> None:
        self.state = state
        self.context = context

    def warn(
        self,
        raw_text: str,
        *,
        rendered_nodes: Sequence[nodes.Node] = None,
        unformatted_suffix: str = ""
    ) -> List[nodes.Node]:
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
    def parser_factory(self) -> DoxygenParserFactory:
        return self.env.temp_data["breathe_parser_factory"]

    @property
    def finder_factory(self) -> FinderFactory:
        return FinderFactory(self.env.app, self.parser_factory)

    @property
    def filter_factory(self) -> FilterFactory:
        return FilterFactory(self.env.app)

    @property
    def kind(self) -> str:
        raise NotImplementedError

    def create_warning(self, project_info: Optional[ProjectInfo], **kwargs) -> _WarningHandler:
        if project_info:
            tail = 'in doxygen xml output for project "{project}" from directory: {path}'.format(
                project=project_info.name(), path=project_info.project_path()
            )
        else:
            tail = ""

        context = dict(lineno=self.lineno, tail=tail, **kwargs)
        return _WarningHandler(self.state, context)

    def render(
        self,
        node_stack,
        project_info: ProjectInfo,
        filter_: Filter,
        target_handler: TargetHandler,
        mask_factory: MaskFactoryBase,
        directive_args,
    ) -> List[nodes.Node]:
        "Standard render process used by subclasses"

        try:
            object_renderer = SphinxRenderer(
                self.parser_factory.app,
                project_info,
                node_stack,
                self.state,
                self.state.document,
                target_handler,
                self.parser_factory.create_compound_parser(project_info),
                filter_,
            )
        except ParserError as e:
            return format_parser_error(
                "doxygenclass", e.error, e.filename, self.state, self.lineno, True
            )
        except FileIOError as e:
            return format_parser_error(
                "doxygenclass", e.error, e.filename, self.state, self.lineno, True
            )

        context = RenderContext(node_stack, mask_factory, directive_args)
        return object_renderer.render(node_stack[0], context)
