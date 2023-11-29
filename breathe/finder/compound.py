from __future__ import annotations

from breathe.finder import ItemFinder
from breathe.renderer.filter import NodeStack
from breathe import parser
from breathe.renderer import TaggedNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter


class DoxygenTypeSubItemFinder(ItemFinder[parser.Node_DoxygenType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = [TaggedNode(None,self.data_object)] + ancestors
        assert len(self.data_object.compounddef) == 1
        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef[0])
        compound_finder.filter_(node_stack, filter_, matches)


class CompoundDefTypeSubItemFinder(ItemFinder[parser.Node_compounddefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        """Finds nodes which match the filter and continues checks to children"""

        node_stack = [TaggedNode(None,self.data_object)] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            finder.filter_(node_stack, filter_, matches)

        for innerclass in self.data_object.innerclass:
            finder = self.item_finder_factory.create_finder(innerclass)
            finder.filter_(node_stack, filter_, matches)


class SectionDefTypeSubItemFinder(ItemFinder[parser.Node_sectiondefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = [TaggedNode(None,self.data_object)] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            finder.filter_(node_stack, filter_, matches)


class MemberDefTypeSubItemFinder(ItemFinder[parser.Node_memberdefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        data_object = self.data_object
        node_stack = [TaggedNode(None,self.data_object)] + ancestors

        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        if data_object.kind == parser.DoxMemberKind.enum:
            for value in data_object.enumvalue:
                value_stack = [TaggedNode('enumvalue',value)] + node_stack
                if filter_(NodeStack(value_stack)):
                    matches.append(value_stack)


class RefTypeSubItemFinder(ItemFinder[parser.Node_refType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        node_stack = [TaggedNode(None,self.data_object)] + ancestors
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)
