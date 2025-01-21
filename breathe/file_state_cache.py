from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

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
        raise MTimeError("Cannot find file: %s" % os.path.realpath(filename))


def update(app: Sphinx, source_file: str | os.PathLike[str]) -> None:
    if not hasattr(app.env, "breathe_file_state"):
        app.env.breathe_file_state = {}  # type: ignore[attr-defined]

    norm_source_file = Path(source_file).resolve().as_posix()
    new_mtime = _getmtime(norm_source_file)
    _mtime, docnames = app.env.breathe_file_state.setdefault(  # type: ignore[attr-defined]
        norm_source_file, (new_mtime, set())
    )

    assert app.env is not None
    docnames.add(app.env.docname)

    app.env.breathe_file_state[norm_source_file] = (new_mtime, docnames)  # type: ignore[attr-defined]


def _get_outdated(
    app: Sphinx, env: BuildEnvironment, added: set[str], changed: set[str], removed: set[str]
) -> list[str]:
    if not hasattr(app.env, "breathe_file_state"):
        return []

    stale = []
    for filename, info in app.env.breathe_file_state.items():
        old_mtime, docnames = info
        if _getmtime(filename) > old_mtime:
            stale.extend(docnames)
    return list(set(stale).difference(removed))


def _purge_doc(app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    if not hasattr(app.env, "breathe_file_state"):
        return

    toremove = []
    for filename, info in app.env.breathe_file_state.items():
        _, docnames = info
        docnames.discard(docname)
        if not docnames:
            toremove.append(filename)

    for filename in toremove:
        del app.env.breathe_file_state[filename]


def setup(app: Sphinx):
    app.connect("env-get-outdated", _get_outdated)
    app.connect("env-purge-doc", _purge_doc)
