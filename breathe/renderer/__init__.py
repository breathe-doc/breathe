
import textwrap

from ..node_factory import create_node_factory
from .base import Renderer
from . import compound as compoundrenderer

from docutils import nodes


class NullRenderer(Renderer):

    def __init__(self):
        pass

    def render(self, node):
        return []


class DoxygenToRstRendererFactory(object):

    def __init__(
            self,
            node_type,
            renderer_factory_creator,
            project_info,
            state,
            document,
            filter_,
            target_handler,
            compound_parser
            ):

        self.filter_ = filter_
        self.renderer = compoundrenderer.SphinxRenderer(
            project_info,
            self,
            create_node_factory(),
            state,
            document,
            target_handler,
            compound_parser
        )

    def create_renderer(self, context):

        if not self.filter_.allow(context.node_stack):
            return NullRenderer()

        self.renderer.set_context(context)
        return self.renderer


class DoxygenToRstRendererFactoryCreator(object):

    def __init__(
            self,
            parser_factory,
            project_info
            ):

        self.parser_factory = parser_factory
        self.project_info = project_info

    def create_factory(self, node_stack, state, document, filter_, target_handler):

        return DoxygenToRstRendererFactory(
            "root",
            self,
            self.project_info,
            state,
            document,
            filter_,
            target_handler,
            self.parser_factory.create_compound_parser(self.project_info)
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
