from . import directives
from . import file_state_cache
from .renderer import sphinxrenderer

from sphinx.application import Sphinx

__version__ = '4.20.0'


def setup(app: Sphinx):
    directives.setup(app)
    file_state_cache.setup(app)
    sphinxrenderer.setup(app)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
