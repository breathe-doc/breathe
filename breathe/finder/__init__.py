from __future__ import annotations

from typing import Generic, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from breathe.project import ProjectInfo
    from breathe.finder.factory import DoxygenItemFinderFactory
    from breathe.renderer.filter import Filter

T = TypeVar('T')

def stack(element, list_):
    """Stack an element on to the start of a list and return as a new list"""

    # Copy list first so we have a new list to insert into
    output = list_[:]
    output.insert(0, element)
    return output


class ItemFinder(Generic[T]):
    def __init__(self, project_info: ProjectInfo, data_object: T, item_finder_factory: DoxygenItemFinderFactory):
        self.data_object = data_object
        self.item_finder_factory: DoxygenItemFinderFactory = item_finder_factory
        self.project_info = project_info

    def filter_(self, ancestors, filter_: Filter, matches) -> None:
        raise NotImplementedError
