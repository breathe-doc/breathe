from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

import os
from typing import List, Set

"""
Store the modified time of the various doxygen xml files against the
reStructuredText file that they are referenced from so that we know which
reStructuredText files to rebuild if the doxygen xml is modified.

We store the information in the environment object as 'breathe_file_state'
so that it is pickled down and stored between builds as Sphinx is designed to do.

(mypy doesn't like dynamically added attributes, hence all references to it are ignored)
"""


class MTimeError(Exception):
    pass


def _getmtime(filename: str):
    try:
        return os.path.getmtime(filename)
    except OSError:
        raise MTimeError('Cannot find file: %s' % os.path.realpath(filename))


def update(app: Sphinx, source_file: str) -> None:
    if not hasattr(app.env, "breathe_file_state"):
        app.env.breathe_file_state = {}  # type: ignore

    new_mtime = _getmtime(source_file)
    mtime, docnames = app.env.breathe_file_state.setdefault(  # type: ignore
        source_file, (new_mtime, set()))

    docnames.add(app.env.docname)
    app.env.breathe_file_state[source_file] = (new_mtime, docnames)  # type: ignore


def _get_outdated(app: Sphinx, env: BuildEnvironment,
                  added: Set[str], changed: Set[str], removed: Set[str]) -> List[str]:
    if not hasattr(app.env, "breathe_file_state"):
        return []

    stale = []
    for filename, info in app.env.breathe_file_state.items():  # type: ignore
        old_mtime, docnames = info
        if _getmtime(filename) > old_mtime:
            stale.extend(docnames)
    return list(set(stale).difference(removed))


def _purge_doc(app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    if not hasattr(app.env, "breathe_file_state"):
        return

    toremove = []
    for filename, info in app.env.breathe_file_state.items():  # type: ignore
        _, docnames = info
        docnames.discard(docname)
        if not docnames:
            toremove.append(filename)

    for filename in toremove:
        del app.env.breathe_file_state[filename]  # type: ignore


def setup(app: Sphinx):
    app.connect("env-get-outdated", _get_outdated)
    app.connect("env-purge-doc", _purge_doc)
