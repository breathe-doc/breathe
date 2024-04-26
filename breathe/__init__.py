from sphinx.application import Sphinx

# Keep in sync with pyproject.toml "version"
__version__ = "4.35.0"


def setup(app: Sphinx):
    from breathe.directives.setup import setup as directive_setup
    from breathe.file_state_cache import setup as file_state_cache_setup
    from breathe.renderer.sphinxrenderer import setup as renderer_setup

    directive_setup(app)
    file_state_cache_setup(app)
    renderer_setup(app)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
