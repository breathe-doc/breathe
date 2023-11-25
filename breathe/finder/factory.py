from __future__ import annotations

from breathe.finder import ItemFinder
from breathe.finder import index as indexfinder
from breathe.finder import compound as compoundfinder
from breathe import parser
from breathe.project import ProjectInfo
from breathe.renderer import FakeParentNode, TaggedNode
from breathe.renderer.filter import Filter

from sphinx.application import Sphinx

from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    ItemFinderCreator = Callable[[ProjectInfo,Any,'DoxygenItemFinderFactory'],ItemFinder]


class _CreateCompoundTypeSubFinder:
    def __init__(self, app: Sphinx, parser_factory: parser.DoxygenParserFactory):
        self.app = app
        self.parser_factory = parser_factory

    def __call__(self, project_info: ProjectInfo, *args) -> indexfinder.CompoundTypeSubItemFinder:
        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexfinder.CompoundTypeSubItemFinder(self.app, compound_parser, project_info, *args)


class DoxygenItemFinderFactory:
    def __init__(self, finders: dict[type[parser.NodeOrValue], ItemFinderCreator], project_info: ProjectInfo):
        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object) -> ItemFinder:
        return self.finders[type(data_object)](self.project_info, data_object, self)


class Finder:
    def __init__(self, root, item_finder_factory: DoxygenItemFinderFactory) -> None:
        self._root = root
        self.item_finder_factory = item_finder_factory

    def filter_(self, filter_: Filter, matches: list[list[TaggedNode]]) -> None:
        """Adds all nodes which match the filter into the matches list"""

        item_finder = self.item_finder_factory.create_finder(self._root)
        item_finder.filter_([TaggedNode(None,FakeParentNode())], filter_, matches)

    def root(self):
        return self._root


class FinderFactory:
    def __init__(self, app: Sphinx, parser_factory: parser.DoxygenParserFactory):
        self.app = app
        self.parser_factory = parser_factory
        self.parser = parser_factory.create_index_parser()

    def create_finder(self, project_info: ProjectInfo) -> Finder:
        root = self.parser.parse(project_info)
        return self.create_finder_from_root(root, project_info)

    def create_finder_from_root(self, root, project_info: ProjectInfo) -> Finder:
        finders: dict[type[parser.NodeOrValue], ItemFinderCreator] = {
            parser.Node_DoxygenTypeIndex: indexfinder.DoxygenTypeSubItemFinder,
            parser.Node_CompoundType: _CreateCompoundTypeSubFinder(self.app, self.parser_factory),
            parser.Node_MemberType: indexfinder.MemberTypeSubItemFinder,
            parser.Node_DoxygenType: compoundfinder.DoxygenTypeSubItemFinder,
            parser.Node_compounddefType: compoundfinder.CompoundDefTypeSubItemFinder,
            parser.Node_sectiondefType: compoundfinder.SectionDefTypeSubItemFinder,
            parser.Node_memberdefType: compoundfinder.MemberDefTypeSubItemFinder,
            parser.Node_refType: compoundfinder.RefTypeSubItemFinder,
        }
        item_finder_factory = DoxygenItemFinderFactory(finders, project_info)
        return Finder(root, item_finder_factory)
