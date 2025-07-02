"""
Filters
-------

Filters are an interesting and somewhat challenging part of the code base. They are used for
two different purposes:

 - To figure out which nodes in the xml hierarchy to start rendering from. These are called
   'finder filters' or 'content filters'. This is done before rendering starts.
 - To figure out which nodes under a selected nodes in the xml hierarchy should be rendered. These
   are called 'render filters'. This is done during the render process with a test in the
   DoxygenToRstRendererFactory.


Finder Filters
~~~~~~~~~~~~~~

The implementation of the filters can change a little depending on how they are called. Finder
filters are called from the breathe.finder.doxygen.index and breathe.finder.doxygen.compound files.
They are called like this:

    # Descend down the hierarchy
    # ...

    if filter_(node_stack):
        matches.append(self.data_object)

    # Keep on descending
    # ...

This means that the result of the filter does not stop us descending down the hierarchy and testing
more nodes. This simplifies the filters as they only have to return true for the exact nodes they
are interested in and they don't have to worry about allowing the iteration down the hierarchy to
continue for nodes which don't match.


Content Filters
~~~~~~~~~~~~~~~

Content filters are harder than the finder filters as they are responsible for halting the iteration
down the hierarchy if they return false. This means that if you're interested in Node_memberdefType
nodes with a particular attribute then you have to check for that but also include a clause which
allows all other non-Node_memberdefType nodes to pass through as you don't want to interrupt them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from breathe import parser, renderer

if TYPE_CHECKING:
    import sys
    from collections.abc import Container, Iterable, Mapping
    from typing import Any, Callable, SupportsIndex, Union

    from sphinx.application import Sphinx

    if sys.version_info >= (3, 11):
        from typing import Any, TypeAlias
    else:
        from typing_extensions import TypeAlias

    from breathe.directives.class_like import DoxClassOptions
    from breathe.directives.content_block import DoxContentBlockOptions
    from breathe.project import ProjectInfo

    DoxFilter: TypeAlias = Callable[["NodeStack"], bool]

    FinderMatch: TypeAlias = list[renderer.TaggedNode]
    FinderMatchItr: TypeAlias = Iterable[FinderMatch]

    DoxIndexFilter: TypeAlias = Callable[[parser.DoxygenIndex], FinderMatchItr]

    DoxNamespaceOptions: TypeAlias = Union[DoxClassOptions, DoxContentBlockOptions]

    T_options = Union[DoxClassOptions, DoxContentBlockOptions]


CLASS_LIKE_COMPOUNDDEF = (
    parser.DoxCompoundKind.class_,
    parser.DoxCompoundKind.struct,
    parser.DoxCompoundKind.interface,
)


class NodeStack:
    def __init__(self, stack: list[renderer.TaggedNode]):
        self.stack = stack

    def ancestor(self, generations: SupportsIndex) -> renderer.DataObject | None:
        i = generations.__index__()
        return self.stack[i].value if len(self.stack) > i else None

    @property
    def parent(self) -> renderer.DataObject | None:
        return self.stack[1].value if len(self.stack) > 1 else None

    @property
    def node(self) -> renderer.DataObject:
        return self.stack[0].value

    @property
    def tag(self) -> str:
        tag = self.stack[0].tag
        assert tag is not None
        return tag


def set_defaults(app: Sphinx, options: T_options) -> T_options:
    r: Any = options.copy()
    for m in app.config.breathe_default_members:
        r.setdefault(m, "")
    return r


def create_show_filter(options: Mapping[str, Any]) -> DoxFilter:
    """Currently only handles the header-file entry"""

    if options.get("show") == "header-file":
        return lambda nstack: True

    # Allow through everything except the header-file includes nodes
    def filter_(nstack: NodeStack) -> bool:
        return not (
            isinstance(nstack.parent, parser.Node_compounddefType)
            and isinstance(nstack.node, parser.Node_incType)
        )

    return filter_


def _create_undoc_members_filter(options: DoxNamespaceOptions) -> DoxFilter:
    if "undoc-members" in options:
        return lambda nstack: True

    def filter_(nstack: NodeStack) -> bool:
        node = nstack.node
        # Allow anything that isn't a Node_memberdefType, or if it is only
        # allow the ones with a description
        return (not isinstance(node, parser.Node_memberdefType)) or bool(
            parser.description_has_content(node.briefdescription)
            or parser.description_has_content(node.detaileddescription)
        )

    return filter_


def _create_public_members_filter(
    options: DoxNamespaceOptions,
) -> Callable[[parser.Node_memberdefType], bool]:
    if "members" in options:
        # If the user has specified the 'members' option with arguments then
        # we only pay attention to that and not to any other member settings
        members_str = options["members"]
        if members_str and not members_str.isspace():
            # Matches sphinx-autodoc behaviour of comma separated values
            members = frozenset([x.strip() for x in members_str.split(",")])

            # Accept any nodes which don't have a "sectiondef" as a parent
            # or, if they do, only accept them if their names are in the
            # members list
            def filter_(node: parser.Node_memberdefType) -> bool:
                return node.name in members

        else:
            # Select anything that doesn't have a parent which is a
            # sectiondef, or, if it does, only select the public ones
            def filter_(node: parser.Node_memberdefType) -> bool:
                return node.prot == parser.DoxProtectionKind.public

    else:
        # Nothing with a parent that's a sectiondef
        def filter_(node: parser.Node_memberdefType) -> bool:
            return False

    return filter_


def create_description_filter(allow: bool, level: type[parser.Node]) -> DoxFilter:
    """Whether or not we allow descriptions is determined by the calling function and we just do
    whatever the 'allow' function parameter tells us.
    """

    if allow:
        # Let through any description children of sectiondefs if we output any kind members
        def filter_(nstack: NodeStack) -> bool:
            return not isinstance(nstack.parent, level) or isinstance(
                nstack.node, parser.Node_descriptionType
            )

    else:
        # Nothing with a parent that's a sectiondef
        def filter_(nstack: NodeStack) -> bool:
            return not isinstance(nstack.parent, level)

    return filter_


def create_class_member_filter(options: DoxNamespaceOptions) -> DoxFilter:
    """Content filter based on :members: and :private-members: classes"""

    # I can't fully explain the filtering of descriptions here. More testing needed to figure
    # out when it is needed. This approach reflects the old code that was here but it wasn't
    # commented (my fault.) I wonder if maybe the public and private declarations themselves can
    # be documented and we need to let them through. Not sure.
    allow = "members" in options or "protected-members" in options or "private-members" in options

    description = create_description_filter(allow, parser.Node_sectiondefType)

    # Create all necessary filters and combine them
    public_members = _create_public_members_filter(options)

    undoc_members = _create_undoc_members_filter(options)

    prot_filter: tuple[parser.DoxProtectionKind, ...] = ()
    if "protected-members" in options:
        prot_filter += (parser.DoxProtectionKind.protected,)
    if "private-members" in options:
        prot_filter += (parser.DoxProtectionKind.private,)

    # Allow anything that isn't a memberdef, or if it is, and 'prot' is not
    # empty, allow the ones with an equal 'prot' attribute
    def filter_(nstack: NodeStack) -> bool:
        node = nstack.node
        return (
            (
                not (
                    isinstance(node, parser.Node_memberdefType)
                    and isinstance(nstack.parent, parser.Node_sectiondefType)
                )
                or (bool(prot_filter) and node.prot in prot_filter)
                or public_members(node)
            )
            and undoc_members(nstack)
        ) or description(nstack)

    return filter_


def create_innerclass_filter(options: DoxNamespaceOptions, outerclass: str = "") -> DoxFilter:
    """
    :param outerclass: Should be the class/struct being target by the directive calling this
                        code. If it is a group or namespace directive then it should be left
                        blank. It is used when looking for names listed in the :members: option.

                        The name should include any additional namespaces that the target class
                        is in.
    """
    allowed: set[parser.DoxProtectionKind] = set()
    if "protected-members" in options:
        allowed.add(parser.DoxProtectionKind.protected)
    if "private-members" in options:
        allowed.add(parser.DoxProtectionKind.private)

    description = create_description_filter(True, parser.Node_compounddefType)

    members: set[str] | None = None
    if "members" in options:
        members_str = options["members"]
        if members_str and members_str.strip():
            prefix = ("%s::" % outerclass) if outerclass else ""

            # Matches sphinx-autodoc behaviour of comma separated values
            members = {"%s%s" % (prefix, x.strip()) for x in members_str.split(",")}
        else:
            allowed.add(parser.DoxProtectionKind.public)

    def filter_(nstack: NodeStack) -> bool:
        node = nstack.node
        parent = nstack.parent

        return (
            not (
                isinstance(node, parser.Node_refType)
                and nstack.tag == "innerclass"
                and isinstance(parent, parser.Node_compounddefType)
                and parent.kind in CLASS_LIKE_COMPOUNDDEF
            )
            or node.prot in allowed
            or (members is not None and "".join(node) in members)
            or description(nstack)
        )

    return filter_


def create_class_filter(app: Sphinx, target: str, options: DoxClassOptions) -> DoxFilter:
    """Content filter for classes based on various directive options"""

    filter_options = set_defaults(app, options)

    cm_filter = create_class_member_filter(filter_options)
    ic_filter = create_innerclass_filter(filter_options, outerclass=target)
    o_filter = create_outline_filter(filter_options)
    s_filter = create_show_filter(filter_options)

    return (
        lambda nstack: cm_filter(nstack)
        and ic_filter(nstack)
        and o_filter(nstack)
        and s_filter(nstack)
    )


def create_outline_filter(options: Mapping[str, Any]) -> DoxFilter:
    if "outline" in options:
        return lambda nstack: not isinstance(
            nstack.node, (parser.Node_descriptionType, parser.Node_incType)
        )

    return lambda nstack: True


def extend_member_with_compound(
    d_parser: parser.DoxygenParser,
    project_info: ProjectInfo,
    m: parser.Node_MemberType,
    c: parser.Node_CompoundType,
    index: parser.Node_DoxygenTypeIndex,
) -> FinderMatch:
    dc = d_parser.parse_compound(c.refid, project_info)
    mdef, sdef, cdef = dc.members_by_id[m.refid]

    TN = renderer.TaggedNode
    return [
        TN("memberdef", mdef),
        TN("sectiondef", sdef),
        TN("compounddef", cdef),
        TN("doxygen", dc.root),
        TN("compound", c),
        TN("doxygenindex", index),
    ]


def member_finder_filter(
    app: Sphinx,
    namespace: str,
    name: str,
    d_parser: parser.DoxygenParser,
    project_info: ProjectInfo,
    kinds: Container[parser.MemberKind] | str,
    index: parser.DoxygenIndex,
) -> FinderMatchItr:
    """Looks for a member with the specified name and kind."""

    if isinstance(kinds, str):
        kinds = (parser.MemberKind(kinds),)

    if namespace:
        c_kinds = {
            parser.CompoundKind.namespace,
            parser.CompoundKind.class_,
            parser.CompoundKind.struct,
            parser.CompoundKind.interface,
        }

        for m, c in index.members[name]:
            if c.kind in c_kinds and c.name == namespace:
                if m.kind in kinds:
                    yield extend_member_with_compound(d_parser, project_info, m, c, index.root)

    else:
        ext = tuple(app.config.breathe_implementation_filename_extensions)

        for m, c in index.members[name]:
            if c.kind != parser.CompoundKind.file or not c.name.endswith(ext):
                if m.kind in kinds:
                    yield extend_member_with_compound(d_parser, project_info, m, c, index.root)


def compound_finder_filter(
    name: str,
    kind: str,
    index: parser.DoxygenIndex,
) -> FinderMatchItr:
    """Looks for a compound with the specified name and kind."""

    for c in index.compounds[name]:
        if c.kind.value != kind:
            continue

        yield [
            renderer.TaggedNode("compound", c),
            renderer.TaggedNode("doxygenindex", index.root),
        ]
