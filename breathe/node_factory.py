
import docutils.nodes
import collections
import sphinx.addnodes
import sphinx.ext.mathbase

from .exception import BreatheError


class NodeNotFoundError(BreatheError):
    pass


class NodeFactory(object):

    def __init__(self, *args):

        self.sources = args

    def __getattr__(self, node_name):

        for source in self.sources:
            try:
                return getattr(source, node_name)
            except AttributeError:
                pass

        raise NodeNotFoundError(node_name)


def create_node_factory():

    # Create a math_nodes object with a displaymath member for the displaymath
    # node so that we can treat it in the same way as the nodes & addnodes
    # modules in the NodeFactory
    math_nodes = collections.namedtuple("MathNodes", ["displaymath"])
    math_nodes.displaymath = sphinx.ext.mathbase.displaymath
    return NodeFactory(docutils.nodes, sphinx.addnodes, math_nodes)
