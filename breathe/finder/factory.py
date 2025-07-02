from __future__ import annotations

from typing import TYPE_CHECKING

from breathe import parser
from breathe.finder import compound as compoundfinder
from breathe.finder import index as indexfinder
from breathe.renderer import TaggedNode

if TYPE_CHECKING:
    from typing import Callable, Union

    from sphinx.application import Sphinx

    from breathe.finder import ItemFinder
    from breathe.project import ProjectInfo
    from breathe.renderer.filter import DoxFilter, FinderMatch

    ItemFinderCreator = Callable[[ProjectInfo, TaggedNode, "FinderCreatorMap"], ItemFinder]
    FinderCreatorMap = dict[type[parser.NodeOrValue], ItemFinderCreator]

    FinderRoot = Union[
        parser.Node_CompoundType,
        parser.Node_MemberType,
        parser.Node_DoxygenType,
        parser.Node_compounddefType,
        parser.Node_sectiondefType,
        parser.Node_memberdefType,
        parser.Node_refType,
    ]


class _CreateCompoundTypeSubFinder:
    def __init__(self, app: Sphinx, dox_parser: parser.DoxygenParser):
        self.app = app
        self.dox_parser = dox_parser

    def __call__(self, project_info: ProjectInfo, *args) -> indexfinder.CompoundTypeSubItemFinder:
        return indexfinder.CompoundTypeSubItemFinder(self.app, self.dox_parser, project_info, *args)


def create_item_finder(
    finders: dict[type[parser.NodeOrValue], ItemFinderCreator],
    project_info: ProjectInfo,
    data_object: parser.NodeOrValue,
    tag: str | None = None,
) -> ItemFinder:
    return finders[type(data_object)](project_info, TaggedNode(tag, data_object), finders)


class Finder:
    def __init__(
        self, root: parser.NodeOrValue, project_info: ProjectInfo, finders: FinderCreatorMap
    ):
        self._root = root
        self.project_info = project_info
        self.finders = finders

    def filter_(self, filter_: DoxFilter, matches: list[FinderMatch]) -> None:
        """Adds all nodes which match the filter into the matches list"""

        item_finder = create_item_finder(self.finders, self.project_info, self._root)
        item_finder.filter_([], filter_, matches)

    def root(self):
        return self._root


def create_finder_from_root(
    app: Sphinx, dox_parser: parser.DoxygenParser, root: FinderRoot, project_info: ProjectInfo
) -> Finder:
    finders: FinderCreatorMap = {
        parser.Node_CompoundType: _CreateCompoundTypeSubFinder(app, dox_parser),
        parser.Node_MemberType: indexfinder.MemberTypeSubItemFinder,
        parser.Node_DoxygenType: compoundfinder.DoxygenTypeSubItemFinder,
        parser.Node_compounddefType: compoundfinder.CompoundDefTypeSubItemFinder,
        parser.Node_sectiondefType: compoundfinder.SectionDefTypeSubItemFinder,
        parser.Node_memberdefType: compoundfinder.MemberDefTypeSubItemFinder,
        parser.Node_refType: compoundfinder.RefTypeSubItemFinder,
    }

    return Finder(root, project_info, finders)
