<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

||||||| 542ae9b
from breathe.finder import ItemFinder
from breathe.finder import index as indexfinder
=======
from __future__ import annotations

from breathe.finder import index as indexfinder
>>>>>>> memberdef-in-groups
from breathe.finder import compound as compoundfinder
<<<<<<< HEAD
from breathe.finder import index as indexfinder
||||||| 542ae9b
from breathe.parser import DoxygenParserFactory
from breathe.project import ProjectInfo
from breathe.renderer.filter import Filter
=======
from breathe import parser
from breathe.renderer import TaggedNode
>>>>>>> memberdef-in-groups

<<<<<<< HEAD
if TYPE_CHECKING:
    from sphinx.application import Sphinx
||||||| 542ae9b
from sphinx.application import Sphinx
=======
from typing import Callable, TYPE_CHECKING, Union
>>>>>>> memberdef-in-groups

<<<<<<< HEAD
    from breathe.finder import ItemFinder
    from breathe.parser import DoxygenParserFactory
    from breathe.project import ProjectInfo
    from breathe.renderer.filter import Filter
||||||| 542ae9b
from typing import Dict, Type
=======
if TYPE_CHECKING:
    from breathe.renderer.filter import DoxFilter, FinderMatch
    from breathe.project import ProjectInfo
    from breathe.finder import ItemFinder
    from sphinx.application import Sphinx

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
>>>>>>> memberdef-in-groups


class _CreateCompoundTypeSubFinder:
    def __init__(self, app: Sphinx, dox_parser: parser.DoxygenParser):
        self.app = app
        self.dox_parser = dox_parser

    def __call__(self, project_info: ProjectInfo, *args) -> indexfinder.CompoundTypeSubItemFinder:
        return indexfinder.CompoundTypeSubItemFinder(self.app, self.dox_parser, project_info, *args)


<<<<<<< HEAD
class DoxygenItemFinderFactory:
    def __init__(self, finders: dict[str, type[ItemFinder]], project_info: ProjectInfo):
        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object) -> ItemFinder:
        return self.finders[data_object.node_type](self.project_info, data_object, self)


class _FakeParentNode:
    node_type = "fakeparent"
||||||| 542ae9b
class DoxygenItemFinderFactory:
    def __init__(self, finders: Dict[str, Type[ItemFinder]], project_info: ProjectInfo):
        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object) -> ItemFinder:
        return self.finders[data_object.node_type](self.project_info, data_object, self)


class _FakeParentNode:
    node_type = "fakeparent"
=======
def create_item_finder(
    finders: dict[type[parser.NodeOrValue], ItemFinderCreator],
    project_info: ProjectInfo,
    data_object: parser.NodeOrValue,
    tag: str | None = None,
) -> ItemFinder:
    return finders[type(data_object)](project_info, TaggedNode(tag, data_object), finders)
>>>>>>> memberdef-in-groups


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

<<<<<<< HEAD
    def create_finder(self, project_info: ProjectInfo) -> Finder:
        root = self.parser.parse(project_info)
        return self.create_finder_from_root(root, project_info)

    def create_finder_from_root(self, root, project_info: ProjectInfo) -> Finder:
        finders: dict[str, type[ItemFinder]] = {
            "doxygen": indexfinder.DoxygenTypeSubItemFinder,
            "compound": _CreateCompoundTypeSubFinder(self.app, self.parser_factory),  # type: ignore[dict-item]
            "member": indexfinder.MemberTypeSubItemFinder,
            "doxygendef": compoundfinder.DoxygenTypeSubItemFinder,
            "compounddef": compoundfinder.CompoundDefTypeSubItemFinder,
            "sectiondef": compoundfinder.SectionDefTypeSubItemFinder,
            "memberdef": compoundfinder.MemberDefTypeSubItemFinder,
            "ref": compoundfinder.RefTypeSubItemFinder,
        }
        item_finder_factory = DoxygenItemFinderFactory(finders, project_info)
        return Finder(root, item_finder_factory)
||||||| 542ae9b
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
=======
    return Finder(root, project_info, finders)
>>>>>>> memberdef-in-groups
