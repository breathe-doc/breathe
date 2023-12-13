from __future__ import annotations

import sys
import json
import enum
import dataclasses
import functools
import keyword
import collections

from typing import Any, Callable, cast, Literal, NamedTuple, NoReturn, TYPE_CHECKING, TypeVar

import jinja2
import perfect_hash

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


def comma_join(items: Sequence[str], indent: int = 4):
    if len(items) < SPLIT_LINE_ITEM_THRESHOLD:
        return ", ".join(items)

    return (",\n" + " " * indent).join(items)


class ContentType(enum.Enum):
    bare = enum.auto()
    tuple = enum.auto()
    union = enum.auto()


@dataclasses.dataclass()
class TypeRef:
    name: str
    py_name: str
    type: str | SchemaType
    is_list: bool
    min_items: Literal[0] | Literal[1]

    def py_type(self, as_param=False) -> str:
        assert isinstance(self.type, SchemaType)
        if self.is_list:
            container = "Iterable" if as_param else "FrozenList"
            return f"{container}[{self.type.py_name}]"
        if self.min_items == 0:
            return f"{self.type.py_name} | None"
        return self.type.py_name


@dataclasses.dataclass()
class Attribute:
    name: str
    py_name: str
    type: str | AttributeType
    optional: bool

    def py_type(self, as_param=False) -> str:
        assert isinstance(self.type, SchemaType)
        if self.optional:
            return f"{self.type.py_name} | None"
        return self.type.py_name


@dataclasses.dataclass()
class SchemaType:
    name: str

    def __str__(self):
        return self.name

    def content_names(self) -> Iterable[str]:
        return []

    @property
    def py_name(self) -> str:
        raise NotImplementedError


@dataclasses.dataclass()
class AttributeType(SchemaType):
    pass


@dataclasses.dataclass()
class BuiltinType(SchemaType):
    py_name: str


@dataclasses.dataclass()
class SpType(BuiltinType):
    pass


@dataclasses.dataclass()
class BuiltinAttributeType(BuiltinType, AttributeType):
    pass


class OtherAttrAction(enum.Enum):
    ignore = enum.auto()
    error = enum.auto()


@dataclasses.dataclass()
class ElementType(SchemaType):
    bases: list[str | SchemaType]
    attributes: dict[str, Attribute]
    other_attr: OtherAttrAction
    children: dict[str, TypeRef]
    used_directly: bool

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


@dataclasses.dataclass()
class TagOnlyElement(ElementType):
    pass


@dataclasses.dataclass()
class ListElement(ElementType):
    min_items: int
    content: dict[str, str | SchemaType]
    content_type: ContentType
    allow_text: bool
    sp_tag: str | None = None

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

    def py_item_type_union_size(self) -> int:
        size = len(self.content) if self.content_type == ContentType.union else 0
        for b in self.bases:
            if isinstance(b, ListElement):
                size += b.py_item_type_union_size()
        return size

    def py_union_ref(self) -> list[str]:
        types = self.py_union_list()
        if len(types) <= 1:
            return types
        return ["ListItem_" + self.name]

    def py_union_list(self) -> list[str]:
        by_type = collections.defaultdict(list)
        for name, t in self.content.items():
            assert isinstance(t, SchemaType)
            by_type[t.py_name].append(name)
        types = [
            "TaggedValue[Literal[{}], {}]".format(
                comma_join(sorted(f"'{n}'" for n in names), 26), t
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
    children: list[EnumEntry]
    hash: HashData | None = None

    def any_renamed(self) -> bool:
        return any(c.xml != c.id for c in self.children)

    @property
    def py_name(self) -> str:
        return self.name


@dataclasses.dataclass()
class SchemaCharEnum(AttributeType):
    values: str

    @property
    def py_name(self) -> str:
        return self.name


def unknown_type_error(ref: str, context: str, is_element: bool) -> NoReturn:
    thing = "element" if is_element else "attribute"
    raise ValueError(f'{thing} "{context}" has undefined type "{ref}"')


def check_type_ref(schema: Schema, ref: str, context: str, is_element: bool = True) -> SchemaType:
    t = schema.types.get(ref)
    if t is None:
        unknown_type_error(ref, context, is_element)
    return t


def check_attr_type_ref(schema: Schema, ref: str, context: str) -> AttributeType:
    r = check_type_ref(schema, ref, context, False)
    if isinstance(r, AttributeType):
        return r

    raise ValueError(f'attribute "{context}" has incompatible type "{ref}"')


def check_py_name(name: str) -> None:
    if (not name.isidentifier()) or keyword.iskeyword(name):
        raise ValueError(f'"{name}" is not a valid Python identifier')
    if name == "_children":
        raise ValueError('the name "_children" is reserved by the parser generator')


def resolve_refs(schema: Schema) -> tuple[list[str], list[str]]:
    """Check that all referenced types exist and return the lists of all
    element names and attribute names"""

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


def generate_hash(items: list[str]) -> HashData:
    try:
        f1, f2, g = perfect_hash.generate_hash(items)
        return HashData(f1.salt, f2.salt, g)
    except ValueError:
        print(items, file=sys.stderr)
        raise


def collect_field_names(
    all_fields: set[str], cur_fields: set[str], refs: Iterable[Attribute | TypeRef], type_name: str
) -> None:
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
        if isinstance(t, SchemaEnum):
            if len(t.children) >= HASH_LOOKUP_THRESHOLD:
                t.hash = generate_hash([item.xml for item in t.children])
        elif isinstance(t, SchemaCharEnum):
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
                    tag_names.update(t.content)
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

    for t in schema.types.values():
        if isinstance(t, ElementType) and any(field_count(cast(ElementType, b)) for b in t.bases):
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
            "appends_str": (lambda x: isinstance(x, SpType)),
            "used_directly": used_directly,
            "allow_text": allow_text,
            "has_attributes": has_attributes,
            "has_children": has_children,
            "has_children_or_content": has_children_or_content,
            "has_fields": lambda x: field_count(x) > 0,
            "has_children_or_tuple_content": has_children_or_tuple_content,
            "content_bare": content_type(ContentType.bare),
            "content_tuple": content_type(ContentType.tuple),
            "content_union": content_type(ContentType.union),
            "optional": optional,
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
            "types": list(schema.types.values()),
            "root_elements": list(schema.roots.items()),
            "element_names": elements,
            "attribute_names": attributes,
            "py_field_names": py_field_names,
            "e_hash": generate_hash(elements),
            "a_hash": generate_hash(attributes),
            "py_f_hash": generate_hash(py_field_names),
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

check_obj = check_simple(cast(type[dict[str, Any]], dict), "an object")
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


def generate_from_json(
    json_path, c_template_file, pyi_template_file, c_output_file, pyi_output_file
) -> None:
    with open(json_path, "rb") as ifile:
        schema = check_schema(json.load(ifile))

    env = make_env(schema)

    with open(c_template_file) as tfile:
        template_str = tfile.read()
    with open(c_output_file, "w") as ofile:
        env.from_string(template_str).stream().dump(ofile)

    with open(pyi_template_file) as tfile:
        template_str = tfile.read()
    with open(pyi_output_file, "w") as ofile:
        env.from_string(template_str).stream().dump(ofile)


if __name__ == "__main__":
    generate_from_json(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
