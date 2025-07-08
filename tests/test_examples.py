from __future__ import annotations

import dataclasses
import enum
import os
import pathlib
import shutil
import subprocess
from typing import TYPE_CHECKING
from xml.parsers import expat

import pytest
import sphinx

from breathe.process import AutoDoxygenProcessHandle

if TYPE_CHECKING:
    from typing import Any

sphinx_path: Any

if sphinx.version_info < (7, 2, 0):
    from sphinx.testing.path import path as sphinx_path
else:
    sphinx_path = pathlib.Path


C_FILE_SUFFIXES = frozenset((".h", ".c", ".hpp", ".cpp"))
IGNORED_ELEMENTS: frozenset[str] = frozenset(())

BUFFER_SIZE = 0x1000

TEST_DATA_DIR = pathlib.Path(__file__).parent / "data"

# if this is changed, tests/data/examples/README.rst should be updated
DEFAULT_CONF = {
    "project": "test",
    "breathe_default_project": "example",
    "breathe_show_include": False,
    "extensions": ["breathe", "sphinx.ext.graphviz"],
}

DOXYGEN_CACHE_KEY = "BREATHE_DOXYGEN_TEST_CACHE"


class XMLEventType(enum.Enum):
    E_START = enum.auto()
    E_END = enum.auto()
    E_TEXT = enum.auto()


@dataclasses.dataclass
class XMLElement:
    name: str
    attr: dict[str, str]
    line_no: int
    column_no: int


@dataclasses.dataclass
class XMLElementEnd:
    line_no: int
    column_no: int


@dataclasses.dataclass
class XMLTextElement:
    value: str
    line_no: int
    column_no: int


def xml_stream(infile):
    """XML pull parser.

    This is similar to xml.dom.pulldom.parse, except the locations of the
    elements are tracked."""
    p = expat.ParserCreate()

    pending_events = []
    pending_text = ""

    def dispatch_text():
        nonlocal pending_text

        if pending_text:
            pending_events.append((
                XMLEventType.E_TEXT,
                XMLTextElement(pending_text, p.CurrentLineNumber, p.CurrentColumnNumber),
            ))
            pending_text = ""

    def handle_start(name, attr):
        dispatch_text()

        pending_events.append((
            XMLEventType.E_START,
            XMLElement(name, attr, p.CurrentLineNumber, p.CurrentColumnNumber),
        ))

    p.StartElementHandler = handle_start

    def handle_end(_):
        dispatch_text()
        pending_events.append((
            XMLEventType.E_END,
            XMLElementEnd(p.CurrentLineNumber, p.CurrentColumnNumber),
        ))

    p.EndElementHandler = handle_end

    def handle_text(data):
        nonlocal pending_text
        pending_text += data

    p.CharacterDataHandler = handle_text

    while True:
        data = infile.read(BUFFER_SIZE)
        if not data:
            dispatch_text()
            p.Parse(data, True)
            yield from pending_events
            break
        p.Parse(data, False)
        if pending_events:
            yield from pending_events
            pending_events.clear()


def get_individual_tests():
    return (TEST_DATA_DIR / "examples").glob("test_*")


def filtered_xml(infile):
    ignore = 0
    for event, node in xml_stream(infile):
        if event == XMLEventType.E_START:
            if ignore or node.name in IGNORED_ELEMENTS:
                ignore += 1
            else:
                yield event, node
        elif event == XMLEventType.E_END:
            if ignore:
                ignore -= 1
            else:
                yield event, node
        else:
            if not ignore:
                text = node.value.strip()
                if text:
                    node.value = text
                    yield event, node


def conf_overrides(extra):
    conf = DEFAULT_CONF.copy()
    conf.update(extra)
    return conf


def str_to_set(x):
    return frozenset(x.split())


def attr_compare(name, actual, expected):
    if name == "classes":
        return str_to_set(actual) >= str_to_set(expected)

    return actual == expected


@dataclasses.dataclass
class VersionedFile:
    file: str
    version: tuple[int, ...]


@dataclasses.dataclass
class DoxygenExe(VersionedFile):
    template: str


def str_to_version(v_str):
    return tuple(map(int, v_str.strip().split(".")))


def versioned_model(p):
    return VersionedFile(str(p), str_to_version(str(p.name)[len("compare-") : -len(".xml")]))


def compare_xml(generated, input_dir, version):
    alt_models = list(map(versioned_model, input_dir.glob("compare-*.xml")))
    alt_models.sort(key=(lambda f: f.version), reverse=True)

    model = input_dir / "compare.xml"
    for alt_m in alt_models:
        if version >= alt_m.version:
            model = alt_m.file
            break

    event_str = {
        XMLEventType.E_START: "element start",
        XMLEventType.E_END: "element end",
        XMLEventType.E_TEXT: "text",
    }

    with open(generated, encoding="utf-8") as o_file, open(model, encoding="utf-8") as c_file:
        for o, c in zip(filtered_xml(o_file), filtered_xml(c_file)):
            o_type, o_node = o
            c_type, c_node = c
            assert o_type == c_type, (
                f"at line {o_node.line_no}: found {event_str[o_type]} when expecting {event_str[c_type]}"  # noqa: E501
            )

            if o_type == XMLEventType.E_START:
                assert o_node.name == c_node.name, (
                    f"wrong tag at line {o_node.line_no}: expected {c_node.name}, found {o_node.name}"  # noqa: E501
                )

                # ignore extra attributes in o_node
                for key, value in c_node.attr.items():
                    if (
                        c_node.name == "desc_inline"
                        and key == "domain"
                        and sphinx.version_info[0] < 6
                    ):
                        # prior to Sphinx 6, this attribute was not present
                        continue

                    assert key in o_node.attr, f"missing attribute at line {o_node.line_no}: {key}"
                    o_value = o_node.attr[key]
                    assert attr_compare(key, o_value, value), (
                        f'wrong value for attribute "{key}" at line {o_node.line_no}: expected "{value}", found "{o_value}"'  # noqa: E501
                    )
            elif o_type == XMLEventType.E_TEXT:
                assert o_node.value == c_node.value, (
                    f'wrong content at line {o_node.line_no}: expected "{c_node.value}", found "{o_node.value}"'  # noqa: E501
                )


@pytest.fixture(scope="module")
def doxygen_cache():
    dc = os.environ.get(DOXYGEN_CACHE_KEY)
    if not dc:
        return None
    return pathlib.Path(dc).absolute()


@pytest.fixture(scope="module")
def doxygen(doxygen_cache):
    if doxygen_cache is None:
        exc = shutil.which("doxygen")
        if not exc:
            raise ValueError("cannot find doxygen executable")

        v_str = subprocess.run(
            [exc, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        ).stdout
    else:
        exc = ""
        v_str = (doxygen_cache / "version.txt").read_text(encoding="utf-8")

    return DoxygenExe(
        exc,
        str_to_version(v_str.split()[0]),
        (TEST_DATA_DIR / "examples" / "doxyfile_template").read_text(encoding="utf-8"),
    )


def run_doxygen_with_template(doxygen, tmp_path, cache, example_name, output_name):
    doxyfile = tmp_path / "Doxyfile"
    doxycontent = doxygen.template.format(output=tmp_path)
    extra_opts = pathlib.Path("extra_dox_opts.txt")
    if extra_opts.exists():
        doxycontent += extra_opts.read_text(encoding="utf-8")
    doxyfile.write_text(doxycontent, encoding="utf-8")

    if cache is not None:
        # instead of passing a different path to breathe_projects.example, the
        # folder is copied to the same place it would be without caching so that
        # all paths in the generated output remain the same
        shutil.copytree(cache / example_name / output_name, tmp_path / output_name)
    else:
        subprocess.run([doxygen.file, doxyfile], check=True)
        if output_name != "xml":
            os.rename(tmp_path / "xml", tmp_path / output_name)


def run_sphinx_and_compare(make_app, tmp_path, test_input, overrides, version):
    dest = tmp_path / "conf.py"
    ec = pathlib.Path("extra_conf.py")
    if ec.exists():
        shutil.copyfile(ec, dest)
    else:
        dest.touch()

    make_app(
        buildername="xml",
        srcdir=sphinx_path(tmp_path),
        confoverrides=conf_overrides(overrides),
    ).build()

    compare_xml(tmp_path / "_build" / "xml" / "index.xml", test_input, version)


@pytest.mark.parametrize("test_input", get_individual_tests(), ids=(lambda x: x.name[5:]))
def test_example(make_app, tmp_path, test_input, monkeypatch, doxygen, doxygen_cache):
    monkeypatch.chdir(test_input)

    run_doxygen_with_template(doxygen, tmp_path, doxygen_cache, test_input.name, "xml")
    shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")
    run_sphinx_and_compare(
        make_app,
        tmp_path,
        test_input,
        {"breathe_projects": {"example": str(tmp_path / "xml")}},
        doxygen.version,
    )


def test_auto(make_app, tmp_path, monkeypatch, doxygen, doxygen_cache):
    test_input = TEST_DATA_DIR / "auto"
    monkeypatch.chdir(test_input)

    if doxygen_cache is not None:
        xml_path = str(doxygen_cache / "auto" / "xml")
        monkeypatch.setattr(AutoDoxygenProcessHandle, "process", (lambda *args, **kwds: xml_path))

    shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")
    run_sphinx_and_compare(
        make_app,
        tmp_path,
        test_input,
        {
            "breathe_projects_source": {
                "example": (str(test_input.absolute()), ["auto_class.h", "auto_function.h"])
            }
        },
        doxygen.version,
    )


def test_multiple_projects(make_app, tmp_path, monkeypatch, doxygen, doxygen_cache):
    test_input = TEST_DATA_DIR / "multi_project"

    for c in "ABC":
        monkeypatch.chdir(test_input / c)
        run_doxygen_with_template(doxygen, tmp_path, doxygen_cache, f"multi_project.{c}", f"xml{c}")

    (tmp_path / "index.rst").write_text(
        (test_input / "input.rst")
        .read_text(encoding="utf-8")
        .format(project_c_path=str(tmp_path / "xmlC")),
        encoding="utf-8",
    )
    run_sphinx_and_compare(
        make_app,
        tmp_path,
        test_input,
        {"breathe_projects": {"A": str(tmp_path / "xmlA"), "B": str(tmp_path / "xmlB")}},
        doxygen.version,
    )
