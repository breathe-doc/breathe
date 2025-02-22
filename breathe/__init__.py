from __future__ import annotations

from typing import TYPE_CHECKING

from breathe.directives.setup import setup as directive_setup
from breathe.file_state_cache import setup as file_state_cache_setup
from breathe.renderer.sphinxrenderer import setup as renderer_setup

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "4.36.0"


def setup(app: Sphinx):
    directive_setup(app)
    file_state_cache_setup(app)
    renderer_setup(app)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
