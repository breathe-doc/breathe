from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from breathe import parser
    from breathe.finder.factory import FinderCreatorMap
    from breathe.project import ProjectInfo
    from breathe.renderer import T_data_object, TaggedNode
    from breathe.renderer.filter import DoxFilter, FinderMatch
else:
    T_data_object = TypeVar("T_data_object", covariant=True)


class ItemFinder(Generic[T_data_object]):
    def __init__(
        self,
        project_info: ProjectInfo,
        node: TaggedNode[T_data_object],
        finders: FinderCreatorMap,
    ):
        self.node = node
        self.finders: FinderCreatorMap = finders
        self.project_info = project_info

    def run_filter(
        self,
        filter_: DoxFilter,
        matches: list[FinderMatch],
        node_stack: list[TaggedNode],
        item: parser.NodeOrValue,
        tag: str | None = None,
    ) -> None:
        """Adds all nodes which match the filter into the matches list"""

        item_finder = factory.create_item_finder(self.finders, self.project_info, item, tag)
        item_finder.filter_(node_stack, filter_, matches)

    def filter_(
        self, ancestors: list[TaggedNode], filter_: DoxFilter, matches: list[FinderMatch]
    ) -> None:
        raise NotImplementedError


# ItemFinder needs to be defined before we can import any submodules
from breathe.finder import factory  # noqa: E402
