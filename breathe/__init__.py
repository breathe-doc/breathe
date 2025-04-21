<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

from breathe.directives.setup import setup as directive_setup
from breathe.file_state_cache import setup as file_state_cache_setup
from breathe.renderer.sphinxrenderer import setup as renderer_setup

if TYPE_CHECKING:
    from sphinx.application import Sphinx
||||||| 542ae9b
from breathe.directives.setup import setup as directive_setup
from breathe.file_state_cache import setup as file_state_cache_setup
from breathe.renderer.sphinxrenderer import setup as renderer_setup

from sphinx.application import Sphinx
=======
from sphinx.application import Sphinx
>>>>>>> memberdef-in-groups

<<<<<<< HEAD
__version__ = "4.36.0"
||||||| 542ae9b
# Keep in sync with setup.py __version__
__version__ = "4.35.0"
=======
# Keep in sync with pyproject.toml "version"
__version__ = "4.35.0"
>>>>>>> memberdef-in-groups


def setup(app: Sphinx):
    from breathe.directives.setup import setup as directive_setup
    from breathe.file_state_cache import setup as file_state_cache_setup
    from breathe.renderer.sphinxrenderer import setup as renderer_setup

    directive_setup(app)
    file_state_cache_setup(app)
    renderer_setup(app)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
