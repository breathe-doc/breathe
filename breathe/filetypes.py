from typing import Optional
import os.path

import pygments  # type: ignore


def get_pygments_alias(filename: str) -> Optional[str]:
    "Find first pygments alias from filename"
    try:
        lexer_cls = pygments.lexers.get_lexer_for_filename(filename)
        return lexer_cls.aliases[0]
    except pygments.util.ClassNotFound:
        return None


def get_extension(filename: str) -> str:
    "Get extension from filename"
    # If the filename is just '.ext' then we get ('.ext', '') so we fall back to first part if
    # the second isn't there
    (first, second) = os.path.splitext(filename)
    return (second or first).lstrip(".")
