from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def includes_directory(file_path: str):
    # Check for backslash or forward slash as we don't know what platform we're on and sometimes
    # the doxygen paths will have forward slash even on Windows.
    return bool(str(file_path).count("\\")) or bool(str(file_path).count("/"))


@lru_cache(maxsize=2048)
def _resolved_path(confdir: str, dir: str, filename: str) -> Path:
    """Memoized version of Path.resolve() to avoid redundant filesystem operations.

    Args:
        confdir: Path to the conf.py directory
        dir: Subdirectory inside it
        filename: Filename in the directory

    Returns:
        Resolved Path object
    """
    return Path(confdir, dir, filename).resolve()


def resolve_path(app: Sphinx, directory: str, filename: str) -> Path:
    """Returns a full path to the filename in the given directory assuming that if the directory
    path is relative, then it is relative to the conf.py directory.
    """

    return _resolved_path(app.confdir, directory, filename)
