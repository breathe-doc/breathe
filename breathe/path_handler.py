from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def includes_directory(file_path: str):
    # Check for backslash or forward slash as we don't know what platform we're on and sometimes
    # the doxygen paths will have forward slash even on Windows.
    return bool(str(file_path).count("\\")) or bool(str(file_path).count("/"))


def resolve_path(app: Sphinx, directory: str, filename: str):
    """Returns a full path to the filename in the given directory assuming that if the directory
    path is relative, then it is relative to the conf.py directory.
    """

    return Path(app.confdir, directory, filename).resolve()
