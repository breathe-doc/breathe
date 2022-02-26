from breathe.project import ProjectInfo

from docutils import nodes
from docutils.nodes import Element

from typing import Any, Dict, List, Sequence


class TargetHandler:
    def create_target(self, refid: str) -> Sequence[Element]:
        raise NotImplementedError


class _RealTargetHandler(TargetHandler):
    def __init__(self, project_info: ProjectInfo, document: nodes.document):
        self.project_info = project_info
        self.document = document

    def create_target(self, refid: str) -> List[Element]:
        """Creates a target node and registers it with the document and returns it in a list"""

        target = nodes.target(ids=[refid], names=[refid])
        try:
            self.document.note_explicit_target(target)
        except Exception:
            # TODO: We should really return a docutils warning node here
            print("Warning: Duplicate target detected: %s" % refid)
        return [target]


class _NullTargetHandler(TargetHandler):
    def create_target(self, refid: str) -> List[Element]:
        return []


def create_target_handler(
    options: Dict[str, Any], project_info: ProjectInfo, document: nodes.document
) -> TargetHandler:
    if "no-link" in options:
        return _NullTargetHandler()
    return _RealTargetHandler(project_info, document)
