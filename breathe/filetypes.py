"""
A module to house the methods for resolving a code-blocks language based on filename
(and extension).
"""
from typing import Optional
import os.path

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


def get_pygments_alias(filename: str) -> Optional[str]:
    "Find first pygments alias from filename"
    try:
        lexer_cls = get_lexer_for_filename(filename)
        return lexer_cls.aliases[0]  # type: ignore
    except ClassNotFound:
        return None


def get_extension(filename: str) -> str:
    "Get extension from filename"
    # If the filename is just '.ext' then we get ('.ext', '') so we fall back to first part if
    # the second isn't there
    (first, second) = os.path.splitext(filename)

    # Doxygen allows users to specify the file extension ".unparsed" to disable syntax highlighting.
    # We translate it into the pygments un-highlighted 'text' type
    return (second or first).lstrip(".").replace("unparsed", "text")
