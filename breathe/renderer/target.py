<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING
||||||| 542ae9b
from breathe.project import ProjectInfo
=======
from __future__ import annotations
>>>>>>> memberdef-in-groups

from docutils import nodes

<<<<<<< HEAD
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from docutils.nodes import Element

    from breathe.project import ProjectInfo
||||||| 542ae9b
from typing import Any, Dict, List, Sequence
=======
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from docutils.nodes import Element
    from breathe.project import ProjectInfo
>>>>>>> memberdef-in-groups


class TargetHandler:
    def create_target(self, refid: str) -> Sequence[Element]:
        raise NotImplementedError


class _RealTargetHandler(TargetHandler):
    def __init__(self, project_info: ProjectInfo, document: nodes.document):
        self.project_info = project_info
        self.document = document

    def create_target(self, refid: str) -> list[Element]:
        """Creates a target node and registers it with the document and returns it in a list"""

        target = nodes.target(ids=[refid], names=[refid])
        try:
            self.document.note_explicit_target(target)
        except Exception:
            # TODO: We should really return a docutils warning node here
            print("Warning: Duplicate target detected: %s" % refid)
        return [target]


class _NullTargetHandler(TargetHandler):
    def create_target(self, refid: str) -> list[Element]:
        return []


def create_target_handler(
<<<<<<< HEAD
    options: dict[str, Any], project_info: ProjectInfo, document: nodes.document
||||||| 542ae9b
    options: Dict[str, Any], project_info: ProjectInfo, document: nodes.document
=======
    options: Mapping[str, Any], project_info: ProjectInfo, document: nodes.document
>>>>>>> memberdef-in-groups
) -> TargetHandler:
    if "no-link" in options:
        return _NullTargetHandler()
    return _RealTargetHandler(project_info, document)
