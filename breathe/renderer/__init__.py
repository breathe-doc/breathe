
import textwrap

from ..node_factory import create_node_factory
from .base import Renderer
from . import index as indexrenderer
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
            renderers,
            renderer_factory_creator,
            project_info,
            state,
            document,
            filter_,
            target_handler,
            ):

        self.node_type = node_type
        self.project_info = project_info
        self.renderers = renderers
        self.renderer_factory_creator = renderer_factory_creator
        self.state = state
        self.document = document
        self.filter_ = filter_
        self.target_handler = target_handler
        self.renderer = compoundrenderer.SphinxRenderer(
            self.project_info,
            self,
            create_node_factory(),
            self.state,
            self.document,
            self.target_handler
        )

    def create_renderer(self, context):
        renderer = self.do_create_renderer(context)
        renderer.set_context(context)
        return renderer

    def do_create_renderer(
            self,
            context
            ):

        data_object = context.node_stack[0]

        if not self.filter_.allow(context.node_stack):
            return NullRenderer()

        child_renderer_factory = self.renderer_factory_creator.create_child_factory(
            self.project_info,
            data_object,
            self
        )

        try:
            node_type = data_object.node_type
        except AttributeError as e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                node_type = "unicode"
            else:
                raise e

        Renderer = self.renderers[node_type]

        node_factory = create_node_factory()

        common_args = [
            self.project_info,
            child_renderer_factory,
            node_factory,
            self.state,
            self.document,
            self.target_handler,
        ]

        if node_type == "compound":

            kind = data_object.kind
            if kind in ["file", "dir", "page", "example", "group"]:
                return Renderer(indexrenderer.FileRenderer, *common_args)

            class_ = indexrenderer.CompoundTypeSubRenderer

            # For compound node types Renderer is CreateCompoundTypeSubRenderer
            # as defined below. This could be cleaner
            return Renderer(
                class_,
                *common_args
            )

        if node_type == "memberdef":
            return self.renderer

        return Renderer(
            *common_args
        )


class CreateCompoundTypeSubRenderer(object):

    def __init__(self, parser_factory):

        self.parser_factory = parser_factory

    def __call__(self, class_, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return class_(compound_parser, project_info, *args)


class CreateRefTypeSubRenderer(object):

    def __init__(self, parser_factory):

        self.parser_factory = parser_factory

    def __call__(self, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return compoundrenderer.RefTypeSubRenderer(compound_parser, project_info, *args)


class DoxygenToRstRendererFactoryCreator(object):

    def __init__(
            self,
            parser_factory,
            project_info
            ):

        self.parser_factory = parser_factory
        self.project_info = project_info

    def create_factory(self, node_stack, state, document, filter_, target_handler):

        renderers = {
            "doxygen": compoundrenderer.SphinxRenderer,
            "compound": CreateCompoundTypeSubRenderer(self.parser_factory),
            "doxygendef": compoundrenderer.SphinxRenderer,
            "compounddef": compoundrenderer.SphinxRenderer,
            "sectiondef": compoundrenderer.SphinxRenderer,
            "memberdef": compoundrenderer.SphinxRenderer,
            "enumvalue": compoundrenderer.SphinxRenderer,
            "linkedtext": compoundrenderer.SphinxRenderer,
            "description": compoundrenderer.SphinxRenderer,
            "param": compoundrenderer.SphinxRenderer,
            "docreftext": compoundrenderer.SphinxRenderer,
            "docheading": compoundrenderer.SphinxRenderer,
            "docpara": compoundrenderer.SphinxRenderer,
            "docmarkup": compoundrenderer.SphinxRenderer,
            "docparamlist": compoundrenderer.SphinxRenderer,
            "docparamlistitem": compoundrenderer.SphinxRenderer,
            "docparamnamelist": compoundrenderer.SphinxRenderer,
            "docparamname": compoundrenderer.SphinxRenderer,
            "docsect1": compoundrenderer.SphinxRenderer,
            "docsimplesect": compoundrenderer.SphinxRenderer,
            "doctitle": compoundrenderer.SphinxRenderer,
            "docformula": compoundrenderer.SphinxRenderer,
            "docimage": compoundrenderer.SphinxRenderer,
            "docurllink": compoundrenderer.SphinxRenderer,
            "listing": compoundrenderer.SphinxRenderer,
            "codeline": compoundrenderer.SphinxRenderer,
            "highlight": compoundrenderer.SphinxRenderer,
            "templateparamlist": compoundrenderer.SphinxRenderer,
            "inc": compoundrenderer.SphinxRenderer,
            "ref": CreateRefTypeSubRenderer(self.parser_factory),
            "compoundref": compoundrenderer.SphinxRenderer,
            "verbatim": compoundrenderer.SphinxRenderer,
            "mixedcontainer": compoundrenderer.SphinxRenderer,
            "unicode": compoundrenderer.SphinxRenderer,
            "doclist": compoundrenderer.SphinxRenderer,
            "doclistitem": compoundrenderer.SphinxRenderer,
            }

        return DoxygenToRstRendererFactory(
            "root",
            renderers,
            self,
            self.project_info,
            state,
            document,
            filter_,
            target_handler,
        )

    def create_child_factory(self, project_info, data_object, parent_renderer_factory):

        try:
            node_type = data_object.node_type
        except AttributeError as e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                node_type = "unicode"
            else:
                raise e

        return DoxygenToRstRendererFactory(
            node_type,
            parent_renderer_factory.renderers,
            self,
            parent_renderer_factory.project_info,
            parent_renderer_factory.state,
            parent_renderer_factory.document,
            parent_renderer_factory.filter_,
            parent_renderer_factory.target_handler,
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
