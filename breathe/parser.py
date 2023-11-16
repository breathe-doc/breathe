from breathe import file_state_cache, path_handler
from breathe.project import ProjectInfo

from breathe._parser import *

from sphinx.application import Sphinx


class ParserError(RuntimeError):
    def __init__(self, error: str, filename: str):
        super().__init__(error)

        self.error = error
        self.filename = filename

    def __str__(self):
        # TODO: update _parser.ParseError to store the line number and message
        # as separate fields for better formatting here
        return f"file {self.filename}: {self.error}"


class FileIOError(RuntimeError):
    def __init__(self, error: str, filename: str):
        super().__init__(error)

        self.error = error
        self.filename = filename


class Parser:
    def __init__(self, app: Sphinx, cache):
        self.app = app
        self.cache = cache
    
    def _parse_common(self,filename: str, right_tag: str) -> Node_DoxygenTypeIndex | Node_DoxygenType:
        try:
            # Try to get from our cache
            return self.cache[filename]
        except KeyError:
            # If that fails, parse it afresh
            try:
                with open(filename,'rb') as file:
                    result = parse_file(file)
                if result.name != right_tag:
                    raise ParserError(f'expected "{right_tag}" root element, not "{result.name}"',filename)
                self.cache[filename] = result
                return result.value
            except ParseError as e:
                raise ParserError(str(e), filename)
            except IOError as e:
                raise FileIOError(str(e), filename)


class DoxygenIndexParser(Parser):
    def parse(self, project_info: ProjectInfo) -> Node_DoxygenTypeIndex:
        filename = path_handler.resolve_path(self.app, project_info.project_path(), "index.xml")
        file_state_cache.update(self.app, filename)

        r = self._parse_common(filename, 'doxygenindex')
        assert isinstance(r,Node_DoxygenTypeIndex)
        return r


class DoxygenCompoundParser(Parser):
    def __init__(self, app: Sphinx, cache,
                 project_info: ProjectInfo) -> None:
        super().__init__(app, cache)

        self.project_info = project_info

    def parse(self, refid: str) -> Node_DoxygenType:
        filename = path_handler.resolve_path(
            self.app,
            self.project_info.project_path(),
            f"{refid}.xml"
        )

        file_state_cache.update(self.app, filename)

        r = self._parse_common(filename, 'doxygen')
        assert isinstance(r,Node_DoxygenType)
        return r


class DoxygenParserFactory:
    def __init__(self, app: Sphinx) -> None:
        self.app = app
        self.cache: dict[str, Node_DoxygenType | Node_DoxygenTypeIndex] = {}

    def create_index_parser(self) -> DoxygenIndexParser:
        return DoxygenIndexParser(self.app, self.cache)

    def create_compound_parser(self, project_info: ProjectInfo) -> DoxygenCompoundParser:
        return DoxygenCompoundParser(self.app, self.cache, project_info)
