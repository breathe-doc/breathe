from __future__ import annotations

from xml.dom import minidom

from breathe import path_handler
from breathe.parser.compoundsuper import memberdefType
from breathe.renderer.sphinxrenderer import get_definition_without_template_args, get_param_decl


def test_param_decl():
    # From xml from: examples/specific/parameters.h
    xml = """
    <memberdef>
    <param>
      <type>int</type>
      <declname>a</declname>
    </param>
    <param>
      <type>float</type>
      <declname>b</declname>
    </param>
    <param>
      <type>int *</type>
      <declname>c</declname>
    </param>
    <param>
      <type>int(**)</type>
      <declname>p</declname>
      <array>[3]</array>
    </param>
    <param>
      <type><ref refid="class_my_class" kindref="compound">MyClass</ref></type>
      <declname>a</declname>
    </param>
    <param>
      <type><ref refid="class_my_class" kindref="compound">MyClass</ref> *</type>
      <declname>b</declname>
    </param>
    <param>
      <type>int(&amp;)</type>
      <declname>r</declname>
      <array>[3]</array>
    </param>
    </memberdef>
    """

    doc = minidom.parseString(xml)

    memberdef = memberdefType.factory()
    for child in doc.documentElement.childNodes:
        memberdef.buildChildren(child, "param")

    assert get_param_decl(memberdef.param[0]) == "int a"
    assert get_param_decl(memberdef.param[1]) == "float b"
    assert get_param_decl(memberdef.param[2]) == "int * c"
    assert get_param_decl(memberdef.param[3]) == "int(**p)[3]"
    assert get_param_decl(memberdef.param[4]) == "MyClass a"
    assert get_param_decl(memberdef.param[5]) == "MyClass  * b"
    assert get_param_decl(memberdef.param[6]) == "int(&r)[3]"


def test_definition_without_template_args():
    def get_definition(definition, name, bitfield=""):
        class MockDataObject:
            def __init__(self, definition, name, bitfield):
                self.definition = definition
                self.name = name
                self.bitfield = bitfield

        return get_definition_without_template_args(MockDataObject(definition, name, bitfield))

    assert "void A::foo" == get_definition("void A<T>::foo", "foo")
    # Template arguments in the return type should be preserved:
    assert "Result<T> A::f" == get_definition("Result<T> A::f", "f")
    # Nested template arguments:
    assert "Result<T> A::f" == get_definition("Result<T> A< B<C> >::f", "f")

    # Bit fields
    assert "int f : 3" == get_definition("int f", "f", "3")


def test_path_handler():
    assert path_handler.includes_directory("directory/file.h") is True
    assert path_handler.includes_directory("directory\\file.h") is True
    assert path_handler.includes_directory("file.h") is False
