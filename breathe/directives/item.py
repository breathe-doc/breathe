from __future__ import annotations

from typing import TYPE_CHECKING, cast

from docutils.parsers.rst.directives import flag, unchanged_required

from breathe import parser
from breathe.directives import BaseDirective
from breathe.file_state_cache import MTimeError
from breathe.project import ProjectError
from breathe.renderer import TaggedNode, filter
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.target import create_target_handler

if TYPE_CHECKING:
    import sys
    from typing import ClassVar

    from docutils.nodes import Node

    if sys.version_info >= (3, 11):
        from typing import NotRequired, TypedDict
    else:
        from typing_extensions import NotRequired, TypedDict

    from breathe.project import ProjectInfo, ProjectOptions

    DoxBaseItemOptions = TypedDict(
        "DoxBaseItemOptions",
        {"path": str, "project": str, "outline": NotRequired[None], "no-link": NotRequired[None]},
    )
else:
    DoxBaseItemOptions = None


def enumvalue_finder_filter(
    name: str,
    d_parser: parser.DoxygenParser,
    project_info: ProjectInfo,
    index: parser.DoxygenIndex,
) -> filter.FinderMatchItr:
    """Looks for an enumvalue with the specified name."""

    for m, c in index.members[name]:
        if m.kind != parser.MemberKind.enumvalue:
            continue

        dc = d_parser.parse_compound(c.refid, project_info)
        ev, mdef, sdef, cdef = dc.enumvalue_by_id[m.refid]

        TN = TaggedNode
        yield [
            TN("enumvalue", ev),
            TN("memberdef", mdef),
            TN("sectiondef", sdef),
            TN("compounddef", cdef),
            TN("doxygen", dc.root),
            TN("compound", c),
            TN("doxygenindex", index.root),
        ]


class _DoxygenBaseItemDirective(BaseDirective):
    kind: ClassVar[str]

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
    }
    has_content = False

    def finder_filter(
        self,
        namespace: str,
        name: str,
        project_info: ProjectInfo,
        index: parser.DoxygenIndex,
        matches: list[filter.FinderMatch],
    ) -> None:
        """A filter to find the node corresponding to this item."""

        matches.extend(
            filter.member_finder_filter(
                self.app, namespace, name, self.dox_parser, project_info, self.kind, index
            )
        )

    def run(self) -> list[Node]:
        options = cast("DoxBaseItemOptions", self.options)

        namespace, _, name = self.arguments[0].rpartition("::")

        try:
            project_info = self.project_info_factory.create_project_info(
                cast("ProjectOptions", options)
            )
        except ProjectError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        try:
            d_index = self.get_doxygen_index(project_info)
        except MTimeError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        matches: list[filter.FinderMatch] = []
        self.finder_filter(namespace, name, project_info, d_index, matches)

        if len(matches) == 0:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = self.create_warning(project_info, kind=self.kind, display_name=display_name)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{display_name}" {tail}')

        target_handler = create_target_handler(options, self.env)
        filter_ = filter.create_outline_filter(options)

        node_stack = matches[0]
        mask_factory = NullMaskFactory()
        return self.render(
            node_stack, project_info, filter_, target_handler, mask_factory, self.directive_args
        )


class DoxygenVariableDirective(_DoxygenBaseItemDirective):
    kind = "variable"


class DoxygenDefineDirective(_DoxygenBaseItemDirective):
    kind = "define"


class DoxygenConceptDirective(_DoxygenBaseItemDirective):
    kind = "concept"

    def finder_filter(
        self,
        namespace: str,
        name: str,
        project_info: ProjectInfo,
        index: parser.DoxygenIndex,
        matches: list[filter.FinderMatch],
    ) -> None:
        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        matches.extend(filter.compound_finder_filter(xml_name, "concept", index))


class DoxygenEnumDirective(_DoxygenBaseItemDirective):
    kind = "enum"


class DoxygenEnumValueDirective(_DoxygenBaseItemDirective):
    kind = "enumvalue"

    def finder_filter(
        self,
        namespace: str,
        name: str,
        project_info: ProjectInfo,
        index: parser.DoxygenIndex,
        matches: list[filter.FinderMatch],
    ) -> None:
        for m, c in index.members[name]:
            if m.kind != parser.MemberKind.enumvalue:
                continue

            dc = self.dox_parser.parse_compound(c.refid, project_info)
            ev, mdef, sdef, cdef = dc.enumvalue_by_id[m.refid]

            TN = TaggedNode
            matches.append([
                TN("enumvalue", ev),
                TN("memberdef", mdef),
                TN("sectiondef", sdef),
                TN("compounddef", cdef),
                TN("doxygen", dc.root),
                TN("compound", c),
                TN("doxygenindex", index.root),
            ])


class DoxygenTypedefDirective(_DoxygenBaseItemDirective):
    kind = "typedef"


class DoxygenUnionDirective(_DoxygenBaseItemDirective):
    kind = "union"

    def finder_filter(
        self,
        namespace: str,
        name: str,
        project_info: ProjectInfo,
        index: parser.DoxygenIndex,
        matches: list[filter.FinderMatch],
    ) -> None:
        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        matches.extend(filter.compound_finder_filter(xml_name, "union", index))
