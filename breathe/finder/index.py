from __future__ import annotations

from breathe.finder import ItemFinder
from breathe.renderer.filter import FilterFactory, NodeStack
from breathe import parser
from breathe.renderer import TaggedNode

from sphinx.application import Sphinx

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter


class DoxygenTypeSubItemFinder(ItemFinder[parser.Node_DoxygenTypeIndex]):
    def filter_(self, ancestors, filter_: DoxFilter, matches) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        compounds = self.node.value.compound
        node_stack = [self.node] + ancestors
        for compound in compounds:
            compound_finder = self.item_finder_factory.create_finder(compound)
            compound_finder.filter_(node_stack, filter_, matches)


class CompoundTypeSubItemFinder(ItemFinder[parser.Node_CompoundType]):
    def __init__(self, app: Sphinx, compound_parser: parser.DoxygenCompoundParser, *args):
        super().__init__(*args)

        self.filter_factory = FilterFactory(app)
        self.compound_parser = compound_parser

    def filter_(self, ancestors: list[TaggedNode], filter_: DoxFilter, matches) -> None:
        """Finds nodes which match the filter and continues checks to children

        Requires parsing the xml files referenced by the children for which we use the compound
        parser and continue at the top level of that pretending that this node is the parent of the
        top level node of the compound file.
        """

        node_stack = [self.node] + ancestors

        # Match against compound object
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)

        # Descend to member children
        members = self.node.value.member

        member_matches: list[list[TaggedNode]] = []
        for member in members:
            member_finder = self.item_finder_factory.create_finder(member)
            member_finder.filter_(node_stack, filter_, member_matches)

        # If there are members in this compound that match the criteria
        # then load up the file for this compound and get the member data objects
        if member_matches:
            file_data = self.compound_parser.parse(self.node.value.refid)
            finder = self.item_finder_factory.create_finder(file_data)

            for member_stack in member_matches:
                mem = member_stack[0].value
                assert isinstance(mem, parser.Node_MemberType)
                refid = mem.refid
                def ref_filter(nstack):
                    node = nstack.node
                    return isinstance(node,parser.Node_memberdefType) and node.id == refid

                finder.filter_(node_stack, ref_filter, matches)
        else:
            # Read in the xml file referenced by the compound and descend into that as well
            file_data = self.compound_parser.parse(self.node.value.refid)
            finder = self.item_finder_factory.create_finder(file_data)
            finder.filter_(node_stack, filter_, matches)


class MemberTypeSubItemFinder(ItemFinder[parser.Node_memberdefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches) -> None:
        node_stack = [self.node] + ancestors

        # Match against member object
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)
