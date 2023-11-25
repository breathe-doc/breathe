from __future__ import annotations

import reprlib
from breathe import file_state_cache, path_handler
from breathe.project import ProjectInfo

from breathe._parser import *

from sphinx.application import Sphinx

from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    NodeOrValue = Node | str | None

@reprlib.recursive_repr()
def node_repr(self: Node) -> str:
    cls = type(self)
    fields = ', '.join(f'{field}={getattr(self,field)!r}' for field in cls._fields)
    if isinstance(self,FrozenList):
        pos = ', '.join(map(repr,self))
        fields = f'[{pos}], {fields}'
    return f'{cls.__name__}({fields})'
Node.__repr__ = node_repr # type: ignore


class ParserError(RuntimeError):
    def __init__(self, message: str, filename: str, lineno: int | None = None):
        super().__init__(message,lineno,filename)

    @property
    def message(self) -> str:
        return self.args[0]
    
    @property
    def lineno(self) -> int | None:
        return self.args[1]
    
    @property
    def filename(self) -> str:
        return self.args[2]

    def __str__(self):
        if self.lineno is None:
            return f"{self.filename}: {self.message}"
        return f"{self.filename}:{self.lineno}: {self.message}"


class FileIOError(RuntimeError):
    def __init__(self, error: str, filename: str):
        super().__init__(error)

        self.error = error
        self.filename = filename


class Parser:
    def __init__(self, app: Sphinx, cache: dict[str, Node_DoxygenTypeIndex | Node_DoxygenType]):
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
                self.cache[filename] = result.value
                return result.value
            except ParseError as e:
                raise ParserError(e.message, filename, e.lineno)
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


@overload
def tag_name_value(x: TaggedValue[T, U]) -> tuple[T, U]: ...

@overload
def tag_name_value(x: str) -> tuple[None,str]: ...

@overload
def tag_name_value(x: TaggedValue[T, U] | str) -> tuple[T | None, U | str]: ...

def tag_name_value(x):
    if isinstance(x,str): return None,x
    return x.name,x.value
