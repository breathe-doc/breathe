from breathe.directives.setup import setup as directive_setup
from breathe.file_state_cache import setup as file_state_cache_setup
from breathe.renderer.sphinxrenderer import setup as renderer_setup

from sphinx.application import Sphinx

# Keep in sync with setup.py __version__
__version__ = "4.34.0"


def setup(app: Sphinx):
    directive_setup(app)
    file_state_cache_setup(app)
    renderer_setup(app)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
