
from breathe.directive.base import BaseDirective, BaseNodeHandler
from breathe.project import ProjectError
from breathe.nodes import DoxygenNode, DoxygenAutoNode

from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes

class FileNodeHandler(BaseNodeHandler):
    """
    Replaces a DoxygenNode with the rendered contents of the doxygen xml's index.xml file

    This used to be carried out in the doxygenindex directive implementation but we have this level
    of indirection to support the autodoxygenindex directive and share the code.
    """

    def render(self):

        file_ = self.data

        finder = self.factories.finder_factory.create_finder(self.project_info)

        finder_filter = self.factories.filter_factory.create_file_finder_filter(file_)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) > 1:
            warning = ('doxygenfile: Found multiple matches for file "%s" in doxygen xml output for project "%s" '
                    'from directory: %s' % (file_, self.project_info.name(), self.project_info.project_path()))
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        elif not matches:
            warning = ('doxygenfile: Cannot find file "%s" in doxygen xml output for project "%s" from directory: %s'
                    % (file_, self.project_info.name(), self.project_info.project_path()))
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.factories.target_handler_factory.create_target_handler(self.options,
                self.project_info, self.state.document)
        filter_ = self.factories.filter_factory.create_file_filter(file_, self.options)

        renderer_factory_creator = self.factories.renderer_factory_creator_constructor.create_factory_creator(
                self.project_info,
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

            object_renderer = renderer_factory.create_renderer(self.factories.root_data_object, data_object)
            node_list.extend(object_renderer.render())

        return node_list


class ProjectData(object):
    "Simple handler for the files and project_info for each project"

    def __init__(self, auto_project_info, files):

        self.auto_project_info = auto_project_info
        self.files = files


class DoxygenFileDirective(BaseDirective):

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

        file_ = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenfile: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        handler = FileNodeHandler(
                "doxygenfile",
                file_,
                project_info,
                self.options,
                self.state,
                self.lineno,
                self
                )

        return [DoxygenNode(handler)]


class AutoDoxygenFileDirective(BaseDirective):

    required_arguments = 1
    option_spec = {
            "source-path": unchanged_required,
            "source": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        file_ = self.arguments[0]
        files = [file_]

        try:
            project_info = self.project_info_factory.create_auto_project_info(self.options)
        except ProjectError, e:
            warning = 'autodoxygenfile: %s' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        node = DoxygenAutoNode(
            "autodoxygenfile",
            file_,          # So that the FileHandler code get the filename
            project_info,
            files,          # So that the DoxygenAutoTransform knows to included that file
            self.options,
            self,
            self.state,
            self.lineno
            )

        return [node]

