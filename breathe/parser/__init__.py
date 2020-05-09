from . import index
from . import compound

from breathe import file_state_cache
from breathe import path_handler
from breathe.parser.compoundsuper import DoxygenType

from sphinx.application import Sphinx

from typing import Dict

class ParserError(Exception):
    def __init__(self, error, filename):
        Exception.__init__(self, error)

        self.error = error
        self.filename = filename

    def __str__(self):
        return ("file %s: %s" % (self.filename, self.error))


class FileIOError(Exception):
    def __init__(self, error, filename):
        Exception.__init__(self, error)

        self.error = error
        self.filename = filename


class Parser:
    def __init__(self, app: Sphinx, cache: Dict[str, DoxygenType]):
        self.app = app
        self.cache = cache


class DoxygenIndexParser(Parser):
    def __init__(self, app: Sphinx, cache: Dict[str, DoxygenType]):
        super().__init__(app, cache)

    def parse(self, project_info):
        filename = path_handler.resolve_path(self.app, project_info.project_path(), "index.xml")

        file_state_cache.update(self.app, filename)

        try:
            # Try to get from our cache
            return self.cache[filename]
        except KeyError:

            # If that fails, parse it afresh
            try:
                result = index.parse(filename)
                self.cache[filename] = result
                return result
            except index.ParseError as e:
                raise ParserError(e, filename)
            except index.FileIOError as e:
                raise FileIOError(e, filename)


class DoxygenCompoundParser(Parser):
    def __init__(self, app: Sphinx, cache, project_info):
        super().__init__(app, cache)

        self.project_info = project_info

    def parse(self, refid) -> DoxygenType:
        filename = path_handler.resolve_path(
            self.app,
            self.project_info.project_path(),
            "%s.xml" % refid
        )

        file_state_cache.update(self.app, filename)

        try:
            # Try to get from our cache
            return self.cache[filename]
        except KeyError:
            # If that fails, parse it afresh
            try:
                result = compound.parse(filename)
                self.cache[filename] = result
                return result
            except compound.ParseError as e:
                raise ParserError(e, filename)
            except compound.FileIOError as e:
                raise FileIOError(e, filename)


class DoxygenParserFactory:
    def __init__(self, app: Sphinx):
        self.app = app
        self.cache = {}  # type: Dict[str, DoxygenType]

    def create_index_parser(self):
        return DoxygenIndexParser(self.app, self.cache)

    def create_compound_parser(self, project_info):
        return DoxygenCompoundParser(
            self.app,
            self.cache,
            project_info
        )