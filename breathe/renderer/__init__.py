from . import sphinxrenderer

from breathe.parser import DoxygenParserFactory
from breathe.project import ProjectInfo
from breathe.renderer.filter import Filter
from breathe.renderer.target import TargetHandler

from docutils import nodes

import textwrap


class DoxygenToRstRendererFactory:
    def __init__(self, parser_factory: DoxygenParserFactory, project_info: ProjectInfo) -> None:
        self.parser_factory = parser_factory
        self.project_info = project_info

    def create_renderer(self, node_stack, state, document, filter_: Filter,
                        target_handler: TargetHandler) -> sphinxrenderer.SphinxRenderer:
        return sphinxrenderer.SphinxRenderer(
            self.parser_factory.app,
            self.project_info,
            node_stack,
            state,
            document,
            target_handler,
            self.parser_factory.create_compound_parser(self.project_info),
            filter_
        )


def format_parser_error(name, error, filename, state, lineno, do_unicode_warning):
    warning = '%s: Unable to parse xml file "%s". ' % (name, filename)
    explanation = 'Reported error: %s. ' % error

    unicode_explanation_text = ""
    unicode_explanation = []
    if do_unicode_warning:
        unicode_explanation_text = textwrap.dedent("""
        Parsing errors are often due to unicode errors associated with the encoding of the original
        source files. Doxygen propagates invalid characters from the input source files to the
        output xml.""").strip().replace("\n", " ")
        unicode_explanation = [nodes.paragraph("", "", nodes.Text(unicode_explanation_text))]

    return [
        nodes.warning(
            "",
            nodes.paragraph("", "", nodes.Text(warning)),
            nodes.paragraph("", "", nodes.Text(explanation)),
            *unicode_explanation
        ),
        state.document.reporter.warning(
            warning + explanation + unicode_explanation_text, line=lineno)
    ]
