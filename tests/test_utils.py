from unittest import TestCase

from breathe.renderer.sphinxrenderer import get_param_decl, get_definition_without_template_args
from breathe import path_handler, parser


class TestUtils(TestCase):
    def test_param_decl(self):
        # From xml from: examples/specific/parameters.h
        xml = """
        <doxygen lang="" version="">
        <compounddef id="" kind="type" prot="public">
        <compoundname></compoundname>
        <sectiondef kind="typedef">
        <memberdef id="" kind="function" prot="public" static="no">
        <name>x</name>
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
        <location file="" line="0"/>
        </memberdef>
        </sectiondef>
        </compounddef>
        </doxygen>
        """

        doc = parser.parse_str(xml)
        assert isinstance(doc.value, parser.Node_DoxygenType)

        memberdef = doc.value.compounddef[0].sectiondef[0].memberdef[0]

        self.assertEqual(get_param_decl(memberdef.param[0]), "int a")
        self.assertEqual(get_param_decl(memberdef.param[1]), "float b")
        self.assertEqual(get_param_decl(memberdef.param[2]), "int * c")
        self.assertEqual(get_param_decl(memberdef.param[3]), "int(**p)[3]")
        self.assertEqual(get_param_decl(memberdef.param[4]), "MyClass a")
        self.assertEqual(get_param_decl(memberdef.param[5]), "MyClass  * b")
        self.assertEqual(get_param_decl(memberdef.param[6]), "int(&r)[3]")

    def test_definition_without_template_args(self):
        def get_definition(definition, name, bitfield=""):
            class MockDataObject:
                def __init__(self, definition, name, bitfield):
                    self.definition = definition
                    self.name = name
                    self.bitfield = bitfield

            return get_definition_without_template_args(MockDataObject(definition, name, bitfield))

        self.assertEqual("void A::foo", get_definition("void A<T>::foo", "foo"))
        # Template arguments in the return type should be preserved:
        self.assertEqual("Result<T> A::f", get_definition("Result<T> A::f", "f"))
        # Nested template arguments:
        self.assertEqual("Result<T> A::f", get_definition("Result<T> A< B<C> >::f", "f"))

        # Bit fields
        self.assertEqual("int f : 3", get_definition("int f", "f", "3"))


class TestPathHandler(TestCase):
    def test_path_handler(self):
        self.assertEqual(path_handler.includes_directory("directory/file.h"), True)
        self.assertEqual(path_handler.includes_directory("directory\\file.h"), True)
        self.assertEqual(path_handler.includes_directory("file.h"), False)
