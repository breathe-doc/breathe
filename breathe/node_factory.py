
import docutils.nodes
import sphinx.addnodes

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

    return NodeFactory(docutils.nodes, sphinx.addnodes)
