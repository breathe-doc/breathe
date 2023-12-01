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

from breathe import path_handler, parser

from sphinx.application import Sphinx

import os
from typing import Any, Callable, Literal, SupportsIndex, TYPE_CHECKING
from collections.abc import Container, Iterable, Mapping

if TYPE_CHECKING:
    from typing_extensions import TypeAlias, TypeVar
    from breathe import renderer
    from breathe.directives.class_like import DoxClassOptions
    from breathe.directives.content_block import DoxContentBlockOptions

    DoxNamespaceOptions: TypeAlias = DoxClassOptions | DoxContentBlockOptions

    T_options = TypeVar("T_options", DoxClassOptions, DoxContentBlockOptions)

    DoxFilter: TypeAlias = Callable[["NodeStack"], bool]
else:
    DoxClassOptions = None
    DoxNamespaceOptions = None


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
    def tag(self) -> str | None:
        return self.stack[0].tag


def path_matches(location: str, target_file: str) -> bool:
    if path_handler.includes_directory(target_file):
        # If the target_file contains directory separators then
        # match against the same length at the end of the location
        #
        location_match = location[-len(target_file) :]
        return location_match == target_file

    # If there are no separators, match against the whole filename
    # at the end of the location
    #
    # This is to prevent "Util.cpp" matching "PathUtil.cpp"
    #
    location_basename = os.path.basename(location)
    return location_basename == target_file


def location_matches(location: parser.Node_locationType | None, target_file: str) -> bool:
    return location is not None and path_matches(location.file, target_file)


def namespace_matches(name: str, node: parser.Node_compounddefType):
    to_find = name.rpartition("::")[0]
    return any(to_find == "".join(ns) for ns in node.innernamespace) or any(
        to_find == "".join(ns) for ns in node.innerclass
    )


class FilterFactory:
    # C++ style public entries
    public_kinds = set(
        [
            "public-type",
            "public-func",
            "public-attrib",
            "public-slot",
            "public-static-func",
            "public-static-attrib",
        ]
    )

    def __init__(self, app: Sphinx) -> None:
        self.app = app

    def set_defaults(self, options: T_options) -> T_options:
        r: Any = options.copy()
        for m in self.app.config.breathe_default_members:
            r.setdefault(m, "")
        return r

    def create_render_filter(
        self, kind: Literal["group", "page", "namespace"], options: DoxContentBlockOptions
    ) -> DoxFilter:
        """Render filter for group & namespace blocks"""

        filter_options = self.set_defaults(options)

        if "desc-only" in filter_options:
            return self._create_description_filter(True, parser.Node_compounddefType)

        cm_filter = self.create_class_member_filter(filter_options)
        ic_filter = self.create_innerclass_filter(filter_options)
        o_filter = self.create_outline_filter(filter_options)

        def filter(nstack: NodeStack) -> bool:
            grandparent = nstack.ancestor(2)
            return (
                (
                    cm_filter(nstack)
                    or (
                        isinstance(grandparent, parser.Node_compounddefType)
                        and grandparent.kind not in CLASS_LIKE_COMPOUNDDEF
                        and isinstance(nstack.node, parser.Node_memberdefType)
                    )
                )
                and ic_filter(nstack)
                and o_filter(nstack)
            )

        return filter

    def create_class_filter(self, target: str, options: DoxClassOptions) -> DoxFilter:
        """Content filter for classes based on various directive options"""

        filter_options = self.set_defaults(options)

        cm_filter = self.create_class_member_filter(filter_options)
        ic_filter = self.create_innerclass_filter(filter_options, outerclass=target)
        o_filter = self.create_outline_filter(filter_options)
        s_filter = self.create_show_filter(filter_options)

        return (
            lambda nstack: cm_filter(nstack)
            and ic_filter(nstack)
            and o_filter(nstack)
            and s_filter(nstack)
        )

    @classmethod
    def create_innerclass_filter(
        cls, options: DoxNamespaceOptions, outerclass: str = ""
    ) -> DoxFilter:
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

        description = cls._create_description_filter(True, parser.Node_compounddefType)

        members: set[str] | None = None
        if "members" in options:
            members_str = options["members"]
            if members_str and members_str.strip():
                prefix = ("%s::" % outerclass) if outerclass else ""

                # Matches sphinx-autodoc behaviour of comma separated values
                members = set(["%s%s" % (prefix, x.strip()) for x in members_str.split(",")])
            else:
                allowed.add(parser.DoxProtectionKind.public)

        def filter(nstack: NodeStack) -> bool:
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

        return filter

    @staticmethod
    def create_show_filter(options: Mapping[str, Any]) -> DoxFilter:
        """Currently only handles the header-file entry"""

        if options.get("show") == "header-file":
            return lambda nstack: True

        # Allow through everything except the header-file includes nodes
        def filter(nstack: NodeStack) -> bool:
            return not (
                isinstance(nstack.parent, parser.Node_compounddefType)
                and isinstance(nstack.node, parser.Node_incType)
            )

        return filter

    @staticmethod
    def _create_description_filter(allow: bool, level: type[parser.Node]) -> DoxFilter:
        """Whether or not we allow descriptions is determined by the calling function and we just do
        whatever the 'allow' function parameter tells us.
        """

        if allow:
            # Let through any description children of sectiondefs if we output any kind members
            def filter(nstack: NodeStack) -> bool:
                return not isinstance(nstack.parent, level) or isinstance(
                    nstack.node, parser.Node_descriptionType
                )

        else:
            # Nothing with a parent that's a sectiondef
            def filter(nstack: NodeStack) -> bool:
                return not isinstance(nstack.parent, level)

        return filter

    @staticmethod
    def _create_public_members_filter(
        options: DoxNamespaceOptions,
    ) -> Callable[[parser.Node_memberdefType], bool]:
        if "members" in options:
            # If the user has specified the 'members' option with arguments then
            # we only pay attention to that and not to any other member settings
            members_str = options["members"]
            if members_str and members_str.strip():
                # Matches sphinx-autodoc behaviour of comma separated values
                members = set([x.strip() for x in members_str.split(",")])

                # Accept any nodes which don't have a "sectiondef" as a parent
                # or, if they do, only accept them if their names are in the
                # members list
                def filter(node: parser.Node_memberdefType) -> bool:
                    return node.name in members

            else:
                # Select anything that doesn't have a parent which is a
                # sectiondef, or, if it does, only select the public ones
                def filter(node: parser.Node_memberdefType) -> bool:
                    return node.prot == parser.DoxProtectionKind.public

        else:
            # Nothing with a parent that's a sectiondef
            def filter(node: parser.Node_memberdefType) -> bool:
                return False

        return filter

    @staticmethod
    def _create_undoc_members_filter(options: DoxNamespaceOptions) -> DoxFilter:
        if "undoc-members" in options:
            return lambda nstack: True

        def filter(nstack: NodeStack) -> bool:
            node = nstack.node
            # Allow anything that isn't a Node_memberdefType, or if it is only
            # allow the ones with a description
            return (not isinstance(node, parser.Node_memberdefType)) or bool(
                node.briefdescription or node.detaileddescription
            )

        return filter

    @classmethod
    def create_class_member_filter(cls, options: DoxNamespaceOptions) -> DoxFilter:
        """Content filter based on :members: and :private-members: classes"""

        # I can't fully explain the filtering of descriptions here. More testing needed to figure
        # out when it is needed. This approach reflects the old code that was here but it wasn't
        # commented (my fault.) I wonder if maybe the public and private declarations themselves can
        # be documented and we need to let them through. Not sure.
        allow = (
            "members" in options or "protected-members" in options or "private-members" in options
        )

        description = cls._create_description_filter(allow, parser.Node_sectiondefType)

        # Create all necessary filters and combine them
        public_members = cls._create_public_members_filter(options)

        undoc_members = cls._create_undoc_members_filter(options)

        prot_filter = ()
        if "protected-members" in options:
            prot_filter += (parser.DoxProtectionKind.protected,)
        if "private-members" in options:
            prot_filter += (parser.DoxProtectionKind.private,)

        # Allow anything that isn't a memberdef, or if it is, and 'prot' is not
        # empty, allow the ones with an equal 'prot' attribute
        def filter(nstack: NodeStack) -> bool:
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

        return filter

    @staticmethod
    def create_outline_filter(options: Mapping[str, Any]) -> DoxFilter:
        if "outline" in options:
            return lambda nstack: not isinstance(
                nstack.node, (parser.Node_descriptionType, parser.Node_incType)
            )

        return lambda nstack: True

    @classmethod
    def create_file_filter(
        cls,
        filename: str,
        options: Mapping[str, Any],
        *,
        init_valid_names: Iterable[str] | None = None,
    ) -> DoxFilter:
        valid_names: set[str] = set()
        if init_valid_names:
            valid_names.update(init_valid_names)

        outline_filter = cls.create_outline_filter(options)

        def filter(nstack: NodeStack) -> bool:
            if not outline_filter(nstack):
                return False

            node = nstack.node
            parent = nstack.parent
            if isinstance(node, parser.Node_compounddefType):
                if node.kind == parser.DoxCompoundKind.file:
                    # Gather the "namespaces" attribute from the
                    # compounddef for the file we're rendering and
                    # store the information in the "valid_names" list
                    if location_matches(node.location, filename):
                        valid_names.update("".join(ns) for ns in node.innernamespace)
                        valid_names.update("".join(ns) for ns in node.innerclass)

                if node.kind != parser.DoxCompoundKind.namespace:
                    # Ignore compounddefs which are from another file
                    # (normally means classes and structs which are in a
                    # namespace that we have other interests in) but only
                    # check it if the compounddef is not a namespace
                    # itself, as for some reason compounddefs for
                    # namespaces are registered with just a single file
                    # location even if they namespace is spread over
                    # multiple files
                    return location_matches(node.location, filename)

            elif isinstance(node, parser.Node_refType):
                name = "".join(node)
                if isinstance(parent, parser.Node_compounddefType) and nstack.tag in {
                    "innerclass",
                    "innernamespace",
                }:
                    # Take the valid_names and every time we handle an
                    # innerclass or innernamespace, check that its name
                    # was one of those initial valid names so that we
                    # never end up rendering a namespace or class that
                    # wasn't in the initial file. Notably this is
                    # required as the location attribute for the
                    # namespace in the xml is unreliable.
                    if name not in valid_names:
                        return False

                    # Ignore innerclasses and innernamespaces that are inside a
                    # namespace that is going to be rendered as they will be
                    # rendered with that namespace and we don't want them twice
                    if namespace_matches(name, parent):
                        return False

            elif isinstance(node, parser.Node_memberdefType):
                # Ignore memberdefs from files which are different to
                # the one we're rendering. This happens when we have to
                # cross into a namespace xml file which has entries
                # from multiple files in it
                return path_matches(node.location.file, filename)

            return True

        return filter

    @staticmethod
    def create_content_filter(
        kind: Literal["group", "page", "namespace"], options: Mapping[str, Any]
    ) -> DoxFilter:
        """Returns a filter which matches the contents of the or namespace but not the group or
        namepace name or description.

        This allows the groups to be used to structure sections of the documentation rather than to
        structure and further document groups of documentation

        As a finder/content filter we only need to match exactly what we're interested in.
        """

        def filter(nstack: NodeStack) -> bool:
            node = nstack.node
            parent = nstack.parent

            if isinstance(node, parser.Node_memberdefType):
                return node.prot == parser.DoxProtectionKind.public

            return (
                isinstance(node, parser.Node_refType)
                and isinstance(parent, parser.Node_compounddefType)
                and parent.kind.value == kind
                and nstack.tag == "innerclass"
                and node.prot == parser.DoxProtectionKind.public
            )

        return filter

    @classmethod
    def create_index_filter(cls, options: Mapping[str, Any]) -> DoxFilter:
        outline_filter = cls.create_outline_filter(options)

        def filter(nstack: NodeStack) -> bool:
            if not outline_filter(nstack):
                return False

            node = nstack.node
            parent = nstack.parent
            return not (
                isinstance(parent, parser.Node_compounddefType)
                and (
                    (
                        isinstance(node, parser.Node_refType)
                        and nstack.tag in ("innerclass", "innernamespace")
                    )
                    or (
                        parent.kind == parser.DoxCompoundKind.group
                        and isinstance(node, parser.Node_sectiondefType)
                        and node.kind == parser.DoxSectionKind.func
                    )
                )
            )

        return filter

    @staticmethod
    def create_file_finder_filter(filename: str) -> DoxFilter:
        def filter(nstack: NodeStack) -> bool:
            node = nstack.node
            return (
                isinstance(node, parser.Node_compounddefType)
                and node.kind == parser.DoxCompoundKind.file
                and location_matches(node.location, filename)
            )

        return filter

    def create_member_finder_filter(
        self, namespace: str, name: str, kinds: Container[parser.MemberKind] | str
    ) -> DoxFilter:
        """Returns a filter which looks for a member with the specified name and kind."""

        if isinstance(kinds, str):
            kinds = (parser.MemberKind(kinds),)

        def node_matches(nstack: NodeStack) -> bool:
            node = nstack.node
            return (
                isinstance(node, parser.Node_MemberType)
                and node.kind in kinds
                and node.name == name
            )

        if namespace:

            def filter(nstack: NodeStack) -> bool:
                parent = nstack.parent
                return (
                    node_matches(nstack)
                    and isinstance(parent, parser.Node_CompoundType)
                    and parent.kind
                    in {
                        parser.CompoundKind.namespace,
                        parser.CompoundKind.class_,
                        parser.CompoundKind.struct,
                        parser.CompoundKind.interface,
                    }
                    and parent.name == namespace
                )

        else:
            ext = self.app.config.breathe_implementation_filename_extensions

            def filter(nstack: NodeStack) -> bool:
                parent = nstack.parent
                return isinstance(parent, parser.Node_CompoundType) and (
                    parent.kind != parser.CompoundKind.file or parent.name.endswith(ext)
                )

        return filter

    def create_function_and_all_friend_finder_filter(self, namespace: str, name: str) -> DoxFilter:
        fun_finder = self.create_member_finder_filter(
            namespace, name, (parser.MemberKind.function, parser.MemberKind.friend)
        )

        # Get matching functions but only ones where the parent is not a group.
        # We want to skip function entries in groups as we'll find the same
        # functions in a file's xml output elsewhere and having more than one
        # match is confusing for our logic later on.
        def filter(nstack: NodeStack) -> bool:
            if not fun_finder(nstack):
                return False

            parent = nstack.parent
            return not (
                isinstance(parent, parser.Node_CompoundType)
                and parent.kind == parser.CompoundKind.group
            )

        return filter

    @staticmethod
    def create_enumvalue_finder_filter(name: str) -> DoxFilter:
        """Returns a filter which looks for an enumvalue with the specified name."""

        def filter(nstack: NodeStack):
            node = nstack.node
            return isinstance(node, parser.Node_enumvalueType) and node.name == name

        return filter

    @staticmethod
    def create_compound_finder_filter(name: str, kind: str) -> DoxFilter:
        """Returns a filter which looks for a compound with the specified name and kind."""

        def filter(nstack: NodeStack):
            node = nstack.node
            return (
                isinstance(node, parser.Node_CompoundType)
                and node.kind.value == kind
                and node.name == name
            )

        return filter

    @classmethod
    def create_finder_filter(
        cls, kind: Literal["group", "page", "namespace"], name: str
    ) -> DoxFilter:
        """Returns a filter which looks for the compound node from the index which is a group node
        (kind=group) and has the appropriate name

        The compound node should reference the group file which we can parse for the group
        contents.
        """
        return cls.create_compound_finder_filter(name, kind)
