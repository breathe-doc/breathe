
from breathe.nodes import DoxygenNode, DoxygenAutoNode

from docutils.transforms import Transform


class DoxygenTransform(Transform):

    default_priority = 210

    def apply(self):
        """Iterate over all DoxygenNodes in the document and extract their handlers
        to replace them.
        """

        for node in self.document.traverse(DoxygenNode):
            handler = node.handler

            # Replaces "node" in document with the renderer contents
            node.replace_self(handler.render())


class ProjectData(object):
    "Simple handler for the files and project_info for each project"

    def __init__(self, auto_project_info, files):

        self.auto_project_info = auto_project_info
        self.files = files

class DoxygenAutoTransform(Transform):

    default_priority = 209

    def __init__(self, doxygen_handle, node_handler_factory, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        self.doxygen_handle = doxygen_handle
        self.node_handler_factory = node_handler_factory

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
        # directive
        for node in self.document.traverse(DoxygenAutoNode):

            handler = self.node_handler_factory.create(
                    node.kind,
                    node.data,
                    per_project_project_info[node.auto_project_info.name()],
                    node.options,
                    node.state,
                    node.lineno,
                    node.factories
                    )

            standard_index_node = DoxygenNode(handler)

            node.replace_self(standard_index_node)


class TransformWrapper(object):

    def __init__(self, transform, doxygen_handle, node_handler_factory):

        self.transform = transform
        self.doxygen_handle = doxygen_handle
        self.node_handler_factory = node_handler_factory

        # Set up default_priority so sphinx/docutils can read it from this instance
        self.default_priority = transform.default_priority

    def __call__(self, *args, **kwargs):

        return self.transform(self.doxygen_handle, self.node_handler_factory, *args, **kwargs)

