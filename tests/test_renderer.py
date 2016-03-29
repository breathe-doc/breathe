# Renderer tests

import sphinx.environment
from breathe.renderer.compound import FuncMemberDefTypeSubRenderer
from docutils import frontend, nodes, parsers, utils
from sphinx.domains import CPPDomain
from distutils.version import LooseVersion


sphinx.locale.init([], None)


class MockDoxygenNode:
    def __init__(self, **kwargs):
        attributes = {
            'id': None,
            'kind': None,
            'name': '',
            'definition': '',
            'param': [],
            'virt': None,
            'const': None,
            'volatile': None,
            'argsstring': '',
            'briefdescription': None,
            'detaileddescription': None,
            'templateparamlist': None
        }
        for name, value in attributes.items():
            setattr(self, name, kwargs.get(name, value))


class MockState:
    def __init__(self):
        env = sphinx.environment.BuildEnvironment(None, None, None)
        CPPDomain(env)
        env.temp_data['docname'] = None
        settings = frontend.OptionParser(
            components=(parsers.rst.Parser,)).get_default_values()
        settings.env = env
        self.document = utils.new_document('', settings)

    def nested_parse(self, content, content_offset, contentnode):
        pass


class MockReporter:
    def __init__(self):
        pass

    def warning(self, description, line):
        pass

    def debug(self, message):
        pass


class MockStateMachine:
    def __init__(self):
        self.reporter = MockReporter()


class MockContext:
    def __init__(self, node_stack):
        self.domain = None
        self.node_stack = node_stack
        self.directive_args = [
            None,  # name
            None,  # arguments
            [],    # options
            None,  # content
            None,  # lineno
            None,  # content_offset
            None,  # block_text
            MockState(), MockStateMachine()]
        self.child = None

    def create_child_context(self, attribute):
        return self


class MockProjectInfo:
    def __init__(self):
        pass

    def name(self):
        pass


class MockTargetHandler:
    def __init__(self):
        pass

    def create_target(self, refid):
        pass


class MockNodeFactory:
    def __init__(self):
        pass

    def Text(self, data):
        pass


class MockDocument:
    def __init__(self):
        self.reporter = MockReporter()


class NodeFinder(nodes.NodeVisitor):
    """Find node with specified class name."""
    def __init__(self, name, document):
        nodes.NodeVisitor.__init__(self, document)
        self.name = name
        self.found_nodes = []

    def unknown_visit(self, node):
        if node.__class__.__name__ == self.name:
            self.found_nodes.append(node)


def find_nodes(nodes, name):
    """Find all docutils nodes with specified class name in *nodes*."""
    finder = NodeFinder(name, MockDocument())
    for node in nodes:
        node.walk(finder)
    return finder.found_nodes


def find_node(nodes, name):
    """
    Find a single docutils node with specified class name in *nodes*.
    Throw an exception if there isn't exactly one such node.
    """
    found_nodes = find_nodes(nodes, name)
    if len(found_nodes) != 1:
        raise Exception('the number of nodes {0} is {1}'.format(name, len(found_nodes)))
    return found_nodes[0]


def test_find_nodes():
    section = nodes.section()
    foo = nodes.Text('foo')
    desc = nodes.description()
    bar = nodes.Text('bar')
    section.children = [foo, desc, bar]
    assert(find_nodes(section, 'description') == [desc])
    assert(find_nodes([section, desc], 'description') == [desc, desc])
    assert(find_nodes([], 'description') == [])
    assert(find_nodes(section, 'unknown') == [])
    assert(find_nodes(section, 'Text') == [foo, bar])


def check_exception(func, message):
    """Check if func() throws an exception with the specified message."""
    exception = None
    try:
        func()
    except Exception as e:
        exception = e
    print(str(exception))
    assert exception and str(exception) == message


def test_find_node():
    section = nodes.section()
    foo = nodes.Text('foo')
    desc = nodes.description()
    bar = nodes.Text('bar')
    section.children = [foo, desc, bar]
    assert(find_node(section, 'description') == desc)
    check_exception(lambda: find_node([section, desc], 'description'),
                    'the number of nodes description is 2')
    check_exception(lambda: find_node([], 'description'),
                    'the number of nodes description is 0')
    check_exception(lambda: find_node([section], 'unknown'),
                    'the number of nodes unknown is 0')
    check_exception(lambda: find_node([section], 'Text'),
                    'the number of nodes Text is 2')


def test_func_renderer():
    doxy_node = MockDoxygenNode(definition='void f', argsstring='()')
    renderer = FuncMemberDefTypeSubRenderer(MockProjectInfo(), MockContext([doxy_node]),
                                            None,  # renderer_factory
                                            MockNodeFactory(),
                                            None,  # state
                                            None,  # document
                                            MockTargetHandler())
    nodes = renderer.render()
    node = find_node(nodes, 'desc_name')
    if LooseVersion(sphinx.__version__) >= LooseVersion('1.3'):
        assert node[0] == 'f'
