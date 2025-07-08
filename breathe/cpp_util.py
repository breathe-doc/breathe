from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

RE_NAME_PART = re.compile(r"([<>()[\]]|::)")


def _check_pair(dest: list[str], tokens: Iterator[str], start: str, end: str) -> bool:
    if dest[-1] == start:
        for tok in tokens:
            dest.append(tok)
            if tok == end:
                break
            # If we're inside angle brackets, we assume "<" and ">" are brackets
            # and not comparison operators. Once we're inside other brackets, we
            # only need to worry about recursive brackets and can ignore the
            # other types.
            if start == "<":
                _check_all_pairs(dest, tokens)
            else:
                _check_pair(dest, tokens, start, end)
        return True
    return False


def _check_all_pairs(dest: list[str], tokens: Iterator[str]) -> None:
    if not _check_pair(dest, tokens, "<", ">"):
        if not _check_pair(dest, tokens, "(", ")"):
            if not _check_pair(dest, tokens, "[", "]"):
                _check_pair(dest, tokens, "{", "}")


def split_name(name: str) -> list[str]:
    """Split a qualified C++ name into the namespace components.

    E.g. turn "A<B::C>::D::E<(F>G::H),(I<J)>" into
    ["A<B::C>","D","E<(F>G::H),(I<J)>"]

    This can produce incorrect results if any of the template parameters are
    strings containing brackets.
    """
    last: list[str] = []
    parts = [last]
    tokens = iter(RE_NAME_PART.split(name))
    for tok in tokens:
        if tok == "::":
            last = []
            parts.append(last)
        else:
            last.append(tok)
            _check_all_pairs(last, tokens)

    return ["".join(subparts) for subparts in parts]
