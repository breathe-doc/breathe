from __future__ import annotations

import pytest

from breathe import parser


def test_bad_content():
    xml = """<?xml version='1.0' encoding='UTF-8' standalone='no'?>
        <doxygen version="1.9.8" xml:lang="en-US">
          <compounddef id="classSample" kind="class" language="C++" prot="public">
            <compoundname>Sample</compoundname>
            <includes local="no">sample.hpp</includes>
            <sectiondef kind="INVALID KIND">
              <memberdef kind="variable" id="1" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int public_field</definition>
                <argsstring></argsstring>
                <name>public_field</name>
                <qualifiedname>Sample::public_field</qualifiedname>
                <location file="sample.hpp"/>
              </memberdef>
            </sectiondef>
            <location file="sample.hpp" line="1"/>
          </compounddef>
        </doxygen>"""

    with pytest.raises(parser.ParseError) as exc:
        parser.parse_str(xml)
    assert exc.value.lineno == 6


def test_malformed():
    xml = """<?xml version='1.0' encoding='UTF-8' standalone='no'?>
        <doxygen version="1.9.8" xml:lang="en-US">
          <compounddef id="classSample" kind="class" language="C++" prot="public">
            <compoundname>Sample</compoundname>
            <includes local="no">sample.hpp</includes>
            <sectiondef kind="public-attrib">
              <memberdef kind="variable" id="1" prot="public" static="no" mutable="no">
                <type>int</type>"""

    with pytest.raises(parser.ParseError):
        parser.parse_str(xml)


def test_unknown_tag():
    xml = """<?xml version='1.0' encoding='UTF-8' standalone='no'?>
        <doxygen version="1.9.8" xml:lang="en-US">
          <compounddef id="classSample" kind="class" language="C++" prot="public">
            <compoundname>Sample</compoundname>
            <FAKE_TAG>
              <compoundname>Sample</compoundname>
            </FAKE_TAG>
            <includes local="no">sample.hpp</includes>
            <sectiondef kind="public-attrib">
              <memberdef kind="variable" id="1" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int public_field</definition>
                <argsstring></argsstring>
                <name>public_field</name>
                <qualifiedname>Sample::public_field</qualifiedname>
                <location file="sample.hpp" line="3"/>
              </memberdef>
            </sectiondef>
            <location file="sample.hpp" line="1"/>
          </compounddef>
        </doxygen>"""

    with pytest.warns(parser.ParseWarning) as record:
        parser.parse_str(xml)
    assert len(record) == 1
    assert "Warning on line 5:" in str(record[0].message)


def test_string_coalesce():
    xml = """<?xml version='1.0' encoding='UTF-8' standalone='no'?>
        <doxygen version="1.9.8" xml:lang="en-US">
          <compounddef id="classSample" kind="class" language="C++" prot="public">
            <compoundname>Sample</compoundname>
            <includes local="no">sample.hpp</includes>
            <sectiondef kind="public-attrib">
              <memberdef kind="variable" id="1" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int a</definition>
                <argsstring></argsstring>
                <name>a</name>
                <qualifiedname>Sample::a</qualifiedname>
                <detaileddescription><para>a<nonbreakablespace/>b</para></detaileddescription>
                <location file="sample.hpp" line="3"/>
              </memberdef>
              <memberdef kind="variable" id="2" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int b</definition>
                <argsstring></argsstring>
                <name>b</name>
                <qualifiedname>Sample::b</qualifiedname>
                <detaileddescription><para><trademark/>c<plusmn/></para></detaileddescription>
                <location file="sample.hpp" line="3"/>
              </memberdef>
            </sectiondef>
            <location file="sample.hpp" line="1"/>
          </compounddef>
        </doxygen>"""

    doc = parser.parse_str(xml).value
    assert isinstance(doc, parser.Node_DoxygenType)
    members = doc.compounddef[0].sectiondef[0].memberdef
    desc1 = members[0].detaileddescription
    desc2 = members[1].detaileddescription
    assert desc1 is not None
    assert desc2 is not None
    tv1 = desc1[0]
    tv2 = desc2[0]
    assert isinstance(tv1, parser.TaggedValue)
    assert isinstance(tv2, parser.TaggedValue)
    p1 = tv1.value
    p2 = tv2.value
    assert isinstance(p1, parser.Node_docParaType)
    assert isinstance(p2, parser.Node_docParaType)
    assert len(p1) == 1
    assert len(p2) == 1
    assert p1[0] == "a\N{NO-BREAK SPACE}b"
    assert p2[0] == "\N{TRADE MARK SIGN}c\N{PLUS-MINUS SIGN}"
