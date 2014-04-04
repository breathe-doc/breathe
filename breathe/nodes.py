
from docutils import nodes


class DoxygenNode(nodes.Element):

    def __init__(self, handler):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.handler = handler

