from breathe.directives import BaseDirective
from breathe.parser import ParserError, FileIOError
from breathe.project import ProjectError
from breathe.renderer import format_parser_error, RenderContext
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler

from docutils.nodes import Node
from docutils.parsers.rst.directives import unchanged_required, flag

from typing import List


class RootDataObject:
    node_type = "root"


class _BaseIndexDirective(BaseDirective):
    """Base class handle the main work when given the appropriate project info to work from."""

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, project_info):
        try:
            finder = self.finder_factory.create_finder(project_info)
        except ParserError as e:
            return format_parser_error(
                self.name, e.error, e.filename, self.state, self.lineno, True
            )
        except FileIOError as e:
            return format_parser_error(self.name, e.error, e.filename, self.state, self.lineno)

        data_object = finder.root()

        target_handler = create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_index_filter(self.options)

        object_renderer = SphinxRenderer(
            self.parser_factory.app,
            project_info,
            [data_object],
            self.state,
            self.state.document,
            target_handler,
            self.parser_factory.create_compound_parser(project_info),
            filter_,
        )

        mask_factory = NullMaskFactory()
        context = RenderContext([data_object, RootDataObject()], mask_factory, self.directive_args)

        try:
            node_list = object_renderer.render(context.node_stack[0], context)
        except ParserError as e:
            return format_parser_error(
                self.name, e.error, e.filename, self.state, self.lineno, True
            )
        except FileIOError as e:
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

    def run(self) -> List[Node]:
        """Extract the project info from the auto project info store and pass it to the helper
        method.
        """

        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("autodoxygenindex: %s" % e)

        return self.handle_contents(project_info)
