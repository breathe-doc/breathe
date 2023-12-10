import enum
from typing import ClassVar, Generic, Literal, overload, Protocol, Self, SupportsIndex, TypeVar
from collections.abc import Iterable

T = TypeVar('T',covariant=True)
U = TypeVar('U',covariant=True)

class SupportsRead(Protocol):
    def read(self, length: int, /) -> bytes | bytearray: ...

class FrozenListItr(Generic[T]):
    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...

class FrozenList(Generic[T]):
    def __init__(self, items: Iterable[T]): ...
    def __len__(self) -> int: ...
    def __getitem__(self, i: SupportsIndex) -> T: ...
    def __iter__(self) -> FrozenListItr[T]: ...

class TaggedValue(Generic[T, U]):
    @property
    def name(self) -> T: ...

    @property
    def value(self) -> U: ...

    def __init__(self, name: T, value: U): ...

    def __len__(self) -> Literal[2]: ...

    @overload
    def __getitem__(self, i: Literal[0]) -> T: ...

    @overload
    def __getitem__(self, i: Literal[1]) -> U: ...

    @overload
    def __getitem__(self, i: SupportsIndex) -> T | U: ...

class Node:
    _fields: ClassVar[tuple[str, ...]]

class ParseError(RuntimeError):
    @property
    def message(self) -> str: ...
    @property
    def lineno(self) -> int: ...

class ParseWarning(UserWarning):
    pass

TopLevel = (
//% for name,type in root_elements
    {$ '| ' if not loop.first $}TaggedValue[Literal['{$ name $}'],{$ type.py_name $}]
//% endfor
)

def parse_str(data: str, /) -> TopLevel: ...

def parse_file(file: SupportsRead, /) -> TopLevel: ...


//% macro emit_fields(type)
{%- for b in type.bases %}{$ emit_fields(b) $}{% endfor -%}
//%   for ref in type|attributes
    {$ ref.py_name $}: {$ ref.py_type() $}
//%   endfor
//%   for ref in type|children
    {$ ref.py_name $}: {$ ref.py_type() $}
//%   endfor
//% endmacro

//% macro emit_content_fields(type)
{%- for b in type.bases %}{$ emit_content_fields(b) $}{% endfor -%}
//%   for cname,ctype in type|content
    {$ cname $}: {$ ctype.py_name $}
//%   endfor
//% endmacro

//% for type in types
//%   if type is content_tuple
//%     set list_item_type = 'ListItem_'~type
class ListItem_{$ type $}:
{$ emit_content_fields(type) $}
    def __init__(self{% for cname,ctype in type|content %}, {$ cname $}: {$ ctype.py_name $}{% endfor %}): ...

    def __len__(self) -> Literal[{$ type|content|length $}]: ...
//%     for cname,ctype in type|content
    @overload
    def __getitem__(self,i: Literal[{$ loop.index0 $}]) -> {$ ctype.py_name $}: ...
//%     endfor
    @overload
    def __getitem__(self,i: SupportsIndex) -> {$ type|content|map('last')|map(attribute='py_name')|join(' | ') $}: ...

//%   elif type is content_union
//%     set members = type.py_union_list()|sort
//%     if members|length > 1
//%       set list_item_type = 'ListItem_'~type
ListItem_{$ type $} = (
//%       for m in members
    {$ '| ' if not loop.first $}{$ m $}
//%       endfor
)

//%     else
//%       set list_item_type = members|first
//%     endif
//%   elif type is content_bare
//%     set list_item_type = (type|content|first)[1].py_name
//%   elif type is list_e
{$ "invalid content type"|error $}
//%   endif
//%   if type is used_directly
class Node_{$ type $}(Node{$ ', FrozenList['~list_item_type~']' if type is list_e $}):
{$ emit_fields(type) $}
    def __init__(self{$ ', __items: Iterable['~list_item_type~'], /' if type is list_e $}
        {%- if type|field_count -%}, *
            {%- for f in type.all_fields() if f is not optional %}, {$ f.py_name $}: {$ f.py_type(true) $}{% endfor -%}
            {%- for f in type.all_fields() if f is optional %}, {$ f.py_name $}: {$ f.py_type(true) $} = ...{% endfor -%}
        {%- endif %}): ...

//%   elif type is enumeration_t
class {$ type $}(enum.Enum):
//%     for entry in type.children
    {$ entry.id $} = '{$ entry.xml $}'
//%     endfor

//%   elif type is char_enum_t
{$ type $} = Literal[{% for c in type.values %}{$ "'"~c~"'" $}{$ ',' if not loop.last $}{% endfor %}]
//%   endif
//% endfor
