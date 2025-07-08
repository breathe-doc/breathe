from __future__ import annotations

import os
from typing import TYPE_CHECKING

import docutils.parsers.rst
import sphinx.addnodes
import sphinx.environment
import sphinx.locale
from docutils import frontend, nodes, utils

from breathe import parser, renderer
from breathe.renderer.sphinxrenderer import SphinxRenderer

if TYPE_CHECKING:
    from breathe.renderer import filter


sphinx.locale.init([], "")
COMMON_ARGS_memberdefType = {
    "id": "",
    "prot": parser.DoxProtectionKind.public,
    "static": False,
    "location": parser.Node_locationType(file="", line=0),
}


class MockMemo:
    def __init__(self):
        self.title_styles = ""
        self.section_level = ""


class MockState:
    def __init__(self, app):
        from breathe.parser import DoxygenParser
        from breathe.project import ProjectInfoFactory

        env = sphinx.environment.BuildEnvironment(app)
        env.setup(app)
        env.temp_data["docname"] = "mock-doc"
        env.temp_data["breathe_project_info_factory"] = ProjectInfoFactory(app)
        env.temp_data["breathe_dox_parser"] = DoxygenParser(app)
        if hasattr(frontend, "get_default_settings"):
            settings = frontend.get_default_settings(docutils.parsers.rst.Parser)
        else:
            settings = frontend.OptionParser(
                components=(docutils.parsers.rst.Parser,)
            ).get_default_values()
        settings.env = env
        self.document = utils.new_document("", settings)

        # In sphinx 5.3.0 the method state.nested_parse is not called directly
        # so this memo object should exist here
        self.memo = MockMemo()

    def nested_parse(self, content, content_offset, contentnode, match_titles=1):
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
        if lineno is None:
            lineno = 42
        return "mock-doc", lineno


class MockMaskFactory:
    def __init__(self):
        pass

    def mask(self, node):
        return node


class MockContext:
    def __init__(self, app, node_stack, domain=None, options=[]):
        self.domain = domain
        self.node_stack = node_stack
        self.directive_args = [
            None,  # name
            None,  # arguments
            options,  # options
            "",  # content
            None,  # lineno
            None,  # content_offset
            None,  # block_text
            MockState(app),
            MockStateMachine(),
        ]
        self.child = None
        self.mask_factory = MockMaskFactory()

    def create_child_context(self, attribute, tag):
        return self


class MockTargetHandler:
    def __init__(self):
        pass

    def __call__(self, document, refid):
        return []


class MockDocument:
    def __init__(self):
        self.reporter = MockReporter()


class MockCompoundParser:
    """
    A compound parser reads a doxygen XML file from disk; this mock implements
    a mapping of what would be the file name on disk to data using a dict.
    """

    def __init__(self, compound_dict):
        self.compound_dict = compound_dict

    class MockFileData:
        def __init__(self, compounddef):
            self.compounddef = [compounddef]

    class MockCompound:
        def __init__(self, root):
            self.root = root

    def parse_compound(self, compoundname, project_info):
        compounddef = self.compound_dict[compoundname]
        return self.MockCompound(self.MockFileData(compounddef))


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
        raise Exception(f"the number of nodes {name} is {len(found_nodes)}")
    return found_nodes[0]


def test_find_nodes():
    section = nodes.section()
    foo = nodes.Text("foo")
    desc = nodes.description()
    bar = nodes.Text("bar")
    section.children = [foo, desc, bar]
    assert find_nodes(section, "description") == [desc]
    assert find_nodes([section, desc], "description") == [desc, desc]
    assert find_nodes([], "description") == []
    assert find_nodes(section, "unknown") == []
    assert find_nodes(section, "Text") == [foo, bar]


def check_exception(func, message):
    """Check if func() throws an exception with the specified message."""
    exception = None
    try:
        func()
    except Exception as e:
        exception = e
    print(str(exception))
    assert exception
    assert str(exception) == message


def test_find_node():
    section = nodes.section()
    foo = nodes.Text("foo")
    desc = nodes.description()
    bar = nodes.Text("bar")
    section.children = [foo, desc, bar]
    assert find_node(section, "description") == desc
    check_exception(
        lambda: find_node([section, desc], "description"), "the number of nodes description is 2"
    )
    check_exception(lambda: find_node([], "description"), "the number of nodes description is 0")
    check_exception(lambda: find_node([section], "unknown"), "the number of nodes unknown is 0")
    check_exception(lambda: find_node([section], "Text"), "the number of nodes Text is 2")


def render(
    app, member_def, domain=None, show_define_initializer=False, dox_parser=None, options=[]
):
    """Render Doxygen *member_def* with *renderer_class*."""

    app.config.breathe_separate_member_pages = False
    app.config.breathe_use_project_refids = False
    app.config.breathe_show_define_initializer = show_define_initializer
    app.config.breathe_order_parameters_first = False
    app.config.breathe_debug_trace_directives = False
    app.config.breathe_debug_trace_doxygen_ids = False
    app.config.breathe_debug_trace_qualification = False
    r = SphinxRenderer(
        app,
        None,  # project_info
        [],  # node_stack
        None,  # state
        None,  # document
        MockTargetHandler(),
        dox_parser,
        (lambda nstack: True),
    )
    r.context = MockContext(app, [renderer.TaggedNode(None, member_def)], domain, options)
    return r.render(member_def)


def test_render_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void foo",
        type=parser.Node_linkedTextType(["void"]),
        name="foo",
        argsstring="(int)",
        virt=parser.DoxVirtualKind.non_virtual,
        param=[parser.Node_paramType(type=parser.Node_linkedTextType(["int"]))],
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext().startswith("void")
    n = find_node(signature, "desc_name")[0]
    assert isinstance(n, sphinx.addnodes.desc_sig_name)
    assert len(n) == 1
    assert n[0] == "foo"
    params = find_node(signature, "desc_parameterlist")
    assert len(params) == 1
    param = params[0]
    assert isinstance(param[0], sphinx.addnodes.desc_sig_keyword_type)
    assert param[0][0] == "int"


def test_render_typedef(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.typedef,
        definition="typedef int foo",
        type=parser.Node_linkedTextType(["int"]),
        name="foo",
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext() == "typedef int foo"


def test_render_c_typedef(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.typedef,
        definition="typedef unsigned int bar",
        type=parser.Node_linkedTextType(["unsigned int"]),
        name="bar",
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def, domain="c"), "desc_signature")
    assert signature.astext() == "typedef unsigned int bar"


def test_render_c_function_typedef(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.typedef,
        definition="typedef void* (*voidFuncPtr)(float, int)",
        type=parser.Node_linkedTextType(["void* (*"]),
        name="voidFuncPtr",
        argsstring=")(float, int)",
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def, domain="c"), "desc_signature")
    assert signature.astext().startswith("typedef void *")
    # the use of desc_parameterlist in this case was not correct,
    # it should only be used for a top-level function


def test_render_using_alias(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.typedef,
        definition="using foo = int",
        type=parser.Node_linkedTextType(["int"]),
        name="foo",
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext() == "using foo = int"


def test_render_const_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void f",
        type=parser.Node_linkedTextType(["void"]),
        name="f",
        argsstring="() const",
        virt=parser.DoxVirtualKind.non_virtual,
        const=True,
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert "_CPPv2NK1fEv" in signature["ids"]


def test_render_lvalue_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void f",
        type=parser.Node_linkedTextType(["void"]),
        name="f",
        argsstring="() &",
        virt=parser.DoxVirtualKind.non_virtual,
        refqual=parser.DoxRefQualifierKind.lvalue,
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext().endswith("&")


def test_render_rvalue_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void f",
        type=parser.Node_linkedTextType(["void"]),
        name="f",
        argsstring="() &&",
        virt=parser.DoxVirtualKind.non_virtual,
        refqual=parser.DoxRefQualifierKind.rvalue,
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext().endswith("&&")


def test_render_const_lvalue_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void f",
        type=parser.Node_linkedTextType(["void"]),
        name="f",
        argsstring="() const &",
        virt=parser.DoxVirtualKind.non_virtual,
        const=True,
        refqual=parser.DoxRefQualifierKind.lvalue,
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext().endswith("const &")


def test_render_const_rvalue_func(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.function,
        definition="void f",
        type=parser.Node_linkedTextType(["void"]),
        name="f",
        argsstring="() const &&",
        virt=parser.DoxVirtualKind.non_virtual,
        const=True,
        refqual=parser.DoxRefQualifierKind.rvalue,
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext().endswith("const &&")


def test_render_variable_initializer(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.variable,
        definition="const int EOF",
        type=parser.Node_linkedTextType(["const int"]),
        name="EOF",
        initializer=parser.Node_linkedTextType(["= -1"]),
        **COMMON_ARGS_memberdefType,
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext() == "const int EOF = -1"


def test_render_define_initializer(app):
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.define,
        name="MAX_LENGTH",
        initializer=parser.Node_linkedTextType(["100"]),
        **COMMON_ARGS_memberdefType,
    )
    signature_w_initializer = find_node(
        render(app, member_def, show_define_initializer=True), "desc_signature"
    )
    assert signature_w_initializer.astext() == "MAX_LENGTH 100"

    member_def_no_show = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.define,
        name="MAX_LENGTH_NO_INITIALIZER",
        initializer=parser.Node_linkedTextType(["100"]),
        **COMMON_ARGS_memberdefType,
    )

    signature_wo_initializer = find_node(
        render(app, member_def_no_show, show_define_initializer=False), "desc_signature"
    )
    assert signature_wo_initializer.astext() == "MAX_LENGTH_NO_INITIALIZER"


def test_render_define_no_initializer(app):
    sphinx.addnodes.setup(app)
    member_def = parser.Node_memberdefType(
        kind=parser.DoxMemberKind.define, name="USE_MILK", **COMMON_ARGS_memberdefType
    )
    signature = find_node(render(app, member_def), "desc_signature")
    assert signature.astext() == "USE_MILK"


def test_render_innergroup(app):
    refid = "group__innergroup"
    mock_compound_parser = MockCompoundParser({
        refid: parser.Node_compounddefType(
            kind=parser.DoxCompoundKind.group,
            compoundname="InnerGroup",
            briefdescription=parser.Node_descriptionType(["InnerGroup"]),
            id="",
            prot=parser.DoxProtectionKind.public,
        )
    })
    ref = parser.Node_refType(["InnerGroup"], refid=refid)
    compound_def = parser.Node_compounddefType(
        kind=parser.DoxCompoundKind.group,
        compoundname="OuterGroup",
        briefdescription=parser.Node_descriptionType(["OuterGroup"]),
        innergroup=[ref],
        id="",
        prot=parser.DoxProtectionKind.public,
    )
    assert all(
        el.astext() != "InnerGroup"
        for el in render(app, compound_def, dox_parser=mock_compound_parser)
    )
    assert any(
        el.astext() == "InnerGroup"
        for el in render(app, compound_def, dox_parser=mock_compound_parser, options=["inner"])
    )


def get_directive(app):
    from docutils.statemachine import StringList

    from breathe.directives.function import DoxygenFunctionDirective

    app.config.breathe_separate_member_pages = False
    app.config.breathe_default_project = "test_project"
    app.config.breathe_domain_by_extension = {}
    app.config.breathe_domain_by_file_pattern = {}
    app.config.breathe_use_project_refids = False
    cls_args = (
        "doxygenclass",
        ["at::Tensor"],
        {"members": "", "protected-members": None, "undoc-members": None},
        StringList([], items=[]),
        20,
        24,
        (
            ".. doxygenclass:: at::Tensor\n   :members:\n"
            "   :protected-members:\n   :undoc-members:"
        ),
        MockState(app),
        MockStateMachine(),
    )  # fmt: skip
    return DoxygenFunctionDirective(*cls_args)


def get_matches(datafile) -> tuple[list[str], list[filter.FinderMatch]]:
    with open(os.path.join(os.path.dirname(__file__), "data", datafile), "rb") as fid:
        doc = parser.parse_file(fid)
    assert isinstance(doc.value, parser.Node_DoxygenType)

    sectiondef = doc.value.compounddef[0].sectiondef[0]
    argsstrings = [child.argsstring for child in sectiondef.memberdef if child.argsstring]
    matches = [
        [renderer.TaggedNode(None, m), renderer.TaggedNode(None, sectiondef)]
        for m in sectiondef.memberdef
    ]
    return argsstrings, matches


def test_resolve_overrides(app):
    # Test that multiple function overrides works
    argsstrings, matches = get_matches("arange.xml")
    cls = get_directive(app)

    # Verify that the exact arguments returns one override
    for args in argsstrings:
        ast_param = cls._parse_args(args)
        _ = cls._resolve_function(matches, ast_param, None)


def test_ellipsis(app):
    argsstrings, matches = get_matches("ellipsis.xml")
    cls = get_directive(app)

    # Verify that parsing an ellipsis works
    ast_param = cls._parse_args(argsstrings[0])
    _ = cls._resolve_function(matches, ast_param, None)
