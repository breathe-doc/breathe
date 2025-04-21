<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

from breathe.finder import ItemFinder, stack
from breathe.renderer.filter import FilterFactory
||||||| 542ae9b
from breathe.finder import ItemFinder, stack
from breathe.renderer.filter import Filter, FilterFactory
from breathe.parser import DoxygenCompoundParser
=======
from __future__ import annotations

from breathe.finder import ItemFinder
from breathe.renderer.filter import NodeStack
from breathe import parser
from breathe.renderer import TaggedNode
>>>>>>> memberdef-in-groups

if TYPE_CHECKING:
    from typing import Any

<<<<<<< HEAD
    from sphinx.application import Sphinx

    from breathe.parser import DoxygenCompoundParser
    from breathe.renderer.filter import Filter
||||||| 542ae9b
from typing import Any, List
=======
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter, FinderMatch
>>>>>>> memberdef-in-groups


class DoxygenTypeSubItemFinder(ItemFinder[parser.Node_DoxygenTypeIndex]):
    def filter_(self, ancestors, filter_: DoxFilter, matches) -> None:
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        compounds = self.node.value.compound
        node_stack = [self.node] + ancestors
        for compound in compounds:
            self.run_filter(filter_, matches, node_stack, compound)


class CompoundTypeSubItemFinder(ItemFinder[parser.Node_CompoundType]):
    def __init__(self, app: Sphinx, dox_parser: parser.DoxygenParser, *args):
        super().__init__(*args)
        self.dox_parser = dox_parser

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
<<<<<<< HEAD
        members = self.data_object.get_member()
        # TODO: find a more precise type for the Doxygen nodes
        member_matches: list[Any] = []
||||||| 542ae9b
        members = self.data_object.get_member()
        # TODO: find a more precise type for the Doxygen nodes
        member_matches: List[Any] = []
=======
        members = self.node.value.member

        member_matches: list[FinderMatch] = []
>>>>>>> memberdef-in-groups
        for member in members:
            self.run_filter(filter_, member_matches, node_stack, member)

        # If there are members in this compound that match the criteria
        # then load up the file for this compound and get the member data objects
        if member_matches:
            file_data = self.dox_parser.parse_compound(
                self.node.value.refid, self.project_info
            ).root

            for member_stack in member_matches:
                mem = member_stack[0].value
                assert isinstance(mem, parser.Node_MemberType)
                refid = mem.refid

                def ref_filter(nstack):
                    node = nstack.node
                    return isinstance(node, parser.Node_memberdefType) and node.id == refid

                self.run_filter(ref_filter, matches, node_stack, file_data)
        else:
            # Read in the xml file referenced by the compound and descend into that as well
            file_data = self.dox_parser.parse_compound(
                self.node.value.refid, self.project_info
            ).root
            self.run_filter(filter_, matches, node_stack, file_data)


class MemberTypeSubItemFinder(ItemFinder[parser.Node_memberdefType]):
    def filter_(self, ancestors, filter_: DoxFilter, matches) -> None:
        node_stack = [self.node] + ancestors

        # Match against member object
        if filter_(NodeStack(node_stack)):
            matches.append(node_stack)
