
from breathe.directive.base import BaseDirective, BaseHandler
from breathe.nodes import DoxygenNode, DoxygenAutoNode

from docutils.parsers.rst.directives import unchanged_required, unchanged, flag
from docutils.transforms import Transform
from docutils import nodes


class IndexHandler(BaseHandler):
    """
    Replaces a DoxygenNode with the rendered contents of the doxygen xml's index.xml file

    This used to be carried out in the doxygenindex directive implementation but we have this level
    of indirection to support the autodoxygenindex directive and share the code.
    """

    def render(self):

        try:
            finder = self.factories.finder_factory.create_finder(self.project_info)
        except ParserError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno, True)
        except FileIOError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        data_object = finder.root()

        target_handler = self.factories.target_handler_factory.create_target_handler(self.options, self.project_info, self.state.document)
        filter_ = self.factories.filter_factory.create_index_filter(self.options)

        renderer_factory_creator = self.factories.renderer_factory_creator_constructor.create_factory_creator(
                self.project_info,
                self.state.document,
                self.options,
                target_handler
                )
        renderer_factory = renderer_factory_creator.create_factory(
                data_object,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )
        object_renderer = renderer_factory.create_renderer(self.factories.root_data_object, data_object)

        try:
            node_list = object_renderer.render()
        except ParserError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno, True)
        except FileIOError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        return node_list


class DoxygenIndexDirective(BaseDirective):

    required_arguments = 0
    optional_arguments = 2
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenindex: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        handler = IndexHandler(
                "doxygenindex",
                None,               # No data required for doxygenindex
                project_info,
                self.options,
                self.state,
                self.lineno,
                self
                )

        return [DoxygenNode(handler)]


class AutoDoxygenIndexDirective(BaseDirective):

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
            "source-path": unchanged_required,
            "source": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        files = self.arguments[0].split()

        try:
            project_info = self.project_info_factory.create_auto_project_info(self.options)
        except ProjectError, e:
            warning = 'autodoxygenindex: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        node = DoxygenAutoNode(
            "autodoxygenindex",
            None,                   # No data required for doxygenindex
            project_info,
            files,
            self.options,
            self,
            self.state,
            self.lineno
            )

        return [node]


