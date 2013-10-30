
from docutils.transforms import Transform
from docutils import nodes

from breathe.nodes import DoxygenNode
from breathe.parser import ParserError

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



class DoxygenTransform(Transform):

    default_priority = 210

    def apply(self):

        for node in self.document.traverse(DoxygenNode):
            handler = node.handler
            handler.handle(node)


