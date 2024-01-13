# flake8: noqa

from __future__ import annotations

import reprlib
import collections
from breathe import file_state_cache, path_handler
from breathe.project import ProjectInfo


from sphinx.application import Sphinx

from typing import overload, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    NodeOrValue = Node | str | None

T_inv = TypeVar("T_inv")


try:
    from breathe._parser import *
except ImportError:
    from breathe._parser_py import *
else:
    @reprlib.recursive_repr()
    def node_repr(self: Node) -> str:  # pragma: no cover
        cls = type(self)
        fields = []
        if isinstance(self, FrozenList):
            pos = ", ".join(map(repr, self))
            fields.append(f"[{pos}]")
        fields.extend(f"{field}={getattr(self,field)!r}" for field in cls._fields)
        inner = ", ".join(fields)
        return f"{cls.__name__}({inner})"


    Node.__repr__ = node_repr  # type: ignore


    @reprlib.recursive_repr()
    def taggedvalue_repr(self: TaggedValue) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}({self.name!r}, {self.value!r})"


    TaggedValue.__repr__ = taggedvalue_repr  # type: ignore


    @reprlib.recursive_repr()
    def frozenlist_repr(self: FrozenList) -> str:  # pragma: no cover
        inner = ", ".join(map(repr, self))
        return f"{self.__class__.__name__}([{inner}])"


    FrozenList.__repr__ = frozenlist_repr  # type: ignore


def description_has_content(node: Node_descriptionType | None) -> bool:
    if node is None:
        return False
    if bool(node.title) or len(node) > 1:
        return True
    if not len(node):
        return False
    item = node[0]
    return not isinstance(item, str) or (len(item) > 0 and not item.isspace())


class ParserError(RuntimeError):
    def __init__(self, message: str, filename: str, lineno: int | None = None):
        super().__init__(message, lineno, filename)

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


class DoxygenIndex:
    def __init__(self, root: Node_DoxygenTypeIndex):
        self.root = root
        self.compounds: collections.defaultdict[
            str, list[Node_CompoundType]
        ] = collections.defaultdict(list)
        self.members: collections.defaultdict[
            str, list[tuple[Node_MemberType, Node_CompoundType]]
        ] = collections.defaultdict(list)

        self.file_compounds: list[Node_CompoundType] = []

        for c in root.compound:
            self.compounds[c.name].append(c)
            if c.kind == CompoundKind.file:
                self.file_compounds.append(c)
            for m in c.member:
                self.members[m.name].append((m, c))


class DoxygenCompound:
    def __init__(self, root: Node_DoxygenType):
        self.root = root
        self.members_by_id: dict[
            str, tuple[Node_memberdefType, Node_sectiondefType, Node_compounddefType]
        ] = {}
        self.enumvalue_by_id: dict[
            str,
            tuple[
                Node_enumvalueType, Node_memberdefType, Node_sectiondefType, Node_compounddefType
            ],
        ] = {}

        for c in root.compounddef:
            for s in c.sectiondef:
                for m in s.memberdef:
                    self.members_by_id[m.id] = (m, s, c)
                    for ev in m.enumvalue:
                        self.enumvalue_by_id[ev.id] = (ev, m, s, c)


def _parse_common(filename: str, right_tag: str) -> Node_DoxygenType | Node_DoxygenTypeIndex:
    try:
        with open(filename, "rb") as file:
            result = parse_file(file)
        if result.name != right_tag:
            raise ParserError(f'expected "{right_tag}" root element, not "{result.name}"', filename)

        return result.value
    except ParseError as e:
        raise ParserError(e.message, filename, e.lineno)
    except IOError as e:
        raise FileIOError(str(e), filename)


class DoxygenParser:
    def __init__(self, app: Sphinx) -> None:
        self.app = app
        self.compound_index: DoxygenIndex | None = None
        self.compound_cache: dict[str, DoxygenCompound] = {}

    def parse_index(self, project_info: ProjectInfo) -> DoxygenIndex:
        r: DoxygenIndex | None = self.compound_index
        if r is None:
            filename = path_handler.resolve_path(self.app, project_info.project_path(), "index.xml")

            file_state_cache.update(self.app, filename)

            n = _parse_common(filename, "doxygenindex")
            assert isinstance(n, Node_DoxygenTypeIndex)
            r = DoxygenIndex(n)

            self.compound_index = r
        return r

    def parse_compound(self, refid: str, project_info: ProjectInfo) -> DoxygenCompound:
        r = self.compound_cache.get(refid)
        if r is None:
            filename = path_handler.resolve_path(
                self.app, project_info.project_path(), f"{refid}.xml"
            )

            file_state_cache.update(self.app, filename)

            n = _parse_common(filename, "doxygen")
            assert isinstance(n, Node_DoxygenType)
            r = DoxygenCompound(n)
            self.compound_cache[refid] = r
        return r


@overload
def tag_name_value(x: TaggedValue[T, U]) -> tuple[T, U]:
    ...


@overload
def tag_name_value(x: str) -> tuple[None, str]:
    ...


@overload
def tag_name_value(x: TaggedValue[T, U] | str) -> tuple[T | None, U | str]:
    ...


def tag_name_value(x):
    if isinstance(x, str):
        return None, x
    return x.name, x.value
