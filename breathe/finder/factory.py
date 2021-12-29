from breathe.finder import ItemFinder
from breathe.finder import index as indexfinder
from breathe.finder import compound as compoundfinder
from breathe.parser import DoxygenParserFactory
from breathe.project import ProjectInfo
from breathe.renderer.filter import Filter

from sphinx.application import Sphinx

from typing import Dict, Type


class _CreateCompoundTypeSubFinder:
    def __init__(self, app: Sphinx, parser_factory: DoxygenParserFactory):
        self.app = app
        self.parser_factory = parser_factory

    def __call__(self, project_info: ProjectInfo, *args):
        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexfinder.CompoundTypeSubItemFinder(self.app, compound_parser, project_info, *args)


class DoxygenItemFinderFactory:
    def __init__(self, finders: Dict[str, Type[ItemFinder]], project_info: ProjectInfo):
        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object) -> ItemFinder:
        return self.finders[data_object.node_type](self.project_info, data_object, self)


class _FakeParentNode:
    node_type = "fakeparent"


class Finder:
    def __init__(self, root, item_finder_factory: DoxygenItemFinderFactory) -> None:
        self._root = root
        self.item_finder_factory = item_finder_factory

    def filter_(self, filter_: Filter, matches) -> None:
        """Adds all nodes which match the filter into the matches list"""

        item_finder = self.item_finder_factory.create_finder(self._root)
        item_finder.filter_([_FakeParentNode()], filter_, matches)

    def root(self):
        return self._root


class FinderFactory:
    def __init__(self, app: Sphinx, parser_factory: DoxygenParserFactory):
        self.app = app
        self.parser_factory = parser_factory
        self.parser = parser_factory.create_index_parser()

    def create_finder(self, project_info: ProjectInfo) -> Finder:
        root = self.parser.parse(project_info)
        return self.create_finder_from_root(root, project_info)

    def create_finder_from_root(self, root, project_info: ProjectInfo) -> Finder:
        finders: Dict[str, Type[ItemFinder]] = {
            "doxygen": indexfinder.DoxygenTypeSubItemFinder,
            "compound": _CreateCompoundTypeSubFinder(self.app, self.parser_factory),  # type: ignore
            "member": indexfinder.MemberTypeSubItemFinder,
            "doxygendef": compoundfinder.DoxygenTypeSubItemFinder,
            "compounddef": compoundfinder.CompoundDefTypeSubItemFinder,
            "sectiondef": compoundfinder.SectionDefTypeSubItemFinder,
            "memberdef": compoundfinder.MemberDefTypeSubItemFinder,
            "ref": compoundfinder.RefTypeSubItemFinder,
        }
        item_finder_factory = DoxygenItemFinderFactory(finders, project_info)
        return Finder(root, item_finder_factory)
