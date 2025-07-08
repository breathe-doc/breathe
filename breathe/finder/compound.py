from __future__ import annotations

from typing import TYPE_CHECKING

from breathe import parser
from breathe.finder import ItemFinder
from breathe.renderer import TaggedNode
from breathe.renderer.filter import NodeStack

if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter, FinderMatch


class DoxygenTypeSubItemFinder(ItemFinder[parser.Node_DoxygenType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = [self.node] + ancestors
        assert len(self.node.value.compounddef) == 1
        self.run_filter(filter_, matches, node_stack, self.node.value.compounddef[0])


class CompoundDefTypeSubItemFinder(ItemFinder[parser.Node_compounddefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        """Finds nodes which match the filter and continues checks to children"""

        node_stack = [self.node] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        for sectiondef in self.node.value.sectiondef:
            self.run_filter(filter_, matches, node_stack, sectiondef)

        for innerclass in self.node.value.innerclass:
            self.run_filter(filter_, matches, node_stack, innerclass, "innerclass")


class SectionDefTypeSubItemFinder(ItemFinder[parser.Node_sectiondefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = [self.node] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        for memberdef in self.node.value.memberdef:
            self.run_filter(filter_, matches, node_stack, memberdef)

        for member in self.node.value.member:
            self.run_filter(filter_, matches, node_stack, member)


class MemberDefTypeSubItemFinder(ItemFinder[parser.Node_memberdefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        data_object = self.node.value
        node_stack = [self.node] + ancestors

        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        if data_object.kind == parser.DoxMemberKind.enum:
            for value in data_object.enumvalue:
                value_stack = [TaggedNode("enumvalue", value)] + node_stack
                if filter_(NodeStack(value_stack)):
                    matches.append(value_stack)


class RefTypeSubItemFinder(ItemFinder[parser.Node_refType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        node_stack = [self.node] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)
