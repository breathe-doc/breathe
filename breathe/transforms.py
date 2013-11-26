
from docutils.transforms import Transform
from docutils import nodes

from breathe.parser import ParserError, FileIOError
from breathe.nodes import DoxygenNode, DoxygenAutoNode
from breathe.renderer.rst.doxygen import format_parser_error

import textwrap

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

class DoxygenAutoTransform(Transform):

    default_priority = 209

    def __init__(self, doxygen_handle, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        self.doxygen_handle = doxygen_handle

    def apply(self):
        """
        Iterate over all the DoxygenAutoNodes and:

        - Collect the information from them regarding what files need to be processed by doxygen and
          in what projects
        - Process those files with doxygen
        - Replace the nodes with DoxygenNodes which can be picked up by the standard rendering
          mechanism
        """

        project_files = {}

        # First collect together all the files which need to be doxygen processed for each project
        for node in self.document.traverse(DoxygenAutoNode):
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

        # Replace each DoxygenAutoNode in the document with a properly prepared DoxygenNode which
        # can then be processed by the DoxygenTransform just as if it had come from a standard
        # doxygenindex directive
        for node in self.document.traverse(DoxygenAutoNode):

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

class DoxygenTransform(Transform):

    default_priority = 210

    def apply(self):
        "Iterate over all DoxygenNodes in the document and extract their handlers to replace them"

        for node in self.document.traverse(DoxygenNode):
            handler = node.handler

            # Replaces "node" in document with the renderer contents
            node.replace_self(handler.render())


class TransformWrapper(object):

    def __init__(self, transform, doxygen_handle):

        self.transform = transform
        self.doxygen_handle = doxygen_handle

        # Set up default_priority so sphinx/docutils can read it from this instance
        self.default_priority = transform.default_priority

    def __call__(self, *args, **kwargs):

        return self.transform(self.doxygen_handle, *args, **kwargs)

