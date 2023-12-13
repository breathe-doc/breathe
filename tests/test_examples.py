from xml.parsers import expat
import pytest
import pathlib
import subprocess
import shutil
import enum
import dataclasses


DOXYFILE_TEMPLATE = """
PROJECT_NAME     = "example"
HAVE_DOT         = YES
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
OUTPUT_DIRECTORY = "{output}"
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
GENERATE_HTML = NO
GENERATE_XML = YES
WARN_IF_UNDOCUMENTED = NO
ALIASES = "rst=\\verbatim embed:rst"
ALIASES += "endrst=\\endverbatim"
ALIASES += "inlinerst=\\verbatim embed:rst:inline"
"""

C_FILE_SUFFIXES = frozenset((".h", ".c", ".hpp", ".cpp"))
IGNORED_ELEMENTS = frozenset(())

BUFFER_SIZE = 0x1000

TEST_DATA_DIR = pathlib.Path(__file__).parent / "data"

DEFAULT_CONF = {
    "project": "test",
    "breathe_default_project": "example",
    "breathe_show_include": False,
    "extensions": ["breathe", "sphinx.ext.graphviz"],
}


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
            pending_events.append(
                (
                    XMLEventType.E_TEXT,
                    XMLTextElement(pending_text, p.CurrentLineNumber, p.CurrentColumnNumber),
                )
            )
            pending_text = ""

    def handle_start(name, attr):
        dispatch_text()

        pending_events.append(
            (
                XMLEventType.E_START,
                XMLElement(name, attr, p.CurrentLineNumber, p.CurrentColumnNumber),
            )
        )

    p.StartElementHandler = handle_start

    def handle_end(_):
        dispatch_text()
        pending_events.append(
            (XMLEventType.E_END, XMLElementEnd(p.CurrentLineNumber, p.CurrentColumnNumber))
        )

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


def compare_xml(generated, model):
    event_str = {
        XMLEventType.E_START: "element start",
        XMLEventType.E_END: "element end",
        XMLEventType.E_TEXT: "text",
    }

    with open(generated) as o_file, open(model) as c_file:
        for o, c in zip(filtered_xml(o_file), filtered_xml(c_file)):
            o_type, o_node = o
            c_type, c_node = c
            assert (
                o_type == c_type
            ), f"at line {o_node.line_no}: found {event_str[o_type]} when expecting {event_str[c_type]}"

            if o_type == XMLEventType.E_START:
                assert (
                    o_node.name == c_node.name
                ), f"wrong tag at line {o_node.line_no}: expected {c_node.name}, found {o_node.name}"

                # ignore extra attributes in o_node
                for key, value in c_node.attr.items():
                    assert key in o_node.attr, f"missing attribute at line {o_node.line_no}: {key}"
                    o_value = o_node.attr[key]
                    assert (
                        o_value == value
                    ), f'wrong value for attribute "{key}" at line {o_node.line_no}: expected "{value}", found "{o_value}"'
            elif o_type == XMLEventType.E_TEXT:
                assert (
                    o_node.value == c_node.value
                ), f'wrong content at line {o_node.line_no}: expected "{c_node.value}", found "{o_node.value}"'


@pytest.mark.parametrize("test_input", get_individual_tests())
def test_example(make_app, tmp_path, test_input, monkeypatch):
    monkeypatch.chdir(test_input)

    doxygen = shutil.which("doxygen")
    if doxygen is None:
        raise ValueError("cannot find doxygen executable")

    doxyfile = tmp_path / "Doxyfile"
    doxycontent = DOXYFILE_TEMPLATE.format(output=tmp_path)
    extra_opts = test_input / "extra_dox_opts.txt"
    if extra_opts.exists():
        doxycontent += extra_opts.read_text()
    doxyfile.write_text(doxycontent)
    (tmp_path / "conf.py").touch()
    shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")

    subprocess.run([doxygen, doxyfile], check=True)

    make_app(
        buildername="xml",
        srcdir=tmp_path,
        confoverrides=conf_overrides({"breathe_projects": {"example": str(tmp_path / "xml")}}),
    ).build()

    compare_xml(tmp_path / "_build" / "xml" / "index.xml", test_input / "compare.xml")


def test_auto(make_app, tmp_path, monkeypatch):
    test_input = TEST_DATA_DIR / "auto"
    monkeypatch.chdir(test_input)
    (tmp_path / "conf.py").touch()
    shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")

    make_app(
        buildername="xml",
        srcdir=tmp_path,
        confoverrides=conf_overrides(
            {
                "breathe_projects_source": {
                    "example": (test_input, ["auto_class.h", "auto_function.h"])
                }
            }
        ),
    ).build()

    compare_xml(tmp_path / "_build" / "xml" / "index.xml", test_input / "compare.xml")
