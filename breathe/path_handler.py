from __future__ import annotations

from functools import cache
from pathlib import Path


def includes_directory(file_path: str):
    # Check for backslash or forward slash as we don't know what platform we're on and sometimes
    # the doxygen paths will have forward slash even on Windows.
    return bool(str(file_path).count("\\")) or bool(str(file_path).count("/"))


@cache
def resolve_path(confdir: str, directory: str, filename: str) -> Path:
    """Returns a full path to the filename in the given directory assuming that if the directory
    path is relative, then it is relative to the conf.py directory.
    It is memoized to avoid redundant filesystem operations.

    Args:
        confdir: Path to the conf.py directory
        dir: Subdirectory inside it
        filename: Filename in the directory

    Returns:
        Resolved Path object
    """
    return Path(confdir, directory, filename).resolve()
