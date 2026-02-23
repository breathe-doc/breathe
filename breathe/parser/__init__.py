from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from breathe import file_state_cache
from breathe.parser import compound, index
from breathe.path_handler import resolve_path

if TYPE_CHECKING:
    from sphinx.application import Sphinx

    from breathe.project import ProjectInfo


class ParserError(Exception):
    def __init__(self, error: Exception, filename: Path):
        super().__init__(error)

        self.error = error
        self.filename = filename

    def __str__(self):
        return "file %s: %s" % (self.filename, self.error)


class FileIOError(Exception):
    def __init__(self, error: Exception, filename: Path):
        super().__init__(error)

        self.error = error
        self.filename = filename


# Within-execution memoization that does not touch fstat
_ephemeral_parse_cache: dict[Path, Any] = {}


class Parser:
    def __init__(self, app: Sphinx, cache):
        self.app = app
        self.cache = cache

    def _cached_parse(self, module, project_info: ProjectInfo, rel_filename: str):
        filename = resolve_path(self.app.confdir, project_info.project_path(), rel_filename)
        try:
            return _ephemeral_parse_cache[filename]
        except KeyError:
            pass

        # Get from persistent cache
        file_state_cache.update(self.app, filename)
        try:
            result = self.cache[filename]
        except KeyError:
            pass
        else:
            _ephemeral_parse_cache[filename] = result
            return result

        # Not cached: parse it afresh
        try:
            result = module.parse(filename)
        except module.ParseError as e:
            raise ParserError(e, filename)
        except module.FileIOError as e:
            raise FileIOError(e, filename)
        else:
            self.cache[filename] = result
            _ephemeral_parse_cache[filename] = result
            return result


class DoxygenIndexParser(Parser):
    def parse(self, project_info: ProjectInfo):
        return self._cached_parse(index, project_info, "index.xml")


class DoxygenCompoundParser(Parser):
    def __init__(self, app: Sphinx, cache, project_info: ProjectInfo) -> None:
        super().__init__(app, cache)

        self.project_info = project_info

    def parse(self, refid: str):
        return self._cached_parse(compound, self.project_info, refid + ".xml")


class DoxygenParserFactory:
    def __init__(self, app: Sphinx) -> None:
        self.app = app
        # TODO: do we have a base class for all the Doxygen XML node types
        #       that we can use for typing?
        self.cache = {}  # type: ignore[var-annotated]

    def create_index_parser(self) -> DoxygenIndexParser:
        return DoxygenIndexParser(self.app, self.cache)

    def create_compound_parser(self, project_info: ProjectInfo) -> DoxygenCompoundParser:
        return DoxygenCompoundParser(self.app, self.cache, project_info)
