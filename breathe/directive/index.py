
from breathe.directive.base import BaseDirective
from breathe.nodes import DoxygenNode

from docutils.parsers.rst.directives import unchanged_required, unchanged, flag
from docutils.transforms import Transform
from docutils import nodes


class DoxygenAutoIndexNode(nodes.Element):

    def __init__(self, auto_project_info, files, options, factories, state, lineno):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.auto_project_info = auto_project_info
        self.files = files
        self.options = options
        self.factories = factories
        self.state = state
        self.lineno = lineno

class IndexHandler(object):
    """
    Replaces a DoxygenNode with the rendered contents of the doxygen xml's index.xml file

    This used to be carried out in the doxygenindex directive implementation but we have this level
    of indirection to support the autodoxygenindex directive and share the code.
    """

    def __init__(self, name, project_info, options, state, lineno, factories):

        self.name = name
        self.project_info = project_info
        self.options = options
        self.state = state
        self.lineno = lineno
        self.factories = factories

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


class ProjectData(object):
    "Simple handler for the files and project_info for each project"

    def __init__(self, auto_project_info, files):

        self.auto_project_info = auto_project_info
        self.files = files


class DoxygenAutoIndexTransform(Transform):

    default_priority = 209

    def __init__(self, doxygen_handle, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        self.doxygen_handle = doxygen_handle

    def apply(self):
        """
        Iterate over all the DoxygenAutoIndexNodes and:

        - Collect the information from them regarding what files need to be processed by doxygen and
          in what projects
        - Process those files with doxygen
        - Replace the nodes with DoxygenNodes which can be picked up by the standard rendering
          mechanism
        """

        project_files = {}

        # First collect together all the files which need to be doxygen processed for each project
        for node in self.document.traverse(DoxygenAutoIndexNode):
            try:
                project_files[node.auto_project_info.name()].files.extend(node.files)
            except KeyError:
                project_files[node.auto_project_info.name()] = ProjectData(node.auto_project_info, node.files)

        per_project_project_info = {}
        
        # Iterate over the projects and generate doxygen xml output for the files for each one into
        # a directory in the Sphinx build area 
        for project_name, data in project_files.items():

            project_path = self.doxygen_handle.process(data.auto_project_info, data.files) 

            project_info = data.auto_project_info.create_project_info(project_path)
            per_project_project_info[data.auto_project_info.name()] = project_info

        # Replace each DoxygenAutoIndexNode in the document with a properly prepared DoxygenNode which
        # can then be processed by the DoxygenTransform just as if it had come from a standard
        # doxygenindex directive
        for node in self.document.traverse(DoxygenAutoIndexNode):

            handler = IndexHandler(
                    "autodoxygenindex",
                    per_project_project_info[node.auto_project_info.name()],
                    node.options,
                    node.state,
                    node.lineno,
                    node.factories
                    )

            standard_index_node = DoxygenNode(handler)

            node.replace_self(standard_index_node)


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

        return [DoxygenAutoIndexNode(project_info, files, self.options, self, self.state, self.lineno)]


