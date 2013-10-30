
from docutils import nodes

class DoxygenNode(nodes.Element):

    def __init__(self, handler):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.handler = handler

class DoxygenAutoNode(nodes.Element):

    def __init__(self, project_info, files, options, factories, state):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.project_info = project_info
        self.files = files
        self.options = options
        self.factories = factories
        self.state = state

