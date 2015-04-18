
from unittest import TestCase
from xml.dom import minidom

from breathe.renderer.rst.doxygen.compound import get_param_decl
from breathe.parser.doxygen.compoundsuper import memberdefType

class TestUtils(TestCase):

    def test_param_decl(self):

        # From declaration:
        #    int f(int (*p)[3]);
        # in: examples/specific/parameters.h
        xml = """
        <param>
          <type>int(*)</type>
          <declname>p</declname>
          <array>[3]</array>
        </param>
        """

        doc = minidom.parseString(xml)

        memberdef = memberdefType.factory()
        memberdef.buildChildren(doc.documentElement, 'param')

        self.assertEqual(get_param_decl(memberdef.param[0]), 'int(*p)[3]')
