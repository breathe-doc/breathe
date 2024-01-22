"""Parse a JSON schema file and generate the C code for a Python module to parse
XML"""

from __future__ import annotations

import re
import json
import enum
import dataclasses
import functools
import keyword
import collections

from typing import Any, Callable, cast, Literal, NamedTuple, NoReturn, TYPE_CHECKING, TypeVar

import jinja2

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

T = TypeVar("T")


# The minimum number of items a set should have before using a hash-based
# lookup. If fewer, the strings are compared one-by-one instead.
HASH_LOOKUP_THRESHOLD = 8

SPLIT_LINE_ITEM_THRESHOLD = 5

BUILTIN_ATTR_SCHEMA_TYPES = [
    ("string", "str"),
    ("DoxBool", "bool"),
    ("integer", "int"),
    ("empty", "None"),
]

RE_CHAR_TYPE = re.compile(r"\s*#\s*char\s*\(([^\s)]+)\s*\)\s*")


def comma_join(items: Sequence[str], indent: int = 4):
    if len(items) < SPLIT_LINE_ITEM_THRESHOLD:
        return ", ".join(items)

    return (",\n" + " " * indent).join(items)


class ContentType(enum.Enum):
    """A value specifying how children are organized when parsing an array-type
    element"""

    bare = enum.auto()
    """Child values are added directly to the array.
    
    There can only be one child type, which can be an element or text.
    """

    tuple = enum.auto()
    """Child elements are grouped into named tuple-like objects.
    
    Each batch of child elements must appear in order in the XML document. Text
    content is not allowed.
    
    Currently, tuple child element names must be valid Python identifiers as
    there isn't a way to have different field names.
    """

    union = enum.auto()
    """Each item is either a tagged union (an instance of TaggedValue) or a
    plain string"""


@dataclasses.dataclass()
class TypeRef:
    """An XML element"""

    name: str
    """the name of the element as it will appear in the XML file"""

    py_name: str
    """The Python field name that will hold the parsed value.
    
    This will be different from "name" if "name" is not a valid Python
    identifier.
    """

    type: str | SchemaType
    """While the schema is being parsed, this will be a string containing the
    name of attribute's type. After parsing, this is set to the object
    representing the type.
    """

    is_list: bool
    """Whether this element can appear more than once in its context"""

    min_items: Literal[0] | Literal[1]
    """If this is zero, the element is optional.
    
    This can only be zero or one.
    """

    def py_type(self, as_param=False) -> str:
        """Get the Python type annotation describing the type of this element.

        If "as_param" is True, this represents a parameter type that can be
        converted to the actual type. For example with a given type "T": the
        generated parser uses FrozenList[T] to store arrays, but constructors
        accept Iterable[T] for array fields.
        """

        assert isinstance(self.type, SchemaType)
        if self.is_list:
            container = "Iterable" if as_param else "FrozenList"
            return f"{container}[{self.type.py_name}]"
        if self.min_items == 0:
            return f"{self.type.py_name} | None"
        return self.type.py_name

    def needs_finish(self) -> bool:
        """Return True if the field value will need to be checked at the end of
        parsing the element.

        This is the case case for all fields except list fields with no minimum.
        For most fields, we need to know how many corresponding child elements
        exist, which can't be known until the parent element is fully parsed,
        but list fields without minimums accept any number of child elements.
        """
        return not self.is_list or self.min_items > 0


@dataclasses.dataclass()
class Attribute:
    """An XML attribute"""

    name: str
    """the name of the attribute as it will appear in the XML file"""

    py_name: str
    """The Python field name that will hold the parsed value.
    
    This will be different from "name" if "name" is not a valid Python
    identifier.
    """

    type: str | AttributeType
    """While the schema is being parsed, this will be a string containing the
    name of attribute's type. After parsing, this is set to the object
    representing the type.
    """

    optional: bool
    """Whether the attribute may be omitted.
    
    Fields corresponding to omitted attributes are set to None.
    """

    def py_type(self, as_param=False) -> str:
        """Get the Python type annotation describing the type of this attribute.

        If "as_param" is True, this represents a parameter type that can be
        converted to the actual type. For example with a given type "T": the
        generated parser uses FrozenList[T] to store arrays, but constructors
        accept Iterable[T] for array fields.
        """

        assert isinstance(self.type, SchemaType)
        if self.optional:
            return f"{self.type.py_name} | None"
        return self.type.py_name


@dataclasses.dataclass()
class SchemaType:
    name: str

    def __str__(self):
        """This is equal to self.name.

        This is important for the Jinja template, which frequently uses the
        names of types.
        """
        return self.name

    def content_names(self) -> Iterable[str]:
        return []

    @property
    def extra_args(self) -> str:
        """A string to add before the closing bracket of the C function call to
        the type's element start handler"""
        return ""

    def add_sorted(self, dest: list[SchemaType], visited: set[int]) -> None:
        if id(self) not in visited:
            visited.add(id(self))
            dest.append(self)

    if TYPE_CHECKING:

        @property
        def py_name(self) -> str:
            raise NotImplementedError


@dataclasses.dataclass()
class AttributeType(SchemaType):
    """A type that can be used in attributes and elements.

    When used for an element, the element will not have any attributes or child
    elements.
    """


@dataclasses.dataclass()
class BuiltinType(SchemaType):
    py_name: str
    """the name of the Python data type that will represent a value of this
    type"""


@dataclasses.dataclass()
class AddsToStringType(BuiltinType):
    pass


@dataclasses.dataclass()
class SpType(AddsToStringType):
    """This element represents an arbitrary character whose code point is
    given in the attribute "value".

    If "value" isn't present, the character is a space.
    """


@dataclasses.dataclass()
class CodePointType(AddsToStringType):
    """This element represents a specific character."""

    char: int
    """The unicode code-point of the character"""

    def __init__(self, char: int):
        self.name = "const_char"
        self.py_name = "str"
        self.char = char

    @property
    def extra_args(self) -> str:
        return f",{self.char:#x}"


@dataclasses.dataclass()
class BuiltinAttributeType(BuiltinType, AttributeType):
    pass


class OtherAttrAction(enum.Enum):
    ignore = enum.auto()
    error = enum.auto()


@dataclasses.dataclass()
class ElementType(SchemaType):
    """An element type specified by the schema"""

    bases: list[str | SchemaType]
    """the types to derive from"""

    attributes: dict[str, Attribute]
    """XML attributes"""

    other_attr: OtherAttrAction
    """how to handle attributes not in "attributes" """

    children: dict[str, TypeRef]
    """XML child elements"""

    used_directly: bool
    """Each element that is used directly, corresponds to a separate Python
    class. If this is False, this element is only used as a base element for
    other types and does not produce any Python classes."""

    def fields(self) -> Iterable[TypeRef | Attribute]:
        yield from self.attributes.values()
        yield from self.children.values()

    @property
    def direct_field_count(self):
        return len(self.attributes) + len(self.children)

    def all_fields(self) -> Iterable[TypeRef | Attribute]:
        for b in self.bases:
            if isinstance(b, ElementType):
                yield from b.all_fields()
        yield from self.fields()

    @property
    def py_name(self) -> str:
        return f"Node_{self.name}"

    def add_sorted(self, dest: list[SchemaType], visited: set[int]) -> None:
        if id(self) not in visited:
            for b in self.bases:
                assert isinstance(b, SchemaType)
                b.add_sorted(dest, visited)
            visited.add(id(self))
            dest.append(self)


@dataclasses.dataclass()
class TagOnlyElement(ElementType):
    """A simple element that cannot contain text (not counting whitespace) and
    does not preserve the order of its child elements"""


@dataclasses.dataclass()
class ListElement(ElementType):
    """An element type that gets parsed as an array type.

    The items of the array depend on "content", "content_type" and "allow_text".
    """

    min_items: int

    content: dict[str, str | SchemaType]
    """Child elements that will be stored as array items.

    While the schema is being parsed, the values will be strings containing the
    names of the elements' types. After parsing, they are set to the objects
    representing the types.
    """

    content_type: ContentType

    allow_text: bool

    def content_names(self) -> Iterable[str]:
        for b in self.bases:
            assert isinstance(b, SchemaType)
            yield from b.content_names()
        yield from self.content

    def all_content(self):
        for b in self.bases:
            if isinstance(b, ListElement):
                yield from b.content.values()
        yield from self.content.values()

    def py_union_ref(self) -> list[str]:
        types = self.py_union_list()
        if len(types) <= 1:
            return types
        return ["ListItem_" + self.name]

    def py_union_list(self, quote=False) -> list[str]:
        """Return a list of type annotations, the union of which, represent
        every possible value of this array's elements.

        This assumes self.content_type == ContentType.union.
        """
        assert self.content_type == ContentType.union
        by_type = collections.defaultdict(list)
        needs_str = False
        for name, t in self.content.items():
            assert isinstance(t, SchemaType)
            if not isinstance(t, AddsToStringType):
                by_type[t.py_name].append(name)
            else:
                needs_str = True
        types = [
            "TaggedValue[Literal[{}], {}]".format(
                comma_join(sorted(f"'{n}'" for n in names), 26), f'"{t}"' if quote else t
            )
            for t, names in by_type.items()
        ]
        str_included = False
        for b in self.bases:
            if isinstance(b, ListElement):
                types.extend(b.py_union_ref())
                if b.allow_text:
                    str_included = True
        if self.allow_text and not str_included:
            types.append("str")
        elif needs_str:
            raise ValueError(
                f'type "{self.name}" cannot have #spType or '
                + '#char(...) items unless "allow_text" is true'
            )
        return types


@dataclasses.dataclass()
class Schema:
    roots: dict[str, str | SchemaType]
    types: dict[str, SchemaType]


class EnumEntry(NamedTuple):
    xml: str
    id: str


@dataclasses.dataclass()
class SchemaEnum(AttributeType):
    """A type representing an enumeration.

    This type is represented in python with enum.Enum.
    """

    children: list[EnumEntry]
    hash: HashData | None = None

    def any_renamed(self) -> bool:
        return any(c.xml != c.id for c in self.children)

    @property
    def py_name(self) -> str:
        return self.name


@dataclasses.dataclass()
class SchemaCharEnum(AttributeType):
    """An enumeration type whose elements are single characters.

    Unlike SchemaEnum, the values are represented as strings.
    """

    values: str

    @property
    def py_name(self) -> str:
        return self.name


def unknown_type_error(ref: str, context: str, is_element: bool) -> NoReturn:
    thing = "element" if is_element else "attribute"
    raise ValueError(f'{thing} "{context}" has undefined type "{ref}"')


def check_type_ref(schema: Schema, ref: str, context: str, is_element: bool = True) -> SchemaType:
    """Get the schema type that represent the type named by "ref" """

    t = schema.types.get(ref)
    if t is None:
        m = RE_CHAR_TYPE.fullmatch(ref)
        if m is not None:
            char = int(m.group(1), 16)
            if char > 0x10FFFF:
                raise ValueError(
                    f'"char" type at "{context}" must have a value between 0 and 0x10FFFF inclusive'
                )
            return CodePointType(char)
        unknown_type_error(ref, context, is_element)
    return t


def check_attr_type_ref(schema: Schema, ref: str, context: str) -> AttributeType:
    """Get the schema type that represent the type named by "ref" and raise an
    exception if it's not usable in an XML attribute"""

    r = check_type_ref(schema, ref, context, False)
    if isinstance(r, AttributeType):
        return r

    raise ValueError(f'attribute "{context}" has incompatible type "{ref}"')


def check_py_name(name: str) -> None:
    """Raise ValueError if "name" is not suitable as a Python field name"""

    if (not name.isidentifier()) or keyword.iskeyword(name):
        raise ValueError(f'"{name}" is not a valid Python identifier')
    if name == "_children":
        raise ValueError('the name "_children" is reserved by the parser generator')


def resolve_refs(schema: Schema) -> tuple[list[str], list[str]]:
    """Replace all type reference names with actual types and return the lists
    of all element names and attribute names"""

    elements: set[str] = set()
    attributes: set[str] = set()

    def check_element_type_defined(name: str, ref: str) -> SchemaType:
        t = check_type_ref(schema, ref, name)
        if isinstance(t, ElementType):
            t.used_directly = True
        return t

    for name, r in schema.roots.items():
        elements.add(name)
        schema.roots[name] = check_element_type_defined(name, cast(str, r))

    for typename, t in schema.types.items():
        if not t.name:
            t.name = typename

        if isinstance(t, ElementType):
            # TODO: check for recursive bases
            for i, b in enumerate(t.bases):
                b_type = schema.types.get(cast(str, b))
                if b_type is None:
                    raise ValueError(f'type "{typename}" has undefined base "{b}"')
                if not isinstance(b_type, ElementType):
                    raise ValueError(f'"{b}" cannot be used as a base')
                if isinstance(b_type, ListElement):
                    if not isinstance(t, ListElement):
                        raise ValueError(f"non-list elements cannot use list elements as bases")
                    if b_type.content_type != t.content_type:
                        raise ValueError(
                            f"list elements of one type cannot use list elements of another type as bases"
                        )
                t.bases[i] = b_type
            for name, child in t.children.items():
                child.name = name
                if not child.py_name:
                    child.py_name = name
                check_py_name(child.py_name)
                elements.add(name)
                child.type = check_element_type_defined(f"{typename}.{name}", cast(str, child.type))
            for name, attr in t.attributes.items():
                attr.name = name
                if not attr.py_name:
                    attr.py_name = name
                check_py_name(attr.py_name)
                attributes.add(name)
                t.attributes[name].type = check_attr_type_ref(schema, cast(str, attr.type), name)
            if isinstance(t, ListElement):
                for name, r in t.content.items():
                    elements.add(name)
                    t.content[name] = check_element_type_defined(f"{typename}.{name}", cast(str, r))

    elements.update(schema.roots)

    return sorted(elements), sorted(attributes)


class HashData(NamedTuple):
    salt1: str
    salt2: str
    g: list[int]


# def generate_hash(items: list[str]) -> HashData:
#    try:
#        f1, f2, g = perfect_hash.generate_hash(items)
#        return HashData(f1.salt, f2.salt, g)
#    except ValueError:
#        print(items, file=sys.stderr)
#        raise


def collect_field_names(
    all_fields: set[str], cur_fields: set[str], refs: Iterable[Attribute | TypeRef], type_name: str
) -> None:
    """Gather all field names into "all_fields" and make sure they are unique in
    "cur_fields" """

    for ref in refs:
        all_fields.add(ref.py_name)
        if ref.py_name in cur_fields:
            raise ValueError(f'python name "{ref.py_name}" appears more than once in "{type_name}"')
        cur_fields.add(ref.py_name)


def make_env(schema: Schema) -> jinja2.Environment:
    elements, attributes = resolve_refs(schema)
    tag_names: set[str] = set(schema.roots)
    py_field_name_set: set[str] = set()
    char_enum_chars: set[str] = set()
    list_element_field_counts: set[int] = set()
    tagonly_and_tuple_field_counts: set[int] = set()
    tuple_field_counts: set[int] = set()

    def field_count(t) -> int:
        if not isinstance(t, ElementType):
            return 0
        return len(t.attributes) + len(t.children) + sum(cast(int, field_count(b)) for b in t.bases)

    for t in schema.types.values():
        # if isinstance(t, SchemaEnum):
        #    if len(t.children) >= HASH_LOOKUP_THRESHOLD:
        #        t.hash = generate_hash([item.xml for item in t.children])
        if isinstance(t, SchemaCharEnum):
            char_enum_chars.update(t.values)
        elif isinstance(t, ElementType):
            fields: set[str] = set()
            collect_field_names(py_field_name_set, fields, t.attributes.values(), t.name)
            collect_field_names(py_field_name_set, fields, t.children.values(), t.name)

            if isinstance(t, TagOnlyElement):
                if t.used_directly:
                    tagonly_and_tuple_field_counts.add(field_count(t))
            elif isinstance(t, ListElement):
                if t.used_directly:
                    list_element_field_counts.add(field_count(t))
                if t.content_type == ContentType.union:
                    tag_names.update(
                        name for name, t in t.content.items() if not isinstance(t, AddsToStringType)
                    )
                elif t.content_type == ContentType.tuple:
                    tuple_field_counts.add(len(t.content))
                    tagonly_and_tuple_field_counts.add(len(t.content))

    py_field_names = sorted(py_field_name_set)

    tmpl_env = jinja2.Environment(
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{$",
        variable_end_string="$}",
        comment_start_string="/*#",
        comment_end_string="#*/",
        line_statement_prefix="//%",
        line_comment_prefix="//#",
        autoescape=False,
    )

    def has_attributes(t):
        if not isinstance(t, ElementType):
            return False
        return t.attributes or any(has_attributes(b) for b in t.bases)

    def has_children(t):
        if not isinstance(t, ElementType):
            return False
        return t.children or any(has_children(b) for b in t.bases)

    def has_children_or_content(t):
        if not isinstance(t, ElementType):
            return False
        return (
            t.children
            or (isinstance(t, ListElement) and t.content)
            or any(has_children_or_content(b) for b in t.bases)
        )

    def has_children_or_tuple_content(t):
        if not isinstance(t, ElementType):
            return False
        return (
            t.children
            or (
                isinstance(t, ListElement)
                and t.content_type == ContentType.tuple
                and len(t.content) > 1
            )
            or any(has_children_or_tuple_content(b) for b in t.bases)
        )

    def base_offsets(t):
        if not isinstance(t, ElementType):
            return tmpl_env.undefined()
        total = 0
        for b in t.bases:
            assert isinstance(b, SchemaType)
            yield b, total
            total += field_count(b)
        yield None, total

    def list_type_or_base(t):
        if not isinstance(t, ElementType):
            return False
        return isinstance(t, ListElement) or any(list_type_or_base(b) for b in t.bases)

    def allow_text(t):
        if not isinstance(t, ListElement):
            return False
        return t.allow_text or any(allow_text(b) for b in t.bases)

    def content_type(ct):
        def inner(t):
            if not isinstance(t, ListElement):
                return False
            return t.content_type == ct

        return inner

    def children(t):
        if not isinstance(t, ElementType):
            return tmpl_env.undefined()
        return t.children.values()

    def get_attributes(t):
        if not isinstance(t, ElementType):
            return tmpl_env.undefined()
        return t.attributes.values()

    def content(t):
        if not isinstance(t, ListElement):
            return tmpl_env.undefined()
        return t.content.items()

    def used_directly(t):
        return isinstance(t, ElementType) and t.used_directly

    def optional(ref: TypeRef | Attribute) -> bool:
        if isinstance(ref, TypeRef):
            return ref.is_list or ref.min_items == 0
        return ref.optional

    def array_field(ref) -> bool:
        if isinstance(ref, TypeRef):
            return ref.is_list
        return False

    def needs_finish_fields_call(t):
        if not isinstance(t, ElementType):
            return False
        return any(c.needs_finish() for c in t.children.values()) or any(
            map(needs_finish_fields_call, t.bases)
        )

    def needs_finish_call(t):
        return needs_finish_fields_call(t) or (
            isinstance(t, ListElement)
            and t.content_type == ContentType.tuple
            and len(t.content) > 1
        )

    def error(msg):
        raise TypeError(msg)

    class Once:
        def __init__(self, content):
            self.content = content
            self.used = False

        def __call__(self):
            if self.used:
                return ""
            self.used = True
            return self.content

    # types sorted topologically with regard to base elements
    sorted_types: list[SchemaType] = []
    visited_types: set[int] = set()

    for t in schema.types.values():
        t.add_sorted(sorted_types, visited_types)
        if isinstance(t, ElementType) and any(field_count(cast(ElementType, b)) for b in t.bases):
            # the code was written to support this but it has never been tested
            raise ValueError(
                'elements having bases that have "attributes" or "children" are not currently supported'
            )

    tmpl_env.tests.update(
        {
            "element": (lambda x: isinstance(x, ElementType)),
            "tagonly_e": (lambda x: isinstance(x, TagOnlyElement)),
            "list_e": list_type_or_base,
            "builtin_t": (lambda x: isinstance(x, BuiltinType)),
            "enumeration_t": (lambda x: isinstance(x, SchemaEnum)),
            "char_enum_t": (lambda x: isinstance(x, SchemaCharEnum)),
            "appends_str": (lambda x: isinstance(x, AddsToStringType)),
            "code_point_t": (lambda x: isinstance(x, CodePointType)),
            "sp_t": (lambda x: isinstance(x, CodePointType)),
            "used_directly": used_directly,
            "allow_text": allow_text,
            "has_attributes": has_attributes,
            "has_children": has_children,
            "has_children_or_content": has_children_or_content,
            "has_fields": lambda x: field_count(x) > 0,
            "has_children_or_tuple_content": has_children_or_tuple_content,
            "needs_finish_fields_call": needs_finish_fields_call,
            "needs_finish_call": needs_finish_call,
            "content_bare": content_type(ContentType.bare),
            "content_tuple": content_type(ContentType.tuple),
            "content_union": content_type(ContentType.union),
            "optional": optional,
            "array_field": array_field,
        }
    )
    tmpl_env.filters.update(
        {
            "field_count": field_count,
            "base_offsets": base_offsets,
            "children": children,
            "attributes": get_attributes,
            "content": content,
            "error": error,
            "Once": Once,
        }
    )
    tmpl_env.globals.update(
        {
            "types": sorted_types,
            "root_elements": list(schema.roots.items()),
            "element_names": elements,
            "attribute_names": attributes,
            "py_field_names": py_field_names,
            # "e_hash": generate_hash(elements),
            # "a_hash": generate_hash(attributes),
            # "py_f_hash": generate_hash(py_field_names),
            "union_tag_names": sorted(tag_names),
            "char_enum_chars": {c: i for i, c in enumerate(sorted(char_enum_chars))},
            "list_element_field_counts": list(list_element_field_counts),
            "tagonly_and_tuple_field_counts": list(tagonly_and_tuple_field_counts),
            "tuple_field_counts": list(tuple_field_counts),
            "OtherAttrAction": OtherAttrAction,
        }
    )

    return tmpl_env


class _NoDefault:
    pass


_NO_DEFAULT = _NoDefault()


def get_json_value(
    conv: Callable[[Any, str], T],
    context: str,
    d: dict[str, Any],
    key: str,
    default: T | _NoDefault = _NO_DEFAULT,
) -> T:
    r = d.get(key, _NO_DEFAULT)
    if r is _NO_DEFAULT:
        if default is _NO_DEFAULT:
            raise ValueError(f'missing value for "{context}.{key}"')
        return cast(T, default)
    return conv(r, context)


def check_simple(t: type[T], name: str) -> Callable[[Any, str], T]:
    def inner(x, context: str) -> T:
        if isinstance(x, t):
            return x
        raise TypeError(f'value for "{context}" must be {name}')

    return inner


get_json_bool = functools.partial(get_json_value, check_simple(bool, "a boolean"))
get_json_int = functools.partial(get_json_value, check_simple(int, "an integer"))

check_string = check_simple(str, "a string")
get_json_str = functools.partial(get_json_value, check_string)

check_obj = check_simple(cast("type[dict[str, Any]]", dict), "an object")
get_json_obj = functools.partial(get_json_value, check_obj)

check_list = check_simple(list, "an array")


def get_json_mapping(
    item_conv: Callable[[Any, str], T],
    context: str,
    d: dict,
    key: str,
    default: dict[str, T] | _NoDefault = _NO_DEFAULT,
) -> dict[str, T]:
    def check(x, context):
        x = check_obj(x, context)
        return {key: item_conv(value, f"{context}.{key}") for key, value in x.items()}

    return get_json_value(check, context, d, key, default)


def get_json_list(
    item_conv: Callable[[Any, str], T],
    context: str,
    d: dict,
    key: str,
    default: list[T] | _NoDefault = _NO_DEFAULT,
) -> list[T]:
    def check(x, context) -> list[T]:
        x = check_list(x, context)
        return [item_conv(value, f"{context}[{i}]") for i, value in enumerate(x)]

    return get_json_value(check, context, d, key, default)


def check_zero_or_one(x, context: str) -> Literal[0] | Literal[1]:
    if x == 0:
        return 0
    if x == 1:
        return 1
    raise TypeError(f'value for "{context}" must be 0 or 1')


get_json_zero_or_one = functools.partial(get_json_value, check_zero_or_one)


def check_other_attr_action(x, context: str) -> OtherAttrAction:
    if x == "ignore":
        return OtherAttrAction.ignore
    if x == "error":
        return OtherAttrAction.error
    raise TypeError(f'value for "{context}" must be "error" or "ignore"')


get_json_other_attr_action = functools.partial(get_json_value, check_other_attr_action)


def check_typeref(x, context: str) -> TypeRef:
    x = check_obj(x, context)
    return TypeRef(
        "",
        get_json_str(context, x, "py_name", ""),
        get_json_str(context, x, "type"),
        get_json_bool(context, x, "is_list", False),
        get_json_zero_or_one(context, x, "min_items", 1),
    )


get_json_typeref = functools.partial(get_json_value, check_typeref)


def check_attribute(x, context: str) -> Attribute:
    x = check_obj(x, context)
    return Attribute(
        "",
        get_json_str(context, x, "py_name", ""),
        get_json_str(context, x, "type"),
        get_json_bool(context, x, "optional", False),
    )


get_json_attribute = functools.partial(get_json_value, check_attribute)


def check_enum_entry(x, context: str) -> EnumEntry:
    if isinstance(x, str):
        return EnumEntry(x, x)
    if isinstance(x, dict):
        xml = get_json_str(context, x, "xml")
        id = get_json_str(context, x, "id", xml)
        if not id.isidentifier():
            raise ValueError(f'value of "{context}" is not a valid Python identifier')
        return EnumEntry(xml, id)
    raise TypeError(f'"{context}" must be a string or object')


def make_tag_only_element(x: dict[str, Any], context: str) -> TagOnlyElement:
    return TagOnlyElement(
        "",
        get_json_list(check_string, context, x, "bases", []),
        get_json_mapping(check_attribute, context, x, "attributes", {}),
        get_json_other_attr_action(context, x, "other_attr", OtherAttrAction.error),
        get_json_mapping(check_typeref, context, x, "children", {}),
        False,
    )


def make_list_element(x: dict[str, Any], context: str, content_t: ContentType) -> ListElement:
    return ListElement(
        "",
        get_json_list(check_string, context, x, "bases", []),
        get_json_mapping(check_attribute, context, x, "attributes", {}),
        get_json_other_attr_action(context, x, "other_attr", OtherAttrAction.error),
        get_json_mapping(check_typeref, context, x, "children", {}),
        False,
        get_json_int(context, x, "min_items", 0),
        get_json_mapping(check_string, context, x, "content", {}),
        content_t,
        get_json_bool(context, x, "allow_text", False),
    )


def make_enumeration(x: dict[str, Any], context: str) -> SchemaEnum:
    return SchemaEnum("", get_json_list(check_enum_entry, context, x, "values"))


def make_char_enumeration(x: dict[str, Any], context: str) -> SchemaCharEnum:
    return SchemaCharEnum("", get_json_str(context, x, "values"))


def check_type(x, context: str) -> SchemaType:
    x = check_obj(x, context)
    kind = get_json_str(context, x, "kind")
    if kind == "tag_only_element":
        return make_tag_only_element(x, context)
    if kind == "list_element":
        return make_list_element(x, context, ContentType.bare)
    if kind == "union_list_element":
        return make_list_element(x, context, ContentType.union)
    if kind == "tuple_list_element":
        return make_list_element(x, context, ContentType.tuple)
    if kind == "enumeration":
        return make_enumeration(x, context)
    if kind == "char_enumeration":
        return make_char_enumeration(x, context)

    raise ValueError(
        f'"{context}.kind" must be "tag_only_element", "list_element", "mixed_element" or "enumeration"'
    )


get_json_type = functools.partial(get_json_value, check_type)


def check_schema(x) -> Schema:
    if not isinstance(x, dict):
        raise TypeError("json value must be an object")
    r = Schema(
        get_json_mapping(check_string, "<root>", x, "roots"),
        get_json_mapping(check_type, "<root>", x, "types", {}),
    )
    r.types["#spType"] = SpType("spType", "str")
    for t, py in BUILTIN_ATTR_SCHEMA_TYPES:
        r.types["#" + t] = BuiltinAttributeType(t, py)
    return r


def generate_from_json(json_path, template_files) -> None:
    with open(json_path, "rb") as ifile:
        schema = check_schema(json.load(ifile))

    env = make_env(schema)

    for i_file, o_file in template_files:
        with open(i_file) as tfile:
            template_str = tfile.read()
        with open(o_file, "w") as ofile:
            env.from_string(template_str).stream().dump(ofile)
