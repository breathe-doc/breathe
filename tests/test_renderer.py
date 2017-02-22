# Renderer tests

import sphinx.environment
from breathe.node_factory import create_node_factory
from breathe.parser.compound import linkedTextTypeSub, memberdefTypeSub, paramTypeSub, MixedContainer
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.filter import OpenFilter
from docutils import frontend, nodes, parsers, utils
from sphinx.domains.cpp import CPPDomain
from sphinx.domains.c import CDomain

from nose.tools import eq_


sphinx.locale.init([], None)


class TestDoxygenNode:
    """
    A base class for test wrappers of Doxygen nodes. It allows setting all attributes via keyword arguments
    in the constructor.
    """
    def __init__(self, cls, **kwargs):
        if cls:
            cls.__init__(self)
        for name, value in kwargs.items():
            if not hasattr(self, name):
                raise AttributeError('invalid attribute ' + name)
            setattr(self, name, value)


class TestMixedContainer(MixedContainer, TestDoxygenNode):
    """A test wrapper of Doxygen mixed container."""
    def __init__(self, **kwargs):
        MixedContainer.__init__(self, None, None, None, None)
        TestDoxygenNode.__init__(self, None, **kwargs)


class TestLinkedText(linkedTextTypeSub, TestDoxygenNode):
    """A test wrapper of Doxygen linked text."""
    def __init__(self, **kwargs):
        TestDoxygenNode.__init__(self, linkedTextTypeSub, **kwargs)


class TestMemberDef(memberdefTypeSub, TestDoxygenNode):
    """A test wrapper of Doxygen class/file/namespace member symbol such as a function declaration."""
    def __init__(self, **kwargs):
        TestDoxygenNode.__init__(self, memberdefTypeSub, **kwargs)


class TestParam(paramTypeSub, TestDoxygenNode):
    """A test wrapper of Doxygen parameter."""
    def __init__(self, **kwargs):
        TestDoxygenNode.__init__(self, paramTypeSub, **kwargs)

class MockConfig(object):
    cpp_id_attributes = []
    cpp_paren_attributes = []
    cpp_index_common_prefix = []


class MockState:
    def __init__(self):
        env = sphinx.environment.BuildEnvironment(None, None, MockConfig())
        CPPDomain(env)
        CDomain(env)
        env.temp_data['docname'] = 'mock-doc'
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


class MockMaskFactory:
    def __init__(self):
        pass

    def mask(self, node):
        return node


class MockContext:
    def __init__(self, node_stack, domain=None):
        self.domain = domain
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
        self.mask_factory = MockMaskFactory()

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


def render(member_def, domain=None):
    """Render Doxygen *member_def* with *renderer_class*."""
    renderer = SphinxRenderer(MockProjectInfo(),
                              None,  # renderer_factory
                              create_node_factory(),
                              None,  # state
                              None,  # document
                              MockTargetHandler(),
                              None,   # compound_parser
                              OpenFilter())
    renderer.context = MockContext([member_def], domain)
    return renderer.render(member_def)


def test_render_func():
    member_def = TestMemberDef(kind='function', definition='void foo', argsstring='(int)', virt='non-virtual',
                               param=[TestParam(type_=TestLinkedText(content_=[TestMixedContainer(value=u'int')]))])
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext().startswith('void')
    assert find_node(signature, 'desc_name')[0] == 'foo'
    params = find_node(signature, 'desc_parameterlist')
    assert len(params) == 1
    param = params[0]
    assert param[0] == 'int'


def test_render_typedef():
    member_def = TestMemberDef(kind='typedef', definition='typedef int foo')
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext() == 'typedef int foo'


def test_render_c_typedef():
    member_def = TestMemberDef(kind='typedef', definition='typedef unsigned int bar')
    signature = find_node(render(member_def, domain='c'), 'desc_signature')
    eq_(signature.astext(), 'typedef unsigned int bar')


def test_render_c_function_typedef():
    member_def = TestMemberDef(kind='typedef', definition='typedef void* (*voidFuncPtr)(float, int)')
    signature = find_node(render(member_def, domain='c'), 'desc_signature')
    assert signature.astext().startswith('typedef void*')
    params = find_node(signature, 'desc_parameterlist')
    assert len(params) == 2
    eq_(params[0].astext(), "float")
    eq_(params[1].astext(), "int")


def test_render_using_alias():
    member_def = TestMemberDef(kind='typedef', definition='using foo = int')
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext() == 'using foo = int'


def test_render_const_func():
    member_def = TestMemberDef(kind='function', definition='void f', argsstring='() const',
                               virt='non-virtual', const='yes')
    signature = find_node(render(member_def), 'desc_signature')
    assert '_CPPv2NK1fEv' in signature['ids']

def test_render_variable_initializer():
    member_def = TestMemberDef(kind='variable', definition='const int EOF', initializer=TestMixedContainer(value=u'= -1'))
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext() == 'const int EOF = -1'

def test_render_define_initializer():
    member_def = TestMemberDef(kind='define', name='MAX_LENGTH', initializer=TestLinkedText(content_=[TestMixedContainer(value=u'100')]))
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext() == 'MAX_LENGTH 100'

def test_render_define_no_initializer():
    member_def = TestMemberDef(kind='define', name='USE_MILK')
    signature = find_node(render(member_def), 'desc_signature')
    assert signature.astext() == 'USE_MILK'
