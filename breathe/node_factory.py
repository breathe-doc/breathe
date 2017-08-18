
import docutils.nodes
import collections
import sphinx.addnodes
import sphinx.ext.mathbase

from .exception import BreatheError


class NodeNotFoundError(BreatheError):
    pass


class NodeFactory(object):

    def __init__(self, source_file, *args):

        self.sources = args
        self.source_file = source_file

    def __getattr__(self, node_name):

        for source in self.sources:
            try:
                attr = getattr(source, node_name)
                if issubclass(attr, docutils.nodes.Node):
                    ret = globals().get(attr.__name__)

                    if ret is not None:
                        return ret

                    def __init__(s, *args, **kwargs):

                        attr.__init__(s, *args, **kwargs)
                        if s.source is None:
                            s.source = self.source_file

                    ret = type(attr.__name__, (attr,), {"__init__": __init__})
                    globals()[attr.__name__] = ret

                    return ret

                return attr
            except AttributeError:
                pass

        raise NodeNotFoundError(node_name)


def create_node_factory(source_file=None):

    # Create a math_nodes object with a displaymath member for the displaymath
    # node so that we can treat it in the same way as the nodes & addnodes
    # modules in the NodeFactory
    math_nodes = collections.namedtuple("MathNodes", ["displaymath"])
    math_nodes.displaymath = sphinx.ext.mathbase.displaymath
    return NodeFactory(source_file, docutils.nodes, sphinx.addnodes, math_nodes)
