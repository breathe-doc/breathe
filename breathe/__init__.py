from . import directives
from . import file_state_cache

from sphinx.application import Sphinx

__version__ = '4.18.1'


def setup(app: Sphinx):
    directives.setup(app)
    file_state_cache.setup(app)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
