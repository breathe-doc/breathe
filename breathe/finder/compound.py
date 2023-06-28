from breathe.finder import ItemFinder, stack
from breathe.parser.compound import compounddefTypeSub
from breathe.renderer.filter import Filter, FilterFactory
from breathe.parser import DoxygenCompoundParser

from sphinx.application import Sphinx

from typing import Any, List


class DoxygenTypeSubItemFinder(ItemFinder):
    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)
        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef)
        compound_finder.filter_(node_stack, filter_, matches)


class CompoundDefTypeSubItemFinder(ItemFinder):
    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        """Finds nodes which match the filter and continues checks to children"""

        node_stack = stack(self.data_object, ancestors)
        if filter_.allow(node_stack):
            matches.append(node_stack)

        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            finder.filter_(node_stack, filter_, matches)

        for innerclass in self.data_object.innerclass:
            finder = self.item_finder_factory.create_finder(innerclass)
            finder.filter_(node_stack, filter_, matches)


class SectionDefTypeSubItemFinder(ItemFinder):
    def __init__(self, app: Sphinx, compound_parser: DoxygenCompoundParser, *args):
        super().__init__(*args)

        self.filter_factory = FilterFactory(app)
        self.compound_parser = compound_parser

    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)
        if filter_.allow(node_stack):
            matches.append(node_stack)

        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            finder.filter_(node_stack, filter_, matches)

        # Descend to member children (Doxygen 1.9.7 or newer)
        members = self.data_object.get_member()
        # TODO: find a more precise type for the Doxygen nodes
        member_matches: List[Any] = []
        for member in members:
            member_finder = self.item_finder_factory.create_finder(member)
            member_finder.filter_(node_stack, filter_, member_matches)

        # If there are members in this sectiondef that match the criteria
        # then load up the file for the group they're in and get the member data objects
        if member_matches:
            matched_member_ids = (member.id for stack in matches for member in stack)
            member_refid = member_matches[0][0].refid
            filename = member_refid.rsplit('_', 1)[0]
            file_data = self.compound_parser.parse(filename)
            finder = self.item_finder_factory.create_finder(file_data)
            for member_stack in member_matches:
                member = member_stack[0]
                if member.refid not in matched_member_ids:
                    ref_filter = self.filter_factory.create_id_filter(
                        "memberdef", member.refid
                    )
                    finder.filter_(node_stack, ref_filter, matches)


class MemberDefTypeSubItemFinder(ItemFinder):
    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        data_object = self.data_object
        node_stack = stack(data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(node_stack)

        if data_object.kind == "enum":
            for value in data_object.enumvalue:
                value_stack = stack(value, node_stack)
                if filter_.allow(value_stack):
                    matches.append(value_stack)


class RefTypeSubItemFinder(ItemFinder):
    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        node_stack = stack(self.data_object, ancestors)
        if filter_.allow(node_stack):
            matches.append(node_stack)
