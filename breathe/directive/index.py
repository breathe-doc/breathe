
from ..renderer.base import RenderContext
from ..renderer.mask import NullMaskFactory
from ..renderer import format_parser_error, DoxygenToRstRendererFactory
from ..directive.base import BaseDirective
from ..project import ProjectError
from ..parser import ParserError, FileIOError
from .base import create_warning

from docutils.parsers.rst.directives import unchanged_required, flag


class RootDataObject(object):

    node_type = "root"


class BaseIndexDirective(BaseDirective):
    """Base class handle the main work when given the appropriate project info to work from.
    """

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, project_info):

        try:
            finder = self.finder_factory.create_finder(project_info)
        except ParserError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state,
                                       self.lineno, True)
        except FileIOError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        data_object = finder.root()

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_index_filter(self.options)

        renderer_factory = DoxygenToRstRendererFactory(
            self.parser_factory,
            project_info
            )
        object_renderer = renderer_factory.create_renderer(
            [data_object],
            self.state,
            self.state.document,
            filter_,
            target_handler,
            )

        mask_factory = NullMaskFactory()
        context = RenderContext([data_object, RootDataObject()], mask_factory,
                                self.directive_args)

        try:
            node_list = object_renderer.render(context.node_stack[0], context)
        except ParserError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state,
                                       self.lineno, True)
        except FileIOError as e:
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
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenindex: %s' % e)

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
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('autodoxygenindex: %s' % e)

        return self.handle_contents(project_info)
