
from breathe.nodes import DoxygenNode

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


class TransformWrapper(object):

    def __init__(self, transform, doxygen_handle):

        self.transform = transform
        self.doxygen_handle = doxygen_handle

        # Set up default_priority so sphinx/docutils can read it from this instance
        self.default_priority = transform.default_priority

    def __call__(self, *args, **kwargs):

        return self.transform(self.doxygen_handle, *args, **kwargs)

