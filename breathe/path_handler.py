from sphinx.application import Sphinx

import os


def includes_directory(file_path: str):
    # Check for backslash or forward slash as we don't know what platform we're on and sometimes
    # the doxygen paths will have forward slash even on Windows.
    return bool(file_path.count('\\')) or bool(file_path.count('/'))


def resolve_path(app: Sphinx, directory: str, filename: str):
    """Returns a full path to the filename in the given directory assuming that if the directory
    path is relative, then it is relative to the conf.py directory.
    """

    # os.path.join does the appropriate handling if _project_path is an absolute path
    return os.path.join(app.confdir, directory, filename)
