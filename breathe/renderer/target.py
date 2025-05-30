from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.nodes import make_id

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from typing import Any, Callable

    from docutils.nodes import Element
    from sphinx.environment import BuildEnvironment

    TargetHandler = Callable[[nodes.document, str], Sequence[Element]]


class _RealTargetHandler:
    def __init__(self, env: BuildEnvironment):
        self.env = env

    def __call__(self, document: nodes.document, refid: str) -> list[Element]:
        """Creates a target node, registers it with the document and returns it in a list"""

        if refid in document.ids:
            # Sphinx will already warn about a duplicate declaration so we don't
            # need any warnings here
            refid = make_id(self.env, document)

        target = nodes.target(ids=[refid], names=[refid])
        document.note_explicit_target(target)

        return [target]


def create_target_handler(options: Mapping[str, Any], env: BuildEnvironment) -> TargetHandler:
    if "no-link" in options:
        return lambda document, refid: []
    return _RealTargetHandler(env)
