
from breathe.renderer.rst.doxygen import format_parser_error
from breathe.directive.base import BaseDirective
from breathe.project import ProjectError
from breathe.parser import ParserError, FileIOError

from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes


class BaseIndexDirective(BaseDirective):
    """Base class handle the main work when given the appropriate project info to work from.
    """

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, project_info):

        try:
            finder = self.finder_factory.create_finder(project_info)
        except ParserError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state,
                                       self.lineno, True)
        except FileIOError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        data_object = finder.root()

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_index_filter(self.options)

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
            project_info,
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
        object_renderer = renderer_factory.create_renderer(self.root_data_object, data_object)

        try:
            node_list = object_renderer.render()
        except ParserError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state,
                                       self.lineno, True)
        except FileIOError, e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        return node_list


class DoxygenIndexDirective(BaseIndexDirective):

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
        """Extract the project info and pass it to the helper method"""

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenindex: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        return self.handle_contents(project_info)


class AutoDoxygenIndexDirective(BaseIndexDirective):

    required_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):
        """Extract the project info from the auto project info store and pass it to the helper
        method
        """

        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError, e:
            warning = 'autodoxygenindex: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        return self.handle_contents(project_info)


