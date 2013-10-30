
from docutils.transforms import Transform
from docutils import nodes

from breathe.nodes import DoxygenNode

class DoxygenTransform(Transform):

    default_priority = 210

    def apply(self):

        for node in self.document.traverse(DoxygenNode):
            handler = node.handler
            handler.handle(node)


