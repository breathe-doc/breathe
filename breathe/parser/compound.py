#!/usr/bin/env python

#
# Generated Tue Feb 21 16:56:51 2023 by generateDS.py version 2.41.1.
# Python 3.10.9 (main, Dec  7 2022, 13:47:07) [GCC 12.2.0]
#
# Command line options:
#   ('-o', 'compoundsuper2.py')
#   ('-s', 'compound_sample.py')
#
# Command line arguments:
#   compound.xsd
#
# Command line:
#   generateDS -o "compoundsuper.py" -s "compound_sample.py" compound.xsd
#
# Current working directory (os.getcwd()):
#   parser
#

import os
import sys
from lxml import etree as etree_

from . import compoundsuper as supermod
from .compoundsuper import MixedContainer

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class DoxygenTypeSub(supermod.DoxygenType):
    def __init__(self, version=None, lang=None, compounddef=None, **kwargs_):
        super(DoxygenTypeSub, self).__init__(version, lang, compounddef,  **kwargs_)
supermod.DoxygenType.subclass = DoxygenTypeSub
# end class DoxygenTypeSub


class compounddefTypeSub(supermod.compounddefType):
    def __init__(self, id=None, kind=None, language=None, prot=None, final=None, inline=None, sealed=None, abstract=None, compoundname=None, title=None, basecompoundref=None, derivedcompoundref=None, includes=None, includedby=None, incdepgraph=None, invincdepgraph=None, innerdir=None, innerfile=None, innerclass=None, innerconcept=None, innernamespace=None, innerpage=None, innergroup=None, qualifier=None, templateparamlist=None, sectiondef=None, tableofcontents=None, requiresclause=None, initializer=None, briefdescription=None, detaileddescription=None, inheritancegraph=None, collaborationgraph=None, programlisting=None, location=None, listofallmembers=None, **kwargs_):
        super(compounddefTypeSub, self).__init__(id, kind, language, prot, final, inline, sealed, abstract, compoundname, title, basecompoundref, derivedcompoundref, includes, includedby, incdepgraph, invincdepgraph, innerdir, innerfile, innerclass, innerconcept, innernamespace, innerpage, innergroup, qualifier, templateparamlist, sectiondef, tableofcontents, requiresclause, initializer, briefdescription, detaileddescription, inheritancegraph, collaborationgraph, programlisting, location, listofallmembers,  **kwargs_)
supermod.compounddefType.subclass = compounddefTypeSub
# end class compounddefTypeSub


class listofallmembersTypeSub(supermod.listofallmembersType):
    def __init__(self, member=None, **kwargs_):
        super(listofallmembersTypeSub, self).__init__(member,  **kwargs_)
supermod.listofallmembersType.subclass = listofallmembersTypeSub
# end class listofallmembersTypeSub


class memberRefTypeSub(supermod.memberRefType):
    def __init__(self, refid=None, prot=None, virt=None, ambiguityscope=None, scope=None, name=None, **kwargs_):
        super(memberRefTypeSub, self).__init__(refid, prot, virt, ambiguityscope, scope, name,  **kwargs_)
supermod.memberRefType.subclass = memberRefTypeSub
# end class memberRefTypeSub


class docHtmlOnlyTypeSub(supermod.docHtmlOnlyType):
    def __init__(self, block=None, valueOf_=None, **kwargs_):
        super(docHtmlOnlyTypeSub, self).__init__(block, valueOf_,  **kwargs_)
supermod.docHtmlOnlyType.subclass = docHtmlOnlyTypeSub
# end class docHtmlOnlyTypeSub


class compoundRefTypeSub(supermod.compoundRefType):
    def __init__(self, refid=None, prot=None, virt=None, valueOf_=None, **kwargs_):
        super(compoundRefTypeSub, self).__init__(refid, prot, virt, valueOf_,  **kwargs_)
supermod.compoundRefType.subclass = compoundRefTypeSub
# end class compoundRefTypeSub


class reimplementTypeSub(supermod.reimplementType):
    def __init__(self, refid=None, valueOf_=None, **kwargs_):
        super(reimplementTypeSub, self).__init__(refid, valueOf_,  **kwargs_)
supermod.reimplementType.subclass = reimplementTypeSub
# end class reimplementTypeSub


class incTypeSub(supermod.incType):
    def __init__(self, refid=None, local=None, valueOf_=None, **kwargs_):
        super(incTypeSub, self).__init__(refid, local, valueOf_,  **kwargs_)
supermod.incType.subclass = incTypeSub
# end class incTypeSub


class refTypeSub(supermod.refType):
    def __init__(self, refid=None, prot=None, inline=None, valueOf_=None, **kwargs_):
        super(refTypeSub, self).__init__(refid, prot, inline, valueOf_,  **kwargs_)
supermod.refType.subclass = refTypeSub
# end class refTypeSub


class refTextTypeSub(supermod.refTextType):
    def __init__(self, refid=None, kindref=None, external=None, tooltip=None, valueOf_=None, **kwargs_):
        super(refTextTypeSub, self).__init__(refid, kindref, external, tooltip, valueOf_,  **kwargs_)
supermod.refTextType.subclass = refTextTypeSub
# end class refTextTypeSub


class MemberTypeSub(supermod.MemberType):
    def __init__(self, refid=None, kind=None, name=None, **kwargs_):
        super(MemberTypeSub, self).__init__(refid, kind, name,  **kwargs_)
supermod.MemberType.subclass = MemberTypeSub
# end class MemberTypeSub


class sectiondefTypeSub(supermod.sectiondefType):
    def __init__(self, kind=None, header=None, description=None, memberdef=None, member=None, **kwargs_):
        super(sectiondefTypeSub, self).__init__(kind, header, description, memberdef, member,  **kwargs_)
supermod.sectiondefType.subclass = sectiondefTypeSub
# end class sectiondefTypeSub


class memberdefTypeSub(supermod.memberdefType):
    def __init__(self, kind=None, id=None, prot=None, static=None, strong=None, const=None, explicit=None, inline=None, refqual=None, virt=None, volatile=None, mutable=None, noexcept=None, constexpr=None, readable=None, writable=None, initonly=None, settable=None, privatesettable=None, protectedsettable=None, gettable=None, privategettable=None, protectedgettable=None, final=None, sealed=None, new=None, add=None, remove=None, raise_=None, optional=None, required=None, accessor=None, attribute=None, property=None, readonly=None, bound=None, removable=None, constrained=None, transient=None, maybevoid=None, maybedefault=None, maybeambiguous=None, templateparamlist=None, type_=None, definition=None, argsstring=None, name=None, qualifiedname=None, read=None, write=None, bitfield=None, reimplements=None, reimplementedby=None, qualifier=None, param=None, enumvalue=None, requiresclause=None, initializer=None, exceptions=None, briefdescription=None, detaileddescription=None, inbodydescription=None, location=None, references=None, referencedby=None, **kwargs_):
        super(memberdefTypeSub, self).__init__(kind, id, prot, static, strong, const, explicit, inline, refqual, virt, volatile, mutable, noexcept, constexpr, readable, writable, initonly, settable, privatesettable, protectedsettable, gettable, privategettable, protectedgettable, final, sealed, new, add, remove, raise_, optional, required, accessor, attribute, property, readonly, bound, removable, constrained, transient, maybevoid, maybedefault, maybeambiguous, templateparamlist, type_, definition, argsstring, name, qualifiedname, read, write, bitfield, reimplements, reimplementedby, qualifier, param, enumvalue, requiresclause, initializer, exceptions, briefdescription, detaileddescription, inbodydescription, location, references, referencedby,  **kwargs_)

        self.parameterlist = supermod.docParamListType.factory()
        self.parameterlist.kind = 'param'

    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(memberdefTypeSub, self)._buildChildren(child_, node, nodeName_)

        # if child_.text:
        #     return
        if nodeName_ == 'param':

            # Get latest param
            param = None
            if not self.param:
                return
            param = self.param[-1]


            # If it doesn't have a description we're done
            if not param.briefdescription:
                return

            # Construct our own param list from the descriptions stored inline
            # with the parameters
            paramdescription = param.briefdescription
            paramname = supermod.docParamName.factory()

            # Add parameter name
            obj_ = paramname.mixedclass_(MixedContainer.CategoryText, MixedContainer.TypeNone, '',
                                         param.declname)
            paramname.content_.append(obj_)

            paramnamelist = supermod.docParamNameList.factory()
            paramnamelist.parametername.append(paramname)

            paramlistitem = supermod.docParamListItem.factory()
            paramlistitem.parameternamelist.append(paramnamelist)

            # Add parameter description
            paramlistitem.parameterdescription = paramdescription

            self.parameterlist.parameteritem.append(paramlistitem)

        elif nodeName_ == 'detaileddescription':

            if not self.parameterlist.parameteritem:
                # No items in our list
                return

            # Assume supermod.memberdefType.buildChildren has already built the
            # description object, we just want to slot our parameterlist in at
            # a reasonable point

            if not self.detaileddescription:
                # Create one if it doesn't exist
                self.detaileddescription = supermod.descriptionType.factory()

            detaileddescription = self.detaileddescription

            para = supermod.docParaType.factory()
            para.parameterlist.append(self.parameterlist)

            obj_ = detaileddescription.mixedclass_(MixedContainer.CategoryComplex,
                                                   MixedContainer.TypeNone, 'para', para)

            index = 0
            detaileddescription.content_.insert(index, obj_)

supermod.memberdefType.subclass = memberdefTypeSub
# end class memberdefTypeSub


class descriptionTypeSub(supermod.descriptionType):
    def __init__(self, title=None, para=None, internal=None, sect1=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(descriptionTypeSub, self).__init__(title, para, internal, sect1, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.descriptionType.subclass = descriptionTypeSub
# end class descriptionTypeSub


class enumvalueTypeSub(supermod.enumvalueType):
    def __init__(self, id=None, prot=None, name=None, initializer=None, briefdescription=None, detaileddescription=None, **kwargs_):
        super(enumvalueTypeSub, self).__init__(id, prot, name, initializer, briefdescription, detaileddescription,  **kwargs_)
supermod.enumvalueType.subclass = enumvalueTypeSub
# end class enumvalueTypeSub


class templateparamlistTypeSub(supermod.templateparamlistType):
    def __init__(self, param=None, **kwargs_):
        super(templateparamlistTypeSub, self).__init__(param,  **kwargs_)
supermod.templateparamlistType.subclass = templateparamlistTypeSub
# end class templateparamlistTypeSub


class paramTypeSub(supermod.paramType):
    def __init__(self, attributes=None, type_=None, declname=None, defname=None, array=None, defval=None, typeconstraint=None, briefdescription=None, **kwargs_):
        super(paramTypeSub, self).__init__(attributes, type_, declname, defname, array, defval, typeconstraint, briefdescription,  **kwargs_)
supermod.paramType.subclass = paramTypeSub
# end class paramTypeSub


class linkedTextTypeSub(supermod.linkedTextType):
    def __init__(self, ref=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(linkedTextTypeSub, self).__init__(ref, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.linkedTextType.subclass = linkedTextTypeSub
# end class linkedTextTypeSub


class graphTypeSub(supermod.graphType):
    def __init__(self, node=None, **kwargs_):
        super(graphTypeSub, self).__init__(node,  **kwargs_)
supermod.graphType.subclass = graphTypeSub
# end class graphTypeSub


class nodeTypeSub(supermod.nodeType):
    def __init__(self, id=None, label=None, link=None, childnode=None, **kwargs_):
        super(nodeTypeSub, self).__init__(id, label, link, childnode,  **kwargs_)
supermod.nodeType.subclass = nodeTypeSub
# end class nodeTypeSub


class childnodeTypeSub(supermod.childnodeType):
    def __init__(self, refid=None, relation=None, edgelabel=None, **kwargs_):
        super(childnodeTypeSub, self).__init__(refid, relation, edgelabel,  **kwargs_)
supermod.childnodeType.subclass = childnodeTypeSub
# end class childnodeTypeSub


class linkTypeSub(supermod.linkType):
    def __init__(self, refid=None, external=None, **kwargs_):
        super(linkTypeSub, self).__init__(refid, external,  **kwargs_)
supermod.linkType.subclass = linkTypeSub
# end class linkTypeSub


class listingTypeSub(supermod.listingType):
    def __init__(self, filename=None, codeline=None, **kwargs_):
        super(listingTypeSub, self).__init__(filename, codeline,  **kwargs_)
supermod.listingType.subclass = listingTypeSub
# end class listingTypeSub


class codelineTypeSub(supermod.codelineType):
    def __init__(self, lineno=None, refid=None, refkind=None, external=None, highlight=None, **kwargs_):
        super(codelineTypeSub, self).__init__(lineno, refid, refkind, external, highlight,  **kwargs_)
supermod.codelineType.subclass = codelineTypeSub
# end class codelineTypeSub


class highlightTypeSub(supermod.highlightType):
    def __init__(self, class_=None, sp=None, ref=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(highlightTypeSub, self).__init__(class_, sp, ref, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.highlightType.subclass = highlightTypeSub
# end class highlightTypeSub


class spTypeSub(supermod.spType):
    def __init__(self, value=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(spTypeSub, self).__init__(value, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.spType.subclass = spTypeSub
# end class spTypeSub


class referenceTypeSub(supermod.referenceType):
    def __init__(self, refid=None, compoundref=None, startline=None, endline=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(referenceTypeSub, self).__init__(refid, compoundref, startline, endline, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.referenceType.subclass = referenceTypeSub
# end class referenceTypeSub


class locationTypeSub(supermod.locationType):
    def __init__(self, file=None, line=None, column=None, declfile=None, declline=None, declcolumn=None, bodyfile=None, bodystart=None, bodyend=None, **kwargs_):
        super(locationTypeSub, self).__init__(file, line, column, declfile, declline, declcolumn, bodyfile, bodystart, bodyend,  **kwargs_)
supermod.locationType.subclass = locationTypeSub
# end class locationTypeSub


class docSect1TypeSub(supermod.docSect1Type):
    def __init__(self, id=None, title=None, para=None, internal=None, sect2=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docSect1TypeSub, self).__init__(id, title, para, internal, sect2, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docSect1Type.subclass = docSect1TypeSub
# end class docSect1TypeSub


class docSect2TypeSub(supermod.docSect2Type):
    def __init__(self, id=None, title=None, para=None, sect3=None, internal=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docSect2TypeSub, self).__init__(id, title, para, sect3, internal, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docSect2Type.subclass = docSect2TypeSub
# end class docSect2TypeSub


class docSect3TypeSub(supermod.docSect3Type):
    def __init__(self, id=None, title=None, para=None, sect4=None, internal=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docSect3TypeSub, self).__init__(id, title, para, sect4, internal, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docSect3Type.subclass = docSect3TypeSub
# end class docSect3TypeSub


class docSect4TypeSub(supermod.docSect4Type):
    def __init__(self, id=None, title=None, para=None, internal=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docSect4TypeSub, self).__init__(id, title, para, internal, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docSect4Type.subclass = docSect4TypeSub
# end class docSect4TypeSub


class docInternalTypeSub(supermod.docInternalType):
    def __init__(self, para=None, sect1=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docInternalTypeSub, self).__init__(para, sect1, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docInternalType.subclass = docInternalTypeSub
# end class docInternalTypeSub


class docInternalS1TypeSub(supermod.docInternalS1Type):
    def __init__(self, para=None, sect2=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docInternalS1TypeSub, self).__init__(para, sect2, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docInternalS1Type.subclass = docInternalS1TypeSub
# end class docInternalS1TypeSub


class docInternalS2TypeSub(supermod.docInternalS2Type):
    def __init__(self, para=None, sect3=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docInternalS2TypeSub, self).__init__(para, sect3, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docInternalS2Type.subclass = docInternalS2TypeSub
# end class docInternalS2TypeSub


class docInternalS3TypeSub(supermod.docInternalS3Type):
    def __init__(self, para=None, sect3=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docInternalS3TypeSub, self).__init__(para, sect3, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docInternalS3Type.subclass = docInternalS3TypeSub
# end class docInternalS3TypeSub


class docInternalS4TypeSub(supermod.docInternalS4Type):
    def __init__(self, para=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docInternalS4TypeSub, self).__init__(para, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docInternalS4Type.subclass = docInternalS4TypeSub
# end class docInternalS4TypeSub


class docTitleTypeSub(supermod.docTitleType):
    def __init__(self, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docTitleTypeSub, self).__init__(ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
        self.type_ = None

    def build(self, child_, nodeName_):
        super(docTitleTypeSub, self).build(child_, nodeName_)

        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "ref":
            obj_ = supermod.docRefTextType.factory()
            obj_.build(child_)
            self.content_.append(obj_)
            self.valueOf_ += obj_.valueOf_
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "anchor":
            obj_ = supermod.docAnchorType.factory()
            obj_.build(child_)
            self.content_.append(obj_)

supermod.docTitleType.subclass = docTitleTypeSub
# end class docTitleTypeSub


class docSummaryTypeSub(supermod.docSummaryType):
    def __init__(self, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docSummaryTypeSub, self).__init__(ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docSummaryType.subclass = docSummaryTypeSub
# end class docSummaryTypeSub


class docParaTypeSub(supermod.docParaType):
    def __init__(self, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, hruler=None, preformatted=None, programlisting=None, verbatim=None, javadocliteral=None, javadoccode=None, indexentry=None, orderedlist=None, itemizedlist=None, simplesect=None, title=None, variablelist=None, table=None, heading=None, dotfile=None, mscfile=None, diafile=None, toclist=None, language=None, parameterlist=None, xrefsect=None, copydoc=None, details=None, blockquote=None, parblock=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docParaTypeSub, self).__init__(ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, hruler, preformatted, programlisting, verbatim, javadocliteral, javadoccode, indexentry, orderedlist, itemizedlist, simplesect, title, variablelist, table, heading, dotfile, mscfile, diafile, toclist, language, parameterlist, xrefsect, copydoc, details, blockquote, parblock, valueOf_, mixedclass_, content_,  **kwargs_)

        self.parameterlist = []
        self.simplesects = []
        self.content = []
        self.programlisting = []
        self.images = []

        self.ordered_children = []

    def build(self, child_, nodeName_):
        import ipdb; ipdb.set_trace()  # type: ignore # pylint: disable=import-outside-toplevel,multiple-statements
        super(docParaTypeSub, self).build(child_, nodeName_)

        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                                    MixedContainer.TypeNone, '', child_.nodeValue)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "ref":
            obj_ = supermod.docRefTextType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'parameterlist':
            obj_ = supermod.docParamListType.factory()
            obj_.build(child_)
            self.parameterlist.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'simplesect':
            obj_ = supermod.docSimpleSectType.factory()
            obj_.build(child_)
            self.simplesects.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'programlisting':
            obj_ = supermod.listingType.factory()
            obj_.build(child_)
            # Add programlisting nodes to self.content rather than self.programlisting,
            # because programlisting and content nodes can interleave as shown in
            # https://www.stack.nl/~dimitri/doxygen/manual/examples/include/html/example.html.
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'image':
            obj_ = supermod.docImageType.factory()
            obj_.build(child_)
            self.images.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and (
                nodeName_ == 'bold' or
                nodeName_ == 'emphasis' or
                nodeName_ == 'computeroutput' or
                nodeName_ == 'subscript' or
                nodeName_ == 'superscript' or
                nodeName_ == 'center' or
                nodeName_ == 'small'):
            obj_ = supermod.docMarkupType.factory()
            obj_.build(child_)
            obj_.type_ = nodeName_
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'verbatim':
            childobj_ = verbatimTypeSub.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone,
                                    'verbatim', childobj_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'formula':
            childobj_ = docFormulaTypeSub.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone,
                                    'formula', childobj_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "itemizedlist":
            obj_ = supermod.docListType.factory(subtype="itemized")
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "orderedlist":
            obj_ = supermod.docListType.factory(subtype="ordered")
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'heading':
            obj_ = supermod.docHeadingType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'ulink':
            obj_ = supermod.docURLLink.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "xrefsect":
            obj_ = supermod.docXRefSectType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "variablelist":
            obj_ = supermod.docVariableListType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "anchor":
            obj_ = supermod.docAnchorType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "parblock":
            obj_ = supermod.docParBlockType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "blockquote":
            obj_ = supermod.docBlockQuoteType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "table":
            obj_ = supermod.docTableType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "dotfile":
            obj_ = supermod.docDotFileType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "dot":
            obj_ = supermod.docDotType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and (
            nodeName_ == "ndash" or nodeName_ == "mdash"
        ):
            # inject a emphasized dash unicode char as a placeholder/flag for rendering
            # later. See visit_docblockquote()
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                                    MixedContainer.TypeText, "", "&#8212;")
            self.content.append(obj_)
        else:
            obj_ = None

        if obj_:
            self.ordered_children.append(obj_)

supermod.docParaType.subclass = docParaTypeSub
# end class docParaTypeSub


class docMarkupTypeSub(supermod.docMarkupType):
    def __init__(self, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, hruler=None, preformatted=None, programlisting=None, verbatim=None, javadocliteral=None, javadoccode=None, indexentry=None, orderedlist=None, itemizedlist=None, simplesect=None, title=None, variablelist=None, table=None, heading=None, dotfile=None, mscfile=None, diafile=None, toclist=None, language=None, parameterlist=None, xrefsect=None, copydoc=None, details=None, blockquote=None, parblock=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docMarkupTypeSub, self).__init__(ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, hruler, preformatted, programlisting, verbatim, javadocliteral, javadoccode, indexentry, orderedlist, itemizedlist, simplesect, title, variablelist, table, heading, dotfile, mscfile, diafile, toclist, language, parameterlist, xrefsect, copydoc, details, blockquote, parblock, valueOf_, mixedclass_, content_,  **kwargs_)

        self.type_ = None

    def build(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText, MixedContainer.TypeNone, '',
                                    child_.nodeValue)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'ref':
            childobj_ = supermod.docRefTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone, 'ref',
                                    childobj_)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
        elif child_.nodeType == Node.CDATA_SECTION_NODE:
            self.valueOf_ += '![CDATA[' + child_.nodeValue + ']]'

supermod.docMarkupType.subclass = docMarkupTypeSub
# end class docMarkupTypeSub


class docURLLinkSub(supermod.docURLLink):
    def __init__(self, url=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docURLLinkSub, self).__init__(url, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docURLLink.subclass = docURLLinkSub
# end class docURLLinkSub


class docAnchorTypeSub(supermod.docAnchorType):
    def __init__(self, id=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docAnchorTypeSub, self).__init__(id, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docAnchorType.subclass = docAnchorTypeSub
# end class docAnchorTypeSub


class docFormulaTypeSub(supermod.docFormulaType):
    def __init__(self, id=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docFormulaTypeSub, self).__init__(id, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docFormulaType.subclass = docFormulaTypeSub
# end class docFormulaTypeSub


class docIndexEntryTypeSub(supermod.docIndexEntryType):
    def __init__(self, primaryie=None, secondaryie=None, **kwargs_):
        super(docIndexEntryTypeSub, self).__init__(primaryie, secondaryie,  **kwargs_)
supermod.docIndexEntryType.subclass = docIndexEntryTypeSub
# end class docIndexEntryTypeSub


class docListTypeSub(supermod.docListType):
    def __init__(self, type_=None, start=None, listitem=None, **kwargs_):
        super(docListTypeSub, self).__init__(type_, start, listitem,  **kwargs_)
supermod.docListType.subclass = docListTypeSub
# end class docListTypeSub


class docListItemTypeSub(supermod.docListItemType):
    def __init__(self, value=None, para=None, **kwargs_):
        super(docListItemTypeSub, self).__init__(value, para,  **kwargs_)
supermod.docListItemType.subclass = docListItemTypeSub
# end class docListItemTypeSub


class docSimpleSectTypeSub(supermod.docSimpleSectType):
    def __init__(self, kind=None, title=None, para=None, **kwargs_):
        super(docSimpleSectTypeSub, self).__init__(kind, title, para,  **kwargs_)
supermod.docSimpleSectType.subclass = docSimpleSectTypeSub
# end class docSimpleSectTypeSub


class docVarListEntryTypeSub(supermod.docVarListEntryType):
    def __init__(self, term=None, **kwargs_):
        super(docVarListEntryTypeSub, self).__init__(term,  **kwargs_)

    def build(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'term':
            obj_ = supermod.docTitleType.factory()
            obj_.build(child_)
            self.set_term(obj_)

supermod.docVarListEntryType.subclass = docVarListEntryTypeSub
# end class docVarListEntryTypeSub


class docVariableListTypeSub(supermod.docVariableListType):
    def __init__(self, varlistentry=None, listitem=None, **kwargs_):
        super(docVariableListTypeSub, self).__init__(varlistentry, listitem,  **kwargs_)

        self.varlistentries = []
        self.listitems = []

    def build(self, child_, nodeName_):
        super(docVariableListType, self).build(child_, nodeName_)

        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "varlistentry":
            obj_ = supermod.docVarListEntryType.factory()
            obj_.build(child_)
            self.varlistentries.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "listitem":
            obj_ = supermod.docListItemType.factory()
            obj_.build(child_)
            self.listitems.append(obj_)

supermod.docVariableListType.subclass = docVariableListTypeSub
# end class docVariableListTypeSub


class docRefTextTypeSub(supermod.docRefTextType):
    def __init__(self, refid=None, kindref=None, external=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docRefTextTypeSub, self).__init__(refid, kindref, external, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)

        self.para = []

    def build(self, child_, nodeName_):
        super(docRefTextType, self).build(child_, nodeName_)

        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'para':
            obj_ = supermod.docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)

supermod.docRefTextType.subclass = docRefTextTypeSub
# end class docRefTextTypeSub


class docTableTypeSub(supermod.docTableType):
    def __init__(self, rows=None, cols=None, width=None, caption=None, row=None, **kwargs_):
        super(docTableTypeSub, self).__init__(rows, cols, width, caption, row,  **kwargs_)
supermod.docTableType.subclass = docTableTypeSub
# end class docTableTypeSub


class docRowTypeSub(supermod.docRowType):
    def __init__(self, entry=None, **kwargs_):
        super(docRowTypeSub, self).__init__(entry,  **kwargs_)
supermod.docRowType.subclass = docRowTypeSub
# end class docRowTypeSub


class docEntryTypeSub(supermod.docEntryType):
    def __init__(self, thead=None, colspan=None, rowspan=None, align=None, valign=None, width=None, class_=None, para=None, **kwargs_):
        super(docEntryTypeSub, self).__init__(thead, colspan, rowspan, align, valign, width, class_, para,  **kwargs_)
supermod.docEntryType.subclass = docEntryTypeSub
# end class docEntryTypeSub


class docCaptionTypeSub(supermod.docCaptionType):
    def __init__(self, id=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docCaptionTypeSub, self).__init__(id, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docCaptionType.subclass = docCaptionTypeSub
# end class docCaptionTypeSub


class docHeadingTypeSub(supermod.docHeadingType):
    def __init__(self, level=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docHeadingTypeSub, self).__init__(level, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)

    def build(self, child_, nodeName_):
        super(docHeadingTypeSub, self).build(child_, nodeName_)

        # Account for styled content in the heading. This might need to be expanded to include other
        # nodes as it seems from the xsd that headings can have a lot of different children but we
        # really don't expect most of them to come up.
        if child_.nodeType == Node.ELEMENT_NODE and (
                nodeName_ == 'bold' or
                nodeName_ == 'emphasis' or
                nodeName_ == 'computeroutput' or
                nodeName_ == 'subscript' or
                nodeName_ == 'superscript' or
                nodeName_ == 'center' or
                nodeName_ == 'small'):
            obj_ = supermod.docMarkupType.factory()
            obj_.build(child_)
            obj_.type_ = nodeName_
            self.content_.append(obj_)

supermod.docHeadingType.subclass = docHeadingTypeSub
# end class docHeadingTypeSub


class docImageTypeSub(supermod.docImageType):
    def __init__(self, type_=None, name=None, width=None, height=None, alt=None, inline=None, caption=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docImageTypeSub, self).__init__(type_, name, width, height, alt, inline, caption, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docImageType.subclass = docImageTypeSub
# end class docImageTypeSub


class docDotMscTypeSub(supermod.docDotMscType):
    def __init__(self, name=None, width=None, height=None, caption=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docDotMscTypeSub, self).__init__(name, width, height, caption, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docDotMscType.subclass = docDotMscTypeSub
# end class docDotMscTypeSub


class docImageFileTypeSub(supermod.docImageFileType):
    def __init__(self, name=None, width=None, height=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docImageFileTypeSub, self).__init__(name, width, height, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docImageFileType.subclass = docImageFileTypeSub
# end class docImageFileTypeSub


class docPlantumlTypeSub(supermod.docPlantumlType):
    def __init__(self, name=None, width=None, height=None, caption=None, engine=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docPlantumlTypeSub, self).__init__(name, width, height, caption, engine, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docPlantumlType.subclass = docPlantumlTypeSub
# end class docPlantumlTypeSub


class docTocItemTypeSub(supermod.docTocItemType):
    def __init__(self, id=None, ulink=None, bold=None, s=None, strike=None, underline=None, emphasis=None, computeroutput=None, subscript=None, superscript=None, center=None, small=None, cite=None, del_=None, ins=None, htmlonly=None, manonly=None, xmlonly=None, rtfonly=None, latexonly=None, docbookonly=None, image=None, dot=None, msc=None, plantuml=None, anchor=None, formula=None, ref=None, emoji=None, linebreak=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docTocItemTypeSub, self).__init__(id, ulink, bold, s, strike, underline, emphasis, computeroutput, subscript, superscript, center, small, cite, del_, ins, htmlonly, manonly, xmlonly, rtfonly, latexonly, docbookonly, image, dot, msc, plantuml, anchor, formula, ref, emoji, linebreak, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docTocItemType.subclass = docTocItemTypeSub
# end class docTocItemTypeSub


class docTocListTypeSub(supermod.docTocListType):
    def __init__(self, tocitem=None, **kwargs_):
        super(docTocListTypeSub, self).__init__(tocitem,  **kwargs_)
supermod.docTocListType.subclass = docTocListTypeSub
# end class docTocListTypeSub


class docLanguageTypeSub(supermod.docLanguageType):
    def __init__(self, langid=None, para=None, **kwargs_):
        super(docLanguageTypeSub, self).__init__(langid, para,  **kwargs_)
supermod.docLanguageType.subclass = docLanguageTypeSub
# end class docLanguageTypeSub


class docParamListTypeSub(supermod.docParamListType):
    def __init__(self, kind=None, parameteritem=None, **kwargs_):
        super(docParamListTypeSub, self).__init__(kind, parameteritem,  **kwargs_)
supermod.docParamListType.subclass = docParamListTypeSub
# end class docParamListTypeSub


class docParamListItemSub(supermod.docParamListItem):
    def __init__(self, parameternamelist=None, parameterdescription=None, **kwargs_):
        super(docParamListItemSub, self).__init__(parameternamelist, parameterdescription,  **kwargs_)
supermod.docParamListItem.subclass = docParamListItemSub
# end class docParamListItemSub


class docParamNameListSub(supermod.docParamNameList):
    def __init__(self, parametertype=None, parametername=None, **kwargs_):
        super(docParamNameListSub, self).__init__(parametertype, parametername,  **kwargs_)
supermod.docParamNameList.subclass = docParamNameListSub
# end class docParamNameListSub


class docParamTypeSub(supermod.docParamType):
    def __init__(self, ref=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docParamTypeSub, self).__init__(ref, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docParamType.subclass = docParamTypeSub
# end class docParamTypeSub


class docParamNameSub(supermod.docParamName):
    def __init__(self, direction=None, ref=None, valueOf_=None, mixedclass_=None, content_=None, **kwargs_):
        super(docParamNameSub, self).__init__(direction, ref, valueOf_, mixedclass_, content_,  **kwargs_)
supermod.docParamName.subclass = docParamNameSub
# end class docParamNameSub


class docXRefSectTypeSub(supermod.docXRefSectType):
    def __init__(self, id=None, xreftitle=None, xrefdescription=None, **kwargs_):
        super(docXRefSectTypeSub, self).__init__(id, xreftitle, xrefdescription,  **kwargs_)
supermod.docXRefSectType.subclass = docXRefSectTypeSub
# end class docXRefSectTypeSub


class docCopyTypeSub(supermod.docCopyType):
    def __init__(self, link=None, para=None, sect1=None, internal=None, **kwargs_):
        super(docCopyTypeSub, self).__init__(link, para, sect1, internal,  **kwargs_)
supermod.docCopyType.subclass = docCopyTypeSub
# end class docCopyTypeSub


class docDetailsTypeSub(supermod.docDetailsType):
    def __init__(self, summary=None, para=None, **kwargs_):
        super(docDetailsTypeSub, self).__init__(summary, para,  **kwargs_)
supermod.docDetailsType.subclass = docDetailsTypeSub
# end class docDetailsTypeSub


class docBlockQuoteTypeSub(supermod.docBlockQuoteType):
    def __init__(self, para=None, **kwargs_):
        super(docBlockQuoteTypeSub, self).__init__(para,  **kwargs_)
supermod.docBlockQuoteType.subclass = docBlockQuoteTypeSub
# end class docBlockQuoteTypeSub


class docParBlockTypeSub(supermod.docParBlockType):
    def __init__(self, para=None, **kwargs_):
        super(docParBlockTypeSub, self).__init__(para,  **kwargs_)
supermod.docParBlockType.subclass = docParBlockTypeSub
# end class docParBlockTypeSub


class docEmptyTypeSub(supermod.docEmptyType):
    def __init__(self, **kwargs_):
        super(docEmptyTypeSub, self).__init__( **kwargs_)
supermod.docEmptyType.subclass = docEmptyTypeSub
# end class docEmptyTypeSub


class tableofcontentsTypeSub(supermod.tableofcontentsType):
    def __init__(self, tocsect=None, **kwargs_):
        super(tableofcontentsTypeSub, self).__init__(tocsect,  **kwargs_)
supermod.tableofcontentsType.subclass = tableofcontentsTypeSub
# end class tableofcontentsTypeSub


class tableofcontentsKindTypeSub(supermod.tableofcontentsKindType):
    def __init__(self, name=None, reference=None, tableofcontents=None, **kwargs_):
        super(tableofcontentsKindTypeSub, self).__init__(name, reference, tableofcontents,  **kwargs_)
supermod.tableofcontentsKindType.subclass = tableofcontentsKindTypeSub
# end class tableofcontentsKindTypeSub


class docEmojiTypeSub(supermod.docEmojiType):
    def __init__(self, name=None, unicode=None, **kwargs_):
        super(docEmojiTypeSub, self).__init__(name, unicode,  **kwargs_)
supermod.docEmojiType.subclass = docEmojiTypeSub
# end class docEmojiTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DoxygenType'
        rootClass = supermod.DoxygenType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DoxygenType'
        rootClass = supermod.DoxygenType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DoxygenType'
        rootClass = supermod.DoxygenType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DoxygenType'
        rootClass = supermod.DoxygenType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
