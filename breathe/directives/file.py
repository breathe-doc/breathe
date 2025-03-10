from __future__ import annotations

from docutils.parsers.rst.directives import flag, unchanged_required

from breathe.directives import BaseDirective
from breathe.project import ProjectError
from breathe.renderer import RenderContext
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler


class _BaseFileDirective(BaseDirective):
    """Base class handle the main work when given the appropriate file and project info to work
    from.
    """

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, file_, project_info):
        finder = self.finder_factory.create_finder(project_info)
        finder_filter = self.filter_factory.create_file_finder_filter(file_)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) > 1:
            warning = self.create_warning(None, file=file_, directivename=self.directive_name)
            return warning.warn('{directivename}: Found multiple matches for file "{file} {tail}')
        elif not matches:
            warning = self.create_warning(None, file=file_, directivename=self.directive_name)
            return warning.warn('{directivename}: Cannot find file "{file} {tail}')

        target_handler = create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_file_filter(file_, self.options)

        node_list = []
        for node_stack in matches:
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

            mask_factory = NullMaskFactory()
            context = RenderContext(node_stack, mask_factory, self.directive_args)
            node_list.extend(object_renderer.render(node_stack[0], context))

        return node_list


class DoxygenFileDirective(_BaseFileDirective):
    directive_name = "doxygenfile"

    required_arguments = 0
    optional_arguments = 3
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
        "sections": unchanged_required,
    }
    has_content = False

    def run(self):
        """Get the file from the argument and the project info from the factory."""

        file_ = self.arguments[0]
        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("doxygenfile: %s" % e)

        return self.handle_contents(file_, project_info)


class AutoDoxygenFileDirective(_BaseFileDirective):
    directive_name = "autodoxygenfile"

    required_arguments = 1
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
        "sections": unchanged_required,
    }
    has_content = False

    def run(self):
        """Get the file from the argument and extract the associated project info for the named
        project given that it is an auto-project.
        """

        file_ = self.arguments[0]
        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("autodoxygenfile: %s" % e)

        return self.handle_contents(file_, project_info)
