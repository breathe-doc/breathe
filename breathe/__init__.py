from breathe.directives.setup import setup as directive_setup
from breathe.file_state_cache import setup as file_state_cache_setup
from breathe.renderer.sphinxrenderer import setup as renderer_setup

from sphinx.application import Sphinx

try:
    from importlib.metadata import version
except ImportError:  # for python v3.7 or older
    from importlib_metadata import version  # type: ignore


def setup(app: Sphinx):
    directive_setup(app)
    file_state_cache_setup(app)
    renderer_setup(app)

    return {"version": version("breathe"), "parallel_read_safe": True, "parallel_write_safe": True}
