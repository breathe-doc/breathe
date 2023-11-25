from __future__ import annotations

from typing import Generic, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from breathe.project import ProjectInfo
    from breathe.finder.factory import DoxygenItemFinderFactory
    from breathe.renderer.filter import Filter
    from breathe.renderer import TaggedNode

T = TypeVar('T', covariant=True)


class ItemFinder(Generic[T]):
    def __init__(self, project_info: ProjectInfo, data_object: T, item_finder_factory: DoxygenItemFinderFactory):
        self.data_object = data_object
        self.item_finder_factory: DoxygenItemFinderFactory = item_finder_factory
        self.project_info = project_info

    def filter_(self, ancestors: list[TaggedNode], filter_: Filter, matches: list[list[TaggedNode]]) -> None:
        raise NotImplementedError
