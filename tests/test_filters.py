from __future__ import annotations

import os.path
from typing import NamedTuple

import pytest

from breathe import parser
from breathe.renderer import TaggedNode, filter

DEFAULT_OPTS = {"path": "", "project": "", "membergroups": "", "show": ""}


@pytest.fixture(scope="module")
def class_doc():
    with open(os.path.join(os.path.dirname(__file__), "data", "classSample.xml"), "rb") as fid:
        return parser.parse_file(fid).value


class SampleMembers(NamedTuple):
    public_field: filter.NodeStack
    public_method: filter.NodeStack
    protected_field: filter.NodeStack
    protected_method: filter.NodeStack
    private_field: filter.NodeStack
    private_method: filter.NodeStack


@pytest.fixture
def members(class_doc):
    common = [TaggedNode(None, class_doc.compounddef[0]), TaggedNode(None, class_doc)]

    memberdefs = {}

    for sect in class_doc.compounddef[0].sectiondef:
        member = sect.memberdef[0]
        memberdefs[member.name] = filter.NodeStack(
            [TaggedNode(None, member), TaggedNode(None, sect)] + common
        )

    return SampleMembers(
        memberdefs["public_field"],
        memberdefs["public_method"],
        memberdefs["protected_field"],
        memberdefs["protected_method"],
        memberdefs["private_field"],
        memberdefs["private_method"],
    )


def create_class_filter(app, extra_ops):
    opts = DEFAULT_OPTS.copy()
    opts.update(extra_ops)
    return filter.create_class_filter(app, "Sample", opts)


def test_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(app, {})

    assert not filter(members.public_field)
    assert not filter(members.public_method)
    assert not filter(members.protected_field)
    assert not filter(members.protected_method)
    assert not filter(members.private_field)
    assert not filter(members.private_method)


bools = (True, False)


@pytest.mark.parametrize("public", bools)
@pytest.mark.parametrize("private", bools)
@pytest.mark.parametrize("protected", bools)
@pytest.mark.parametrize("undocumented", bools)
def test_public_class_members(app, members, public, private, protected, undocumented):
    app.config.breathe_default_members = []

    opts = {}
    if public:
        opts["members"] = None
    if private:
        opts["private-members"] = None
    if protected:
        opts["protected-members"] = None
    if undocumented:
        opts["undoc-members"] = None
    filter = create_class_filter(app, opts)

    assert filter(members.public_field) == public
    assert filter(members.public_method) == (public and undocumented)
    assert filter(members.protected_field) == (protected and undocumented)
    assert filter(members.protected_method) == protected
    assert filter(members.private_field) == private
    assert filter(members.private_method) == (private and undocumented)


def test_specific_class_members(app, members):
    app.config.breathe_default_members = []

    filter = create_class_filter(
        app, {"members": "public_method,protected_method,private_field", "undoc-members": None}
    )

    assert not filter(members.public_field)
    assert filter(members.public_method)
    assert not filter(members.protected_field)
    assert filter(members.protected_method)
    assert filter(members.private_field)
    assert not filter(members.private_method)


# def test_nested_class_filtered(app):
#     app.config.breathe_default_members = []
#
#     doc = parser.parse_str(
#         """<doxygen version="1.9.8">
#         <compounddef id="sample_8hpp" kind="file" language="C++">
#             <compoundname>sample.hpp</compoundname>
#             <innerclass refid="classSample" prot="public">Sample</innerclass>
#             <innerclass refid="classSample_1_1Inner" prot="public">Sample::Inner</innerclass>
#             <location file="sample.hpp"/>
#         </compounddef>
#         </doxygen>"""
#     )
#
#     compounddef = doc.value.compounddef[0]
#     ref_outer, ref_inner = compounddef.innerclass
#
#     filter_ = filter.create_file_filter(
#         app, "sample.hpp", DEFAULT_OPTS, init_valid_names=("Sample", "Sample::Inner")
#     )
#     assert filter_(filter.NodeStack([TaggedNode("innerclass", ref_outer), TaggedNode(None, compounddef)]))  # noqa: E501
#     assert not filter_(
#         filter.NodeStack([TaggedNode("innerclass", ref_inner), TaggedNode(None, compounddef)])
#     )
