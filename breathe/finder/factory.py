from __future__ import annotations

from breathe.finder import ItemFinder
from breathe.finder import index as indexfinder
from breathe.finder import compound as compoundfinder
from breathe import parser
from breathe.project import ProjectInfo
from breathe.renderer import TaggedNode

from sphinx.application import Sphinx

from typing import Callable, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter
    ItemFinderCreator = Callable[[ProjectInfo,TaggedNode,'DoxygenItemFinderFactory'],ItemFinder]

    FinderRoot = Union[
        parser.Node_DoxygenTypeIndex,
        parser.Node_CompoundType,
        parser.Node_MemberType,
        parser.Node_DoxygenType,
        parser.Node_compounddefType,
        parser.Node_sectiondefType,
        parser.Node_memberdefType,
        parser.Node_refType]


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

    def create_finder(self, data_object: parser.NodeOrValue, tag: str | None = None) -> ItemFinder:
        return self.finders[type(data_object)](self.project_info, TaggedNode(tag, data_object), self)


class Finder:
    def __init__(self, root, item_finder_factory: DoxygenItemFinderFactory) -> None:
        self._root = root
        self.item_finder_factory = item_finder_factory

    def filter_(self, filter_: DoxFilter, matches: list[list[TaggedNode]]) -> None:
        """Adds all nodes which match the filter into the matches list"""

        item_finder = self.item_finder_factory.create_finder(self._root)
        item_finder.filter_([], filter_, matches)

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

    def create_finder_from_root(self, root: FinderRoot, project_info: ProjectInfo) -> Finder:
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
