# Renderer tests

import pytest

import sphinx.addnodes
import sphinx.environment
from breathe.node_factory import create_node_factory
from breathe.parser.compound import linkedTextTypeSub, memberdefTypeSub, paramTypeSub, MixedContainer
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.filter import OpenFilter
from docutils import frontend, nodes, parsers, utils

from sphinx.testing.fixtures import (
    test_params, app_params, make_app, shared_result,
    sphinx_test_tempdir, rootdir
)
from sphinx.testing.path import path

sphinx.locale.init([], None)


@pytest.fixture(scope='function')
def app(test_params, app_params, make_app, shared_result):
    """
    Based on sphinx.testing.fixtures.app
    """
    args, kwargs = app_params
    assert 'srcdir' in kwargs
    kwargs['srcdir'].makedirs(exist_ok=True)
    (kwargs['srcdir'] / 'conf.py').write_text('')
    app_ = make_app(*args, **kwargs)
    yield app_

    print('# testroot:', kwargs.get('testroot', 'root'))
    print('# builder:', app_.builder.name)
    print('# srcdir:', app_.srcdir)
    print('# outdir:', app_.outdir)
    print('# status:', '\n' + app_._status.getvalue())
    print('# warning:', '\n' + app_._warning.getvalue())

    if test_params['shared_result']:
        shared_result.store(test_params['shared_result'], app_)


class WrappedDoxygenNode:
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


class WrappedMixedContainer(MixedContainer, WrappedDoxygenNode):
    """A test wrapper of Doxygen mixed container."""
    def __init__(self, **kwargs):
        MixedContainer.__init__(self, None, None, None, None)
        WrappedDoxygenNode.__init__(self, None, **kwargs)


class WrappedLinkedText(linkedTextTypeSub, WrappedDoxygenNode):
    """A test wrapper of Doxygen linked text."""
    def __init__(self, **kwargs):
        WrappedDoxygenNode.__init__(self, linkedTextTypeSub, **kwargs)


class WrappedMemberDef(memberdefTypeSub, WrappedDoxygenNode):
    """A test wrapper of Doxygen class/file/namespace member symbol such as a function declaration."""
    def __init__(self, **kwargs):
        WrappedDoxygenNode.__init__(self, memberdefTypeSub, **kwargs)


class WrappedParam(paramTypeSub, WrappedDoxygenNode):
    """A test wrapper of Doxygen parameter."""
    def __init__(self, **kwargs):
        WrappedDoxygenNode.__init__(self, paramTypeSub, **kwargs)


class MockState:
    def __init__(self, app):
        env = sphinx.environment.BuildEnvironment(app)
        env.setup(app)
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

    def get_source_and_line(self, lineno: int):
        return 'mock-doc', lineno


class MockMaskFactory:
    def __init__(self):
        pass

    def mask(self, node):
        return node


class MockContext:
    def __init__(self, app, node_stack, domain=None):
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
            MockState(app), MockStateMachine()]
        self.child = None
        self.mask_factory = MockMaskFactory()

    def create_child_context(self, attribute):
        return self


class MockProjectInfo:
    def __init__(self, show_define_initializer=False):
        self._show_define_initializer = show_define_initializer
        pass

    def name(self):
        pass

    def show_define_initializer(self):
        return self._show_define_initializer

    def project_refids(self):
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


def render(app, member_def, domain=None, show_define_initializer=False):
    """Render Doxygen *member_def* with *renderer_class*."""
    renderer = SphinxRenderer(MockProjectInfo(show_define_initializer),
                              None,  # renderer_factory
                              create_node_factory(),
                              [],    # node_stack
                              None,  # state
                              None,  # document
                              MockTargetHandler(),
                              None,   # compound_parser
                              OpenFilter())
    renderer.context = MockContext(app, [member_def], domain)
    return renderer.render(member_def)


def test_render_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void foo', argsstring='(int)', virt='non-virtual',
                               param=[WrappedParam(type_=WrappedLinkedText(content_=[WrappedMixedContainer(value=u'int')]))])
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext().startswith('void')
    assert find_node(signature, 'desc_name')[0] == 'foo'
    params = find_node(signature, 'desc_parameterlist')
    assert len(params) == 1
    param = params[0]
    assert param[0] == 'int'


def test_render_typedef(app):
    member_def = WrappedMemberDef(kind='typedef', definition='typedef int foo')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext() == 'typedef int foo'


def test_render_c_typedef(app):
    member_def = WrappedMemberDef(kind='typedef', definition='typedef unsigned int bar')
    signature = find_node(render(app, member_def, domain='c'), 'desc_signature')
    assert signature.astext() == 'typedef unsigned int bar'


def test_render_c_function_typedef(app):
    member_def = WrappedMemberDef(kind='typedef', definition='typedef void* (*voidFuncPtr)(float, int)')
    signature = find_node(render(app, member_def, domain='c'), 'desc_signature')
    assert signature.astext().startswith('typedef void *')
    params = find_node(signature, 'desc_parameterlist')
    assert len(params) == 2
    assert params[0].astext() == "float"
    assert params[1].astext() == "int"


def test_render_using_alias(app):
    member_def = WrappedMemberDef(kind='typedef', definition='using foo = int')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext() == 'using foo = int'


def test_render_const_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void f', argsstring='() const',
                               virt='non-virtual', const='yes')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert '_CPPv2NK1fEv' in signature['ids']


def test_render_lvalue_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void f', argsstring='()',
                               virt='non-virtual', refqual='lvalue')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext().endswith('&')


def test_render_rvalue_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void f', argsstring='()',
                               virt='non-virtual', refqual='rvalue')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext().endswith('&&')


def test_render_const_lvalue_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void f', argsstring='()',
                               virt='non-virtual', const='yes', refqual='lvalue')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext().endswith('const &')


def test_render_const_rvalue_func(app):
    member_def = WrappedMemberDef(kind='function', definition='void f', argsstring='()',
                               virt='non-virtual', const='yes', refqual='rvalue')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext().endswith('const &&')


def test_render_variable_initializer(app):
    member_def = WrappedMemberDef(kind='variable', definition='const int EOF', initializer=WrappedMixedContainer(value=u'= -1'))
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext() == 'const int EOF = -1'


def test_render_define_initializer(app):
    member_def = WrappedMemberDef(kind='define', name='MAX_LENGTH',
                               initializer=WrappedLinkedText(content_=[WrappedMixedContainer(value=u'100')]))
    signature_w_initializer = find_node(render(app, member_def, show_define_initializer=True), 'desc_signature')
    assert signature_w_initializer.astext() == 'MAX_LENGTH 100'

    member_def_no_show = WrappedMemberDef(kind='define', name='MAX_LENGTH_NO_INITIALIZER',
                               initializer=WrappedLinkedText(content_=[WrappedMixedContainer(value=u'100')]))

    signature_wo_initializer = find_node(render(app, member_def_no_show, show_define_initializer=False), 'desc_signature')
    assert signature_wo_initializer.astext() == 'MAX_LENGTH_NO_INITIALIZER'


def test_render_define_no_initializer(app):
    sphinx.addnodes.setup(app)
    member_def = WrappedMemberDef(kind='define', name='USE_MILK')
    signature = find_node(render(app, member_def), 'desc_signature')
    assert signature.astext() == 'USE_MILK'
