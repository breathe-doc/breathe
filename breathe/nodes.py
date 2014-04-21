
from docutils import nodes

class DoxygenNode(nodes.Element):

    def __init__(self, handler):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.handler = handler

class DoxygenAutoNode(nodes.Element):

    def __init__(self, auto_project_info, files, options, factories, state, lineno):

        nodes.Element.__init__(self, rawsource='', children=[], attributes={})

        self.auto_project_info = auto_project_info
        self.files = files
        self.options = options
        self.factories = factories
        self.state = state
        self.lineno = lineno

