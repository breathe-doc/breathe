from __future__ import annotations

from typing import Generic, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from breathe.project import ProjectInfo
    from breathe.finder.factory import DoxygenItemFinderFactory
    from breathe.renderer.filter import DoxFilter
    from breathe.renderer import TaggedNode, T_data_object
else:
    T_data_object = TypeVar("T_data_object", covariant=True)


class ItemFinder(Generic[T_data_object]):
    def __init__(
        self,
        project_info: ProjectInfo,
        node: TaggedNode[T_data_object],
        item_finder_factory: DoxygenItemFinderFactory,
    ):
        self.node = node
        self.item_finder_factory: DoxygenItemFinderFactory = item_finder_factory
        self.project_info = project_info

    def filter_(
        self, ancestors: list[TaggedNode], filter_: DoxFilter, matches: list[list[TaggedNode]]
    ) -> None:
        raise NotImplementedError
