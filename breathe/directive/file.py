
from breathe.directive.base import BaseDirective
from breathe.project import ProjectError

from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes


class BaseFileDirective(BaseDirective):
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
            warning = (
                'doxygenfile: Found multiple matches for file "%s" in doxygen xml output for '
                'project "%s" from directory: %s' % (
                    file_, project_info.name(), project_info.project_path()
                    )
                )
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        elif not matches:
            warning = (
                'doxygenfile: Cannot find file "%s" in doxygen xml output for project "%s" from '
                'directory: %s' % (file_, project_info.name(), project_info.project_path())
                )
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_file_filter(file_, self.options)

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
            project_info,
            self.state.document,
            self.options,
            target_handler
            )
        node_list = []
        for data_object in matches:

            renderer_factory = renderer_factory_creator.create_factory(
                data_object,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )

            object_renderer = renderer_factory.create_renderer(self.root_data_object, data_object)
            node_list.extend(object_renderer.render())

        return node_list


class DoxygenFileDirective(BaseFileDirective):

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
        """Get the file from the argument and the project info from the factory."""

        file_ = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenfile: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        return self.handle_contents(file_, project_info)


class AutoDoxygenFileDirective(BaseFileDirective):

    required_arguments = 1
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):
        """Get the file from the argument and extract the associated project info for the named
        project given that it is an auto-project.
        """

        file_ = self.arguments[0]

        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError, e:
            warning = 'autodoxygenfile: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        return self.handle_contents(file_, project_info)
