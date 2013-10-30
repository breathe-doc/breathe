
from docutils.transforms import Transform
from docutils import nodes

from breathe.parser import ParserError
from breathe.nodes import DoxygenNode, DoxygenAutoNode

import subprocess
import os

class TransformHandler(object):

    def __init__(self, name, project_info, options, state, factories):

        self.name = name
        self.project_info = project_info
        self.options = options
        self.state = state
        self.factories = factories

class IndexHandler(TransformHandler):

    def handle(self, node):

        try:
            finder = self.factories.finder_factory.create_finder(self.project_info)
        except ParserError, e:
            warning = 'autodoxygenindex: Unable to parse file "%s"' % e
            return [nodes.warning("", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        data_object = finder.root()

        target_handler = self.factories.target_handler_factory.create(self.options, self.project_info, self.state.document)
        filter_ = self.factories.filter_factory.create_index_filter(self.options)

        renderer_factory_creator = self.factories.renderer_factory_creator_constructor.create_factory_creator(
                self.project_info,
                self.state.document,
                self.options,
                )
        renderer_factory = renderer_factory_creator.create_factory(
                data_object,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )
        object_renderer = renderer_factory.create_renderer(self.factories.root_data_object, data_object)
        node_list = object_renderer.render()

        # Replaces "node" in document with the contents of node_list
        node.replace_self(node_list)

AUTOCFG_TEMPLATE = r"""PROJECT_NAME     = "{project_name}"
OUTPUT_DIRECTORY = {output_dir}
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
INPUT            = {input}
ENABLE_PREPROCESSING = YES
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
ALIASES = "rst=\verbatim embed:rst"
ALIASES += "endrst=\endverbatim"
"""

class ProjectData(object):

    def __init__(self, project_info, files):

        self.project_info = project_info
        self.files = files

class DoxygenAutoTransform(Transform):
    """
    Iterate over all the DoxygenAutoNodes and:

    - Collect the information from them regarding what files need to be processed by doxygen and in
      what projects
    - Process those files with doxygen
    - Replace the nodes with DoxygenNodes which can be picked up by the standard rendering mechanism
    """

    default_priority = 209

    def apply(self):

        project_files = {}

        for node in self.document.traverse(DoxygenAutoNode):
            try:
                project_files[node.project_info.name()].files.extend(node.files)
            except KeyError:
                project_files[node.project_info.name()] = ProjectData(node.project_info, node.files)

        for project_name, data in project_files.items():

            dir_ = "build/breathe/doxygen"

            cfgfile = "%s.cfg" % project_name
            cfg = AUTOCFG_TEMPLATE.format(
                    project_name=project_name,
                    output_dir=project_name,
                    input=" ".join(map(lambda x: data.project_info.abs_path_to_source_file(x), data.files))
                    )

            if not os.path.exists(dir_):
                os.makedirs(dir_)

            with open(os.path.join(dir_, cfgfile), 'w') as f:
                f.write(cfg)

            subprocess.check_call(['doxygen', cfgfile], cwd=dir_)

            # TODO: Should be a factory creation
            data.project_info.set_project_path(os.path.join(os.path.abspath(dir_), project_name, "xml"))

        for node in self.document.traverse(DoxygenAutoNode):

            handler = IndexHandler(
                    "",
                    node.project_info,
                    node.options,
                    node.state,
                    node.factories
                    )

            standard_index_node = DoxygenNode(handler)

            node.replace_self(standard_index_node)

class DoxygenTransform(Transform):

    default_priority = 210

    def apply(self):

        for node in self.document.traverse(DoxygenNode):
            handler = node.handler
            handler.handle(node)

