from __future__ import annotations

import os.path
import pytest
from typing import NamedTuple

from breathe import parser
from breathe.renderer import TaggedNode
from breathe.renderer.filter import FilterFactory, NodeStack


DEFAULT_OPTS = opts = {
    'path': '',
    'project': '',
    'membergroups': '',
    'show': '',
    'undoc-members': None}

@pytest.fixture(scope="module")
def class_doc():
    with open(os.path.join(os.path.dirname(__file__), "data", "classSample.xml"), "rb") as fid:
        return parser.parse_file(fid).value

class SampleMembers(NamedTuple):
    public_field: NodeStack
    public_method: NodeStack
    protected_field: NodeStack
    protected_method: NodeStack
    private_field: NodeStack
    private_method: NodeStack

@pytest.fixture
def members(class_doc):
    common = [
        TaggedNode(None, class_doc.compounddef[0]),
        TaggedNode(None, class_doc)
    ]

    memberdefs = {}

    for sect in class_doc.compounddef[0].sectiondef:
        member = sect.memberdef[0]
        memberdefs[member.name] = NodeStack([TaggedNode(None, member), TaggedNode(None, sect)] + common)

    return SampleMembers(
        memberdefs['public_field'],
        memberdefs['public_method'],
        memberdefs['protected_field'],
        memberdefs['protected_method'],
        memberdefs['private_field'],
        memberdefs['private_method']
    )

def create_class_filter(app, extra_ops):
    opts = DEFAULT_OPTS.copy()
    opts.update(extra_ops)
    return FilterFactory(app).create_class_filter('Sample', opts)

def test_no_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app,{})

    assert not filter(members.public_field)
    assert not filter(members.public_method)
    assert not filter(members.protected_field)
    assert not filter(members.protected_method)
    assert not filter(members.private_field)
    assert not filter(members.private_method)

def test_public_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app,{'members': ''})

    assert filter(members.public_field)
    assert filter(members.public_method)
    assert not filter(members.protected_field)
    assert not filter(members.protected_method)
    assert not filter(members.private_field)
    assert not filter(members.private_method)

def test_prot_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app,{
        'members': '',
        'protected-members': None})

    assert filter(members.public_field)
    assert filter(members.public_method)
    assert filter(members.protected_field)
    assert filter(members.protected_method)
    assert not filter(members.private_field)
    assert not filter(members.private_method)

def test_all_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app,{
        'members': '',
        'protected-members': None,
        'private-members': None})

    assert filter(members.public_field)
    assert filter(members.public_method)
    assert filter(members.protected_field)
    assert filter(members.protected_method)
    assert filter(members.private_field)
    assert filter(members.private_method)

def test_specific_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app,{
        'members': 'public_method,protected_method,private_field'})

    assert not filter(members.public_field)
    assert filter(members.public_method)
    assert not filter(members.protected_field)
    assert filter(members.protected_method)
    assert filter(members.private_field)
    assert not filter(members.private_method)

def test_nested_class_filtered(app):
    app.config.breathe_default_members = []

    doc = parser.parse_str("""<doxygen version="1.9.8">
        <compounddef id="sample_8hpp" kind="file" language="C++">
            <compoundname>sample.hpp</compoundname>
            <innerclass refid="classSample" prot="public">Sample</innerclass>
            <innerclass refid="classSample_1_1Inner" prot="public">Sample::Inner</innerclass>
            <location file="sample.hpp"/>
        </compounddef>
        </doxygen>""")

    compounddef = doc.value.compounddef[0]
    ref_outer, ref_inner = compounddef.innerclass

    filter = FilterFactory(app).create_file_filter('sample.hpp', DEFAULT_OPTS, init_valid_names=('Sample','Sample::Inner'))
    assert filter(NodeStack([TaggedNode('innerclass',ref_outer), TaggedNode(None, compounddef)]))
    assert not filter(NodeStack([TaggedNode('innerclass',ref_inner), TaggedNode(None, compounddef)]))
