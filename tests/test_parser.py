import pytest
from breathe import parser


def test_bad_content():
    xml = """<?xml version='1.0' encoding='UTF-8' standalone='no'?>
        <doxygen version="1.9.8" xml:lang="en-US">
          <compounddef id="classSample" kind="class" language="C++" prot="public">
            <compoundname>Sample</compoundname>
            <includes local="no">sample.hpp</includes>
            <sectiondef kind="INVALID KIND">
              <memberdef kind="variable" id="classSample_1a16fb7dea2229144983e3a0ee85c42638" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int public_field</definition>
                <argsstring></argsstring>
                <name>public_field</name>
                <qualifiedname>Sample::public_field</qualifiedname>
                <location file="sample.hpp" line="3" column="9" bodyfile="sample.hpp" bodystart="3" bodyend="-1"/>
              </memberdef>
            </sectiondef>
            <location file="sample.hpp" line="1" column="1" bodyfile="sample.hpp" bodystart="1" bodyend="11"/>
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
              <memberdef kind="variable" id="classSample_1a16fb7dea2229144983e3a0ee85c42638" prot="public" static="no" mutable="no">
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
              <memberdef kind="variable" id="classSample_1a16fb7dea2229144983e3a0ee85c42638" prot="public" static="no" mutable="no">
                <type>int</type>
                <definition>int public_field</definition>
                <argsstring></argsstring>
                <name>public_field</name>
                <qualifiedname>Sample::public_field</qualifiedname>
                <location file="sample.hpp" line="3" column="9" bodyfile="sample.hpp" bodystart="3" bodyend="-1"/>
              </memberdef>
            </sectiondef>
            <location file="sample.hpp" line="1" column="1" bodyfile="sample.hpp" bodystart="1" bodyend="11"/>
          </compounddef>
        </doxygen>"""

    with pytest.warns(parser.ParseWarning) as record:
        parser.parse_str(xml)
    assert len(record) == 1
    assert "Warning on line 5:" in str(record[0].message)
