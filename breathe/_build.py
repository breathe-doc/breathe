"""Setuptools build commands used when building Breathe.

The ``breathe/_parser.py`` module is generated from
``xml_parser_generator/schema.json`` at build time. ``setuptools`` requires the
``cmdclass`` entries in ``pyproject.toml`` to be dotted, Python-qualified
identifiers (``pkg.mod.Class``), so this thin module exposes
:class:`xml_parser_generator.setuptools_builder.CustomBuildPy` under the
``breathe`` package.
"""

from __future__ import annotations

import sys
from pathlib import Path

# When setuptools resolves the ``cmdclass`` entry it imports this module by
# file path, without necessarily having the project root on ``sys.path``.
# Make sure the sibling ``xml_parser_generator`` package can be imported.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from xml_parser_generator.setuptools_builder import CustomBuildPy  # noqa: E402

__all__ = ["CustomBuildPy"]
