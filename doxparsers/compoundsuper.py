#!/usr/bin/env python

#
# Generated Mon Feb  9 19:08:05 2009 by generateDS.py.
#

import sys
import getopt
from string import lower as str_lower
from xml.dom import minidom
from xml.dom import Node

#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('"', '&quot;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class _MemberSpec(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type(self): return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container


#
# Data representation classes.
#

class DoxygenType(object):
    subclass = None
    superclass = None
    def __init__(self, version=None, compounddef=None):
        self.version = version
        self.compounddef = compounddef
    def factory(*args_, **kwargs_):
        if DoxygenType.subclass:
            return DoxygenType.subclass(*args_, **kwargs_)
        else:
            return DoxygenType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_compounddef(self): return self.compounddef
    def set_compounddef(self, compounddef): self.compounddef = compounddef
    def get_version(self): return self.version
    def set_version(self, version): self.version = version
    def export(self, outfile, level, namespace_='', name_='DoxygenType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='DoxygenType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='DoxygenType'):
        outfile.write(' version="%s"' % str(self.get_version()))
    def exportChildren(self, outfile, level, namespace_='', name_='DoxygenType'):
        if self.get_compounddef() != None :
            if self.compounddef:
                self.compounddef.export(outfile, level, namespace_, name_='compounddef')
    def exportLiteral(self, outfile, level, name_='DoxygenType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('version = "%s",\n' % (self.get_version(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.compounddef:
            showIndent(outfile, level)
            outfile.write('compounddef=compounddefType(\n')
            self.compounddef.exportLiteral(outfile, level, name_='compounddef')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('version'):
            self.version = attrs.get('version').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'compounddef':
            obj_ = compounddefType.factory()
            obj_.build(child_)
            self.set_compounddef(obj_)
# end class DoxygenType


class compounddefType(object):
    subclass = None
    superclass = None
    def __init__(self, kind=None, prot=None, id=None, compoundname='', title='', basecompoundref=None, derivedcompoundref=None, includes=None, includedby=None, incdepgraph=None, invincdepgraph=None, innerdir=None, innerfile=None, innerclass=None, innernamespace=None, innerpage=None, innergroup=None, templateparamlist=None, sectiondef=None, briefdescription=None, detaileddescription=None, inheritancegraph=None, collaborationgraph=None, programlisting=None, location=None, listofallmembers=None):
        self.kind = kind
        self.prot = prot
        self.id = id
        self.compoundname = compoundname
        self.title = title
        if basecompoundref is None:
            self.basecompoundref = []
        else:
            self.basecompoundref = basecompoundref
        if derivedcompoundref is None:
            self.derivedcompoundref = []
        else:
            self.derivedcompoundref = derivedcompoundref
        if includes is None:
            self.includes = []
        else:
            self.includes = includes
        if includedby is None:
            self.includedby = []
        else:
            self.includedby = includedby
        self.incdepgraph = incdepgraph
        self.invincdepgraph = invincdepgraph
        if innerdir is None:
            self.innerdir = []
        else:
            self.innerdir = innerdir
        if innerfile is None:
            self.innerfile = []
        else:
            self.innerfile = innerfile
        if innerclass is None:
            self.innerclass = []
        else:
            self.innerclass = innerclass
        if innernamespace is None:
            self.innernamespace = []
        else:
            self.innernamespace = innernamespace
        if innerpage is None:
            self.innerpage = []
        else:
            self.innerpage = innerpage
        if innergroup is None:
            self.innergroup = []
        else:
            self.innergroup = innergroup
        self.templateparamlist = templateparamlist
        if sectiondef is None:
            self.sectiondef = []
        else:
            self.sectiondef = sectiondef
        self.briefdescription = briefdescription
        self.detaileddescription = detaileddescription
        self.inheritancegraph = inheritancegraph
        self.collaborationgraph = collaborationgraph
        self.programlisting = programlisting
        self.location = location
        self.listofallmembers = listofallmembers
    def factory(*args_, **kwargs_):
        if compounddefType.subclass:
            return compounddefType.subclass(*args_, **kwargs_)
        else:
            return compounddefType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_compoundname(self): return self.compoundname
    def set_compoundname(self, compoundname): self.compoundname = compoundname
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_basecompoundref(self): return self.basecompoundref
    def set_basecompoundref(self, basecompoundref): self.basecompoundref = basecompoundref
    def add_basecompoundref(self, value): self.basecompoundref.append(value)
    def insert_basecompoundref(self, index, value): self.basecompoundref[index] = value
    def get_derivedcompoundref(self): return self.derivedcompoundref
    def set_derivedcompoundref(self, derivedcompoundref): self.derivedcompoundref = derivedcompoundref
    def add_derivedcompoundref(self, value): self.derivedcompoundref.append(value)
    def insert_derivedcompoundref(self, index, value): self.derivedcompoundref[index] = value
    def get_includes(self): return self.includes
    def set_includes(self, includes): self.includes = includes
    def add_includes(self, value): self.includes.append(value)
    def insert_includes(self, index, value): self.includes[index] = value
    def get_includedby(self): return self.includedby
    def set_includedby(self, includedby): self.includedby = includedby
    def add_includedby(self, value): self.includedby.append(value)
    def insert_includedby(self, index, value): self.includedby[index] = value
    def get_incdepgraph(self): return self.incdepgraph
    def set_incdepgraph(self, incdepgraph): self.incdepgraph = incdepgraph
    def get_invincdepgraph(self): return self.invincdepgraph
    def set_invincdepgraph(self, invincdepgraph): self.invincdepgraph = invincdepgraph
    def get_innerdir(self): return self.innerdir
    def set_innerdir(self, innerdir): self.innerdir = innerdir
    def add_innerdir(self, value): self.innerdir.append(value)
    def insert_innerdir(self, index, value): self.innerdir[index] = value
    def get_innerfile(self): return self.innerfile
    def set_innerfile(self, innerfile): self.innerfile = innerfile
    def add_innerfile(self, value): self.innerfile.append(value)
    def insert_innerfile(self, index, value): self.innerfile[index] = value
    def get_innerclass(self): return self.innerclass
    def set_innerclass(self, innerclass): self.innerclass = innerclass
    def add_innerclass(self, value): self.innerclass.append(value)
    def insert_innerclass(self, index, value): self.innerclass[index] = value
    def get_innernamespace(self): return self.innernamespace
    def set_innernamespace(self, innernamespace): self.innernamespace = innernamespace
    def add_innernamespace(self, value): self.innernamespace.append(value)
    def insert_innernamespace(self, index, value): self.innernamespace[index] = value
    def get_innerpage(self): return self.innerpage
    def set_innerpage(self, innerpage): self.innerpage = innerpage
    def add_innerpage(self, value): self.innerpage.append(value)
    def insert_innerpage(self, index, value): self.innerpage[index] = value
    def get_innergroup(self): return self.innergroup
    def set_innergroup(self, innergroup): self.innergroup = innergroup
    def add_innergroup(self, value): self.innergroup.append(value)
    def insert_innergroup(self, index, value): self.innergroup[index] = value
    def get_templateparamlist(self): return self.templateparamlist
    def set_templateparamlist(self, templateparamlist): self.templateparamlist = templateparamlist
    def get_sectiondef(self): return self.sectiondef
    def set_sectiondef(self, sectiondef): self.sectiondef = sectiondef
    def add_sectiondef(self, value): self.sectiondef.append(value)
    def insert_sectiondef(self, index, value): self.sectiondef[index] = value
    def get_briefdescription(self): return self.briefdescription
    def set_briefdescription(self, briefdescription): self.briefdescription = briefdescription
    def get_detaileddescription(self): return self.detaileddescription
    def set_detaileddescription(self, detaileddescription): self.detaileddescription = detaileddescription
    def get_inheritancegraph(self): return self.inheritancegraph
    def set_inheritancegraph(self, inheritancegraph): self.inheritancegraph = inheritancegraph
    def get_collaborationgraph(self): return self.collaborationgraph
    def set_collaborationgraph(self, collaborationgraph): self.collaborationgraph = collaborationgraph
    def get_programlisting(self): return self.programlisting
    def set_programlisting(self, programlisting): self.programlisting = programlisting
    def get_location(self): return self.location
    def set_location(self, location): self.location = location
    def get_listofallmembers(self): return self.listofallmembers
    def set_listofallmembers(self, listofallmembers): self.listofallmembers = listofallmembers
    def get_kind(self): return self.kind
    def set_kind(self, kind): self.kind = kind
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='compounddefType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='compounddefType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='compounddefType'):
        if self.get_kind() is not None:
            outfile.write(' kind="%s"' % str(self.get_kind()))
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='compounddefType'):
        showIndent(outfile, level)
        outfile.write('<%scompoundname>%s</%scompoundname>\n' % (namespace_, quote_xml(self.get_compoundname()), namespace_))
        if self.get_title() != None :
            if self.get_title() != "" :
                showIndent(outfile, level)
                outfile.write('<%stitle>%s</%stitle>\n' % (namespace_, quote_xml(self.get_title()), namespace_))
        for basecompoundref_ in self.get_basecompoundref():
            basecompoundref_.export(outfile, level, namespace_, name_='basecompoundref')
        for derivedcompoundref_ in self.get_derivedcompoundref():
            derivedcompoundref_.export(outfile, level, namespace_, name_='derivedcompoundref')
        for includes_ in self.get_includes():
            includes_.export(outfile, level, namespace_, name_='includes')
        for includedby_ in self.get_includedby():
            includedby_.export(outfile, level, namespace_, name_='includedby')
        if self.get_incdepgraph() != None :
            if self.incdepgraph:
                self.incdepgraph.export(outfile, level, namespace_, name_='incdepgraph')
        if self.get_invincdepgraph() != None :
            if self.invincdepgraph:
                self.invincdepgraph.export(outfile, level, namespace_, name_='invincdepgraph')
        for innerdir_ in self.get_innerdir():
            innerdir_.export(outfile, level, namespace_, name_='innerdir')
        for innerfile_ in self.get_innerfile():
            innerfile_.export(outfile, level, namespace_, name_='innerfile')
        for innerclass_ in self.get_innerclass():
            innerclass_.export(outfile, level, namespace_, name_='innerclass')
        for innernamespace_ in self.get_innernamespace():
            innernamespace_.export(outfile, level, namespace_, name_='innernamespace')
        for innerpage_ in self.get_innerpage():
            innerpage_.export(outfile, level, namespace_, name_='innerpage')
        for innergroup_ in self.get_innergroup():
            innergroup_.export(outfile, level, namespace_, name_='innergroup')
        if self.get_templateparamlist() != None :
            if self.templateparamlist:
                self.templateparamlist.export(outfile, level, namespace_, name_='templateparamlist')
        for sectiondef_ in self.get_sectiondef():
            sectiondef_.export(outfile, level, namespace_, name_='sectiondef')
        if self.get_briefdescription() != None :
            if self.briefdescription:
                self.briefdescription.export(outfile, level, namespace_, name_='briefdescription')
        if self.get_detaileddescription() != None :
            if self.detaileddescription:
                self.detaileddescription.export(outfile, level, namespace_, name_='detaileddescription')
        if self.get_inheritancegraph() != None :
            if self.inheritancegraph:
                self.inheritancegraph.export(outfile, level, namespace_, name_='inheritancegraph')
        if self.get_collaborationgraph() != None :
            if self.collaborationgraph:
                self.collaborationgraph.export(outfile, level, namespace_, name_='collaborationgraph')
        if self.get_programlisting() != None :
            if self.programlisting:
                self.programlisting.export(outfile, level, namespace_, name_='programlisting')
        if self.get_location() != None :
            if self.location:
                self.location.export(outfile, level, namespace_, name_='location')
        if self.get_listofallmembers() != None :
            if self.listofallmembers:
                self.listofallmembers.export(outfile, level, namespace_, name_='listofallmembers')
    def exportLiteral(self, outfile, level, name_='compounddefType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('kind = "%s",\n' % (self.get_kind(),))
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('compoundname=%s,\n' % quote_python(self.get_compoundname()))
        showIndent(outfile, level)
        outfile.write('title=%s,\n' % quote_python(self.get_title()))
        showIndent(outfile, level)
        outfile.write('basecompoundref=[\n')
        level += 1
        for basecompoundref in self.basecompoundref:
            showIndent(outfile, level)
            outfile.write('basecompoundref(\n')
            basecompoundref.exportLiteral(outfile, level, name_='basecompoundref')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('derivedcompoundref=[\n')
        level += 1
        for derivedcompoundref in self.derivedcompoundref:
            showIndent(outfile, level)
            outfile.write('derivedcompoundref(\n')
            derivedcompoundref.exportLiteral(outfile, level, name_='derivedcompoundref')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('includes=[\n')
        level += 1
        for includes in self.includes:
            showIndent(outfile, level)
            outfile.write('includes(\n')
            includes.exportLiteral(outfile, level, name_='includes')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('includedby=[\n')
        level += 1
        for includedby in self.includedby:
            showIndent(outfile, level)
            outfile.write('includedby(\n')
            includedby.exportLiteral(outfile, level, name_='includedby')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.incdepgraph:
            showIndent(outfile, level)
            outfile.write('incdepgraph=graphType(\n')
            self.incdepgraph.exportLiteral(outfile, level, name_='incdepgraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.invincdepgraph:
            showIndent(outfile, level)
            outfile.write('invincdepgraph=graphType(\n')
            self.invincdepgraph.exportLiteral(outfile, level, name_='invincdepgraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('innerdir=[\n')
        level += 1
        for innerdir in self.innerdir:
            showIndent(outfile, level)
            outfile.write('innerdir(\n')
            innerdir.exportLiteral(outfile, level, name_='innerdir')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('innerfile=[\n')
        level += 1
        for innerfile in self.innerfile:
            showIndent(outfile, level)
            outfile.write('innerfile(\n')
            innerfile.exportLiteral(outfile, level, name_='innerfile')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('innerclass=[\n')
        level += 1
        for innerclass in self.innerclass:
            showIndent(outfile, level)
            outfile.write('innerclass(\n')
            innerclass.exportLiteral(outfile, level, name_='innerclass')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('innernamespace=[\n')
        level += 1
        for innernamespace in self.innernamespace:
            showIndent(outfile, level)
            outfile.write('innernamespace(\n')
            innernamespace.exportLiteral(outfile, level, name_='innernamespace')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('innerpage=[\n')
        level += 1
        for innerpage in self.innerpage:
            showIndent(outfile, level)
            outfile.write('innerpage(\n')
            innerpage.exportLiteral(outfile, level, name_='innerpage')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('innergroup=[\n')
        level += 1
        for innergroup in self.innergroup:
            showIndent(outfile, level)
            outfile.write('innergroup(\n')
            innergroup.exportLiteral(outfile, level, name_='innergroup')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.templateparamlist:
            showIndent(outfile, level)
            outfile.write('templateparamlist=templateparamlistType(\n')
            self.templateparamlist.exportLiteral(outfile, level, name_='templateparamlist')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('sectiondef=[\n')
        level += 1
        for sectiondef in self.sectiondef:
            showIndent(outfile, level)
            outfile.write('sectiondef(\n')
            sectiondef.exportLiteral(outfile, level, name_='sectiondef')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.briefdescription:
            showIndent(outfile, level)
            outfile.write('briefdescription=descriptionType(\n')
            self.briefdescription.exportLiteral(outfile, level, name_='briefdescription')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.detaileddescription:
            showIndent(outfile, level)
            outfile.write('detaileddescription=descriptionType(\n')
            self.detaileddescription.exportLiteral(outfile, level, name_='detaileddescription')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.inheritancegraph:
            showIndent(outfile, level)
            outfile.write('inheritancegraph=graphType(\n')
            self.inheritancegraph.exportLiteral(outfile, level, name_='inheritancegraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.collaborationgraph:
            showIndent(outfile, level)
            outfile.write('collaborationgraph=graphType(\n')
            self.collaborationgraph.exportLiteral(outfile, level, name_='collaborationgraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.programlisting:
            showIndent(outfile, level)
            outfile.write('programlisting=listingType(\n')
            self.programlisting.exportLiteral(outfile, level, name_='programlisting')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=locationType(\n')
            self.location.exportLiteral(outfile, level, name_='location')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.listofallmembers:
            showIndent(outfile, level)
            outfile.write('listofallmembers=listofallmembersType(\n')
            self.listofallmembers.exportLiteral(outfile, level, name_='listofallmembers')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('kind'):
            self.kind = attrs.get('kind').value
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'compoundname':
            compoundname_ = ''
            for text__content_ in child_.childNodes:
                compoundname_ += text__content_.nodeValue
            self.compoundname = compoundname_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = docTitleType.factory()
            obj_.build(child_)
            self.set_title(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'basecompoundref':
            obj_ = compoundRefType.factory()
            obj_.build(child_)
            self.basecompoundref.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'derivedcompoundref':
            obj_ = compoundRefType.factory()
            obj_.build(child_)
            self.derivedcompoundref.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'includes':
            obj_ = incType.factory()
            obj_.build(child_)
            self.includes.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'includedby':
            obj_ = incType.factory()
            obj_.build(child_)
            self.includedby.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'incdepgraph':
            obj_ = graphType.factory()
            obj_.build(child_)
            self.set_incdepgraph(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'invincdepgraph':
            obj_ = graphType.factory()
            obj_.build(child_)
            self.set_invincdepgraph(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innerdir':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innerdir.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innerfile':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innerfile.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innerclass':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innerclass.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innernamespace':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innernamespace.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innerpage':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innerpage.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'innergroup':
            obj_ = refType.factory()
            obj_.build(child_)
            self.innergroup.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'templateparamlist':
            obj_ = templateparamlistType.factory()
            obj_.build(child_)
            self.set_templateparamlist(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sectiondef':
            obj_ = sectiondefType.factory()
            obj_.build(child_)
            self.sectiondef.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'briefdescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_briefdescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'detaileddescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_detaileddescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'inheritancegraph':
            obj_ = graphType.factory()
            obj_.build(child_)
            self.set_inheritancegraph(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'collaborationgraph':
            obj_ = graphType.factory()
            obj_.build(child_)
            self.set_collaborationgraph(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'programlisting':
            obj_ = listingType.factory()
            obj_.build(child_)
            self.set_programlisting(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = locationType.factory()
            obj_.build(child_)
            self.set_location(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'listofallmembers':
            obj_ = listofallmembersType.factory()
            obj_.build(child_)
            self.set_listofallmembers(obj_)
# end class compounddefType


class listofallmembersType(object):
    subclass = None
    superclass = None
    def __init__(self, member=None):
        if member is None:
            self.member = []
        else:
            self.member = member
    def factory(*args_, **kwargs_):
        if listofallmembersType.subclass:
            return listofallmembersType.subclass(*args_, **kwargs_)
        else:
            return listofallmembersType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_member(self): return self.member
    def set_member(self, member): self.member = member
    def add_member(self, value): self.member.append(value)
    def insert_member(self, index, value): self.member[index] = value
    def export(self, outfile, level, namespace_='', name_='listofallmembersType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='listofallmembersType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='listofallmembersType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='listofallmembersType'):
        for member_ in self.get_member():
            member_.export(outfile, level, namespace_, name_='member')
    def exportLiteral(self, outfile, level, name_='listofallmembersType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('member=[\n')
        level += 1
        for member in self.member:
            showIndent(outfile, level)
            outfile.write('member(\n')
            member.exportLiteral(outfile, level, name_='member')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'member':
            obj_ = memberRefType.factory()
            obj_.build(child_)
            self.member.append(obj_)
# end class listofallmembersType


class memberRefType(object):
    subclass = None
    superclass = None
    def __init__(self, virt=None, prot=None, refid=None, ambiguityscope=None, scope='', name=''):
        self.virt = virt
        self.prot = prot
        self.refid = refid
        self.ambiguityscope = ambiguityscope
        self.scope = scope
        self.name = name
    def factory(*args_, **kwargs_):
        if memberRefType.subclass:
            return memberRefType.subclass(*args_, **kwargs_)
        else:
            return memberRefType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_scope(self): return self.scope
    def set_scope(self, scope): self.scope = scope
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_virt(self): return self.virt
    def set_virt(self, virt): self.virt = virt
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def get_ambiguityscope(self): return self.ambiguityscope
    def set_ambiguityscope(self, ambiguityscope): self.ambiguityscope = ambiguityscope
    def export(self, outfile, level, namespace_='', name_='memberRefType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='memberRefType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='memberRefType'):
        if self.get_virt() is not None:
            outfile.write(' virt="%s"' % str(self.get_virt()))
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
        if self.get_ambiguityscope() is not None:
            outfile.write(' ambiguityscope="%s"' % (quote_attrib(self.get_ambiguityscope()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='memberRefType'):
        showIndent(outfile, level)
        outfile.write('<%sscope>%s</%sscope>\n' % (namespace_, quote_xml(self.get_scope()), namespace_))
        showIndent(outfile, level)
        outfile.write('<%sname>%s</%sname>\n' % (namespace_, quote_xml(self.get_name()), namespace_))
    def exportLiteral(self, outfile, level, name_='memberRefType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('virt = "%s",\n' % (self.get_virt(),))
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
        showIndent(outfile, level)
        wrt('ambiguityscope = "%s",\n' % (self.get_ambiguityscope(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('scope=%s,\n' % quote_python(self.get_scope()))
        showIndent(outfile, level)
        outfile.write('name=%s,\n' % quote_python(self.get_name()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('virt'):
            self.virt = attrs.get('virt').value
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
        if attrs.get('ambiguityscope'):
            self.ambiguityscope = attrs.get('ambiguityscope').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'scope':
            scope_ = ''
            for text__content_ in child_.childNodes:
                scope_ += text__content_.nodeValue
            self.scope = scope_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'name':
            name_ = ''
            for text__content_ in child_.childNodes:
                name_ += text__content_.nodeValue
            self.name = name_
# end class memberRefType


class scope(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if scope.subclass:
            return scope.subclass(*args_, **kwargs_)
        else:
            return scope(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='scope'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='scope')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='scope'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='scope'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='scope'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class scope


class name(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if name.subclass:
            return name.subclass(*args_, **kwargs_)
        else:
            return name(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='name'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='name')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='name'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='name'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='name'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class name


class compoundRefType(object):
    subclass = None
    superclass = None
    def __init__(self, virt=None, prot=None, refid=None, valueOf_='', mixedclass_=None, content_=None):
        self.virt = virt
        self.prot = prot
        self.refid = refid
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if compoundRefType.subclass:
            return compoundRefType.subclass(*args_, **kwargs_)
        else:
            return compoundRefType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_virt(self): return self.virt
    def set_virt(self, virt): self.virt = virt
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='compoundRefType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='compoundRefType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='compoundRefType'):
        if self.get_virt() is not None:
            outfile.write(' virt="%s"' % str(self.get_virt()))
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='compoundRefType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='compoundRefType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('virt = "%s",\n' % (self.get_virt(),))
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('virt'):
            self.virt = attrs.get('virt').value
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class compoundRefType


class reimplementType(object):
    subclass = None
    superclass = None
    def __init__(self, refid=None, valueOf_='', mixedclass_=None, content_=None):
        self.refid = refid
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if reimplementType.subclass:
            return reimplementType.subclass(*args_, **kwargs_)
        else:
            return reimplementType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='reimplementType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='reimplementType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='reimplementType'):
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='reimplementType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='reimplementType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class reimplementType


class incType(object):
    subclass = None
    superclass = None
    def __init__(self, local=None, refid=None, valueOf_='', mixedclass_=None, content_=None):
        self.local = local
        self.refid = refid
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if incType.subclass:
            return incType.subclass(*args_, **kwargs_)
        else:
            return incType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_local(self): return self.local
    def set_local(self, local): self.local = local
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='incType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='incType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='incType'):
        if self.get_local() is not None:
            outfile.write(' local="%s"' % str(self.get_local()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='incType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='incType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('local = "%s",\n' % (self.get_local(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('local'):
            self.local = attrs.get('local').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class incType


class refType(object):
    subclass = None
    superclass = None
    def __init__(self, prot=None, refid=None, valueOf_='', mixedclass_=None, content_=None):
        self.prot = prot
        self.refid = refid
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if refType.subclass:
            return refType.subclass(*args_, **kwargs_)
        else:
            return refType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='refType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='refType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='refType'):
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='refType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='refType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class refType


class refTextType(object):
    subclass = None
    superclass = None
    def __init__(self, refid=None, kindref=None, external=None, valueOf_='', mixedclass_=None, content_=None):
        self.refid = refid
        self.kindref = kindref
        self.external = external
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if refTextType.subclass:
            return refTextType.subclass(*args_, **kwargs_)
        else:
            return refTextType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def get_kindref(self): return self.kindref
    def set_kindref(self, kindref): self.kindref = kindref
    def get_external(self): return self.external
    def set_external(self, external): self.external = external
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='refTextType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='refTextType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='refTextType'):
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
        if self.get_kindref() is not None:
            outfile.write(' kindref="%s"' % str(self.get_kindref()))
        if self.get_external() is not None:
            outfile.write(' external="%s"' % (quote_attrib(self.get_external()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='refTextType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='refTextType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
        showIndent(outfile, level)
        wrt('kindref = "%s",\n' % (self.get_kindref(),))
        showIndent(outfile, level)
        wrt('external = "%s",\n' % (self.get_external(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
        if attrs.get('kindref'):
            self.kindref = attrs.get('kindref').value
        if attrs.get('external'):
            self.external = attrs.get('external').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class refTextType


class sectiondefType(object):
    subclass = None
    superclass = None
    def __init__(self, kind=None, header='', description=None, memberdef=None):
        self.kind = kind
        self.header = header
        self.description = description
        if memberdef is None:
            self.memberdef = []
        else:
            self.memberdef = memberdef
    def factory(*args_, **kwargs_):
        if sectiondefType.subclass:
            return sectiondefType.subclass(*args_, **kwargs_)
        else:
            return sectiondefType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_header(self): return self.header
    def set_header(self, header): self.header = header
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_memberdef(self): return self.memberdef
    def set_memberdef(self, memberdef): self.memberdef = memberdef
    def add_memberdef(self, value): self.memberdef.append(value)
    def insert_memberdef(self, index, value): self.memberdef[index] = value
    def get_kind(self): return self.kind
    def set_kind(self, kind): self.kind = kind
    def export(self, outfile, level, namespace_='', name_='sectiondefType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='sectiondefType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='sectiondefType'):
        if self.get_kind() is not None:
            outfile.write(' kind="%s"' % str(self.get_kind()))
    def exportChildren(self, outfile, level, namespace_='', name_='sectiondefType'):
        if self.get_header() != None :
            if self.get_header() != "" :
                showIndent(outfile, level)
                outfile.write('<%sheader>%s</%sheader>\n' % (namespace_, quote_xml(self.get_header()), namespace_))
        if self.get_description() != None :
            if self.description:
                self.description.export(outfile, level, namespace_, name_='description')
        for memberdef_ in self.get_memberdef():
            memberdef_.export(outfile, level, namespace_, name_='memberdef')
    def exportLiteral(self, outfile, level, name_='sectiondefType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('kind = "%s",\n' % (self.get_kind(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('header=%s,\n' % quote_python(self.get_header()))
        if self.description:
            showIndent(outfile, level)
            outfile.write('description=descriptionType(\n')
            self.description.exportLiteral(outfile, level, name_='description')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('memberdef=[\n')
        level += 1
        for memberdef in self.memberdef:
            showIndent(outfile, level)
            outfile.write('memberdef(\n')
            memberdef.exportLiteral(outfile, level, name_='memberdef')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('kind'):
            self.kind = attrs.get('kind').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'header':
            header_ = ''
            for text__content_ in child_.childNodes:
                header_ += text__content_.nodeValue
            self.header = header_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'memberdef':
            obj_ = memberdefType.factory()
            obj_.build(child_)
            self.memberdef.append(obj_)
# end class sectiondefType


class memberdefType(object):
    subclass = None
    superclass = None
    def __init__(self, initonly=None, kind=None, volatile=None, const=None, raisexx=None, virt=None, readable=None, prot=None, explicit=None, new=None, final=None, writable=None, add=None, static=None, remove=None, sealed=None, mutable=None, gettable=None, inline=None, settable=None, id=None, templateparamlist=None, typexx=None, definition='', argsstring='', name='', read='', write='', bitfield='', reimplements=None, reimplementedby=None, param=None, enumvalue=None, initializer=None, exceptions=None, briefdescription=None, detaileddescription=None, inbodydescription=None, location=None, references=None, referencedby=None):
        self.initonly = initonly
        self.kind = kind
        self.volatile = volatile
        self.const = const
        self.raisexx = raisexx
        self.virt = virt
        self.readable = readable
        self.prot = prot
        self.explicit = explicit
        self.new = new
        self.final = final
        self.writable = writable
        self.add = add
        self.static = static
        self.remove = remove
        self.sealed = sealed
        self.mutable = mutable
        self.gettable = gettable
        self.inline = inline
        self.settable = settable
        self.id = id
        self.templateparamlist = templateparamlist
        self.typexx = typexx
        self.definition = definition
        self.argsstring = argsstring
        self.name = name
        self.read = read
        self.write = write
        self.bitfield = bitfield
        if reimplements is None:
            self.reimplements = []
        else:
            self.reimplements = reimplements
        if reimplementedby is None:
            self.reimplementedby = []
        else:
            self.reimplementedby = reimplementedby
        if param is None:
            self.param = []
        else:
            self.param = param
        if enumvalue is None:
            self.enumvalue = []
        else:
            self.enumvalue = enumvalue
        self.initializer = initializer
        self.exceptions = exceptions
        self.briefdescription = briefdescription
        self.detaileddescription = detaileddescription
        self.inbodydescription = inbodydescription
        self.location = location
        if references is None:
            self.references = []
        else:
            self.references = references
        if referencedby is None:
            self.referencedby = []
        else:
            self.referencedby = referencedby
    def factory(*args_, **kwargs_):
        if memberdefType.subclass:
            return memberdefType.subclass(*args_, **kwargs_)
        else:
            return memberdefType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_templateparamlist(self): return self.templateparamlist
    def set_templateparamlist(self, templateparamlist): self.templateparamlist = templateparamlist
    def get_type(self): return self.typexx
    def set_type(self, typexx): self.typexx = typexx
    def get_definition(self): return self.definition
    def set_definition(self, definition): self.definition = definition
    def get_argsstring(self): return self.argsstring
    def set_argsstring(self, argsstring): self.argsstring = argsstring
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_read(self): return self.read
    def set_read(self, read): self.read = read
    def get_write(self): return self.write
    def set_write(self, write): self.write = write
    def get_bitfield(self): return self.bitfield
    def set_bitfield(self, bitfield): self.bitfield = bitfield
    def get_reimplements(self): return self.reimplements
    def set_reimplements(self, reimplements): self.reimplements = reimplements
    def add_reimplements(self, value): self.reimplements.append(value)
    def insert_reimplements(self, index, value): self.reimplements[index] = value
    def get_reimplementedby(self): return self.reimplementedby
    def set_reimplementedby(self, reimplementedby): self.reimplementedby = reimplementedby
    def add_reimplementedby(self, value): self.reimplementedby.append(value)
    def insert_reimplementedby(self, index, value): self.reimplementedby[index] = value
    def get_param(self): return self.param
    def set_param(self, param): self.param = param
    def add_param(self, value): self.param.append(value)
    def insert_param(self, index, value): self.param[index] = value
    def get_enumvalue(self): return self.enumvalue
    def set_enumvalue(self, enumvalue): self.enumvalue = enumvalue
    def add_enumvalue(self, value): self.enumvalue.append(value)
    def insert_enumvalue(self, index, value): self.enumvalue[index] = value
    def get_initializer(self): return self.initializer
    def set_initializer(self, initializer): self.initializer = initializer
    def get_exceptions(self): return self.exceptions
    def set_exceptions(self, exceptions): self.exceptions = exceptions
    def get_briefdescription(self): return self.briefdescription
    def set_briefdescription(self, briefdescription): self.briefdescription = briefdescription
    def get_detaileddescription(self): return self.detaileddescription
    def set_detaileddescription(self, detaileddescription): self.detaileddescription = detaileddescription
    def get_inbodydescription(self): return self.inbodydescription
    def set_inbodydescription(self, inbodydescription): self.inbodydescription = inbodydescription
    def get_location(self): return self.location
    def set_location(self, location): self.location = location
    def get_references(self): return self.references
    def set_references(self, references): self.references = references
    def add_references(self, value): self.references.append(value)
    def insert_references(self, index, value): self.references[index] = value
    def get_referencedby(self): return self.referencedby
    def set_referencedby(self, referencedby): self.referencedby = referencedby
    def add_referencedby(self, value): self.referencedby.append(value)
    def insert_referencedby(self, index, value): self.referencedby[index] = value
    def get_initonly(self): return self.initonly
    def set_initonly(self, initonly): self.initonly = initonly
    def get_kind(self): return self.kind
    def set_kind(self, kind): self.kind = kind
    def get_volatile(self): return self.volatile
    def set_volatile(self, volatile): self.volatile = volatile
    def get_const(self): return self.const
    def set_const(self, const): self.const = const
    def get_raise(self): return self.raisexx
    def set_raise(self, raisexx): self.raisexx = raisexx
    def get_virt(self): return self.virt
    def set_virt(self, virt): self.virt = virt
    def get_readable(self): return self.readable
    def set_readable(self, readable): self.readable = readable
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_explicit(self): return self.explicit
    def set_explicit(self, explicit): self.explicit = explicit
    def get_new(self): return self.new
    def set_new(self, new): self.new = new
    def get_final(self): return self.final
    def set_final(self, final): self.final = final
    def get_writable(self): return self.writable
    def set_writable(self, writable): self.writable = writable
    def get_add(self): return self.add
    def set_add(self, add): self.add = add
    def get_static(self): return self.static
    def set_static(self, static): self.static = static
    def get_remove(self): return self.remove
    def set_remove(self, remove): self.remove = remove
    def get_sealed(self): return self.sealed
    def set_sealed(self, sealed): self.sealed = sealed
    def get_mutable(self): return self.mutable
    def set_mutable(self, mutable): self.mutable = mutable
    def get_gettable(self): return self.gettable
    def set_gettable(self, gettable): self.gettable = gettable
    def get_inline(self): return self.inline
    def set_inline(self, inline): self.inline = inline
    def get_settable(self): return self.settable
    def set_settable(self, settable): self.settable = settable
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='memberdefType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='memberdefType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='memberdefType'):
        if self.get_initonly() is not None:
            outfile.write(' initonly="%s"' % str(self.get_initonly()))
        if self.get_kind() is not None:
            outfile.write(' kind="%s"' % str(self.get_kind()))
        if self.get_volatile() is not None:
            outfile.write(' volatile="%s"' % str(self.get_volatile()))
        if self.get_const() is not None:
            outfile.write(' const="%s"' % str(self.get_const()))
        if self.get_raise() is not None:
            outfile.write(' raise="%s"' % str(self.get_raise()))
        if self.get_virt() is not None:
            outfile.write(' virt="%s"' % str(self.get_virt()))
        if self.get_readable() is not None:
            outfile.write(' readable="%s"' % str(self.get_readable()))
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_explicit() is not None:
            outfile.write(' explicit="%s"' % str(self.get_explicit()))
        if self.get_new() is not None:
            outfile.write(' new="%s"' % str(self.get_new()))
        if self.get_final() is not None:
            outfile.write(' final="%s"' % str(self.get_final()))
        if self.get_writable() is not None:
            outfile.write(' writable="%s"' % str(self.get_writable()))
        if self.get_add() is not None:
            outfile.write(' add="%s"' % str(self.get_add()))
        if self.get_static() is not None:
            outfile.write(' static="%s"' % str(self.get_static()))
        if self.get_remove() is not None:
            outfile.write(' remove="%s"' % str(self.get_remove()))
        if self.get_sealed() is not None:
            outfile.write(' sealed="%s"' % str(self.get_sealed()))
        if self.get_mutable() is not None:
            outfile.write(' mutable="%s"' % str(self.get_mutable()))
        if self.get_gettable() is not None:
            outfile.write(' gettable="%s"' % str(self.get_gettable()))
        if self.get_inline() is not None:
            outfile.write(' inline="%s"' % str(self.get_inline()))
        if self.get_settable() is not None:
            outfile.write(' settable="%s"' % str(self.get_settable()))
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='memberdefType'):
        if self.get_templateparamlist() != None :
            if self.templateparamlist:
                self.templateparamlist.export(outfile, level, namespace_, name_='templateparamlist')
        if self.get_type() != None :
            if self.typexx:
                self.typexx.export(outfile, level, namespace_, name_='type')
        if self.get_definition() != None :
            if self.get_definition() != "" :
                showIndent(outfile, level)
                outfile.write('<%sdefinition>%s</%sdefinition>\n' % (namespace_, quote_xml(self.get_definition()), namespace_))
        if self.get_argsstring() != None :
            if self.get_argsstring() != "" :
                showIndent(outfile, level)
                outfile.write('<%sargsstring>%s</%sargsstring>\n' % (namespace_, quote_xml(self.get_argsstring()), namespace_))
        showIndent(outfile, level)
        outfile.write('<%sname>%s</%sname>\n' % (namespace_, quote_xml(self.get_name()), namespace_))
        if self.get_read() != None :
            if self.get_read() != "" :
                showIndent(outfile, level)
                outfile.write('<%sread>%s</%sread>\n' % (namespace_, quote_xml(self.get_read()), namespace_))
        if self.get_write() != None :
            if self.get_write() != "" :
                showIndent(outfile, level)
                outfile.write('<%swrite>%s</%swrite>\n' % (namespace_, quote_xml(self.get_write()), namespace_))
        if self.get_bitfield() != None :
            if self.get_bitfield() != "" :
                showIndent(outfile, level)
                outfile.write('<%sbitfield>%s</%sbitfield>\n' % (namespace_, quote_xml(self.get_bitfield()), namespace_))
        for reimplements_ in self.get_reimplements():
            reimplements_.export(outfile, level, namespace_, name_='reimplements')
        for reimplementedby_ in self.get_reimplementedby():
            reimplementedby_.export(outfile, level, namespace_, name_='reimplementedby')
        for param_ in self.get_param():
            param_.export(outfile, level, namespace_, name_='param')
        for enumvalue_ in self.get_enumvalue():
            enumvalue_.export(outfile, level, namespace_, name_='enumvalue')
        if self.get_initializer() != None :
            if self.initializer:
                self.initializer.export(outfile, level, namespace_, name_='initializer')
        if self.get_exceptions() != None :
            if self.exceptions:
                self.exceptions.export(outfile, level, namespace_, name_='exceptions')
        if self.get_briefdescription() != None :
            if self.briefdescription:
                self.briefdescription.export(outfile, level, namespace_, name_='briefdescription')
        if self.get_detaileddescription() != None :
            if self.detaileddescription:
                self.detaileddescription.export(outfile, level, namespace_, name_='detaileddescription')
        if self.get_inbodydescription() != None :
            if self.inbodydescription:
                self.inbodydescription.export(outfile, level, namespace_, name_='inbodydescription')
        if self.location:
            self.location.export(outfile, level, namespace_, name_='location', )
        for references_ in self.get_references():
            references_.export(outfile, level, namespace_, name_='references')
        for referencedby_ in self.get_referencedby():
            referencedby_.export(outfile, level, namespace_, name_='referencedby')
    def exportLiteral(self, outfile, level, name_='memberdefType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('initonly = "%s",\n' % (self.get_initonly(),))
        showIndent(outfile, level)
        wrt('kind = "%s",\n' % (self.get_kind(),))
        showIndent(outfile, level)
        wrt('volatile = "%s",\n' % (self.get_volatile(),))
        showIndent(outfile, level)
        wrt('const = "%s",\n' % (self.get_const(),))
        showIndent(outfile, level)
        wrt('raisexx = "%s",\n' % (self.get_raise(),))
        showIndent(outfile, level)
        wrt('virt = "%s",\n' % (self.get_virt(),))
        showIndent(outfile, level)
        wrt('readable = "%s",\n' % (self.get_readable(),))
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('explicit = "%s",\n' % (self.get_explicit(),))
        showIndent(outfile, level)
        wrt('new = "%s",\n' % (self.get_new(),))
        showIndent(outfile, level)
        wrt('final = "%s",\n' % (self.get_final(),))
        showIndent(outfile, level)
        wrt('writable = "%s",\n' % (self.get_writable(),))
        showIndent(outfile, level)
        wrt('add = "%s",\n' % (self.get_add(),))
        showIndent(outfile, level)
        wrt('static = "%s",\n' % (self.get_static(),))
        showIndent(outfile, level)
        wrt('remove = "%s",\n' % (self.get_remove(),))
        showIndent(outfile, level)
        wrt('sealed = "%s",\n' % (self.get_sealed(),))
        showIndent(outfile, level)
        wrt('mutable = "%s",\n' % (self.get_mutable(),))
        showIndent(outfile, level)
        wrt('gettable = "%s",\n' % (self.get_gettable(),))
        showIndent(outfile, level)
        wrt('inline = "%s",\n' % (self.get_inline(),))
        showIndent(outfile, level)
        wrt('settable = "%s",\n' % (self.get_settable(),))
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.templateparamlist:
            showIndent(outfile, level)
            outfile.write('templateparamlist=templateparamlistType(\n')
            self.templateparamlist.exportLiteral(outfile, level, name_='templateparamlist')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.typexx:
            showIndent(outfile, level)
            outfile.write('typexx=linkedTextType(\n')
            self.typexx.exportLiteral(outfile, level, name_='type')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('definition=%s,\n' % quote_python(self.get_definition()))
        showIndent(outfile, level)
        outfile.write('argsstring=%s,\n' % quote_python(self.get_argsstring()))
        showIndent(outfile, level)
        outfile.write('name=%s,\n' % quote_python(self.get_name()))
        showIndent(outfile, level)
        outfile.write('read=%s,\n' % quote_python(self.get_read()))
        showIndent(outfile, level)
        outfile.write('write=%s,\n' % quote_python(self.get_write()))
        showIndent(outfile, level)
        outfile.write('bitfield=%s,\n' % quote_python(self.get_bitfield()))
        showIndent(outfile, level)
        outfile.write('reimplements=[\n')
        level += 1
        for reimplements in self.reimplements:
            showIndent(outfile, level)
            outfile.write('reimplements(\n')
            reimplements.exportLiteral(outfile, level, name_='reimplements')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('reimplementedby=[\n')
        level += 1
        for reimplementedby in self.reimplementedby:
            showIndent(outfile, level)
            outfile.write('reimplementedby(\n')
            reimplementedby.exportLiteral(outfile, level, name_='reimplementedby')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('param=[\n')
        level += 1
        for param in self.param:
            showIndent(outfile, level)
            outfile.write('param(\n')
            param.exportLiteral(outfile, level, name_='param')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('enumvalue=[\n')
        level += 1
        for enumvalue in self.enumvalue:
            showIndent(outfile, level)
            outfile.write('enumvalue(\n')
            enumvalue.exportLiteral(outfile, level, name_='enumvalue')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.initializer:
            showIndent(outfile, level)
            outfile.write('initializer=linkedTextType(\n')
            self.initializer.exportLiteral(outfile, level, name_='initializer')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.exceptions:
            showIndent(outfile, level)
            outfile.write('exceptions=linkedTextType(\n')
            self.exceptions.exportLiteral(outfile, level, name_='exceptions')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.briefdescription:
            showIndent(outfile, level)
            outfile.write('briefdescription=descriptionType(\n')
            self.briefdescription.exportLiteral(outfile, level, name_='briefdescription')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.detaileddescription:
            showIndent(outfile, level)
            outfile.write('detaileddescription=descriptionType(\n')
            self.detaileddescription.exportLiteral(outfile, level, name_='detaileddescription')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.inbodydescription:
            showIndent(outfile, level)
            outfile.write('inbodydescription=descriptionType(\n')
            self.inbodydescription.exportLiteral(outfile, level, name_='inbodydescription')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.location:
            showIndent(outfile, level)
            outfile.write('location=locationType(\n')
            self.location.exportLiteral(outfile, level, name_='location')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('references=[\n')
        level += 1
        for references in self.references:
            showIndent(outfile, level)
            outfile.write('references(\n')
            references.exportLiteral(outfile, level, name_='references')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('referencedby=[\n')
        level += 1
        for referencedby in self.referencedby:
            showIndent(outfile, level)
            outfile.write('referencedby(\n')
            referencedby.exportLiteral(outfile, level, name_='referencedby')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('initonly'):
            self.initonly = attrs.get('initonly').value
        if attrs.get('kind'):
            self.kind = attrs.get('kind').value
        if attrs.get('volatile'):
            self.volatile = attrs.get('volatile').value
        if attrs.get('const'):
            self.const = attrs.get('const').value
        if attrs.get('raise'):
            self.raisexx = attrs.get('raise').value
        if attrs.get('virt'):
            self.virt = attrs.get('virt').value
        if attrs.get('readable'):
            self.readable = attrs.get('readable').value
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('explicit'):
            self.explicit = attrs.get('explicit').value
        if attrs.get('new'):
            self.new = attrs.get('new').value
        if attrs.get('final'):
            self.final = attrs.get('final').value
        if attrs.get('writable'):
            self.writable = attrs.get('writable').value
        if attrs.get('add'):
            self.add = attrs.get('add').value
        if attrs.get('static'):
            self.static = attrs.get('static').value
        if attrs.get('remove'):
            self.remove = attrs.get('remove').value
        if attrs.get('sealed'):
            self.sealed = attrs.get('sealed').value
        if attrs.get('mutable'):
            self.mutable = attrs.get('mutable').value
        if attrs.get('gettable'):
            self.gettable = attrs.get('gettable').value
        if attrs.get('inline'):
            self.inline = attrs.get('inline').value
        if attrs.get('settable'):
            self.settable = attrs.get('settable').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'templateparamlist':
            obj_ = templateparamlistType.factory()
            obj_.build(child_)
            self.set_templateparamlist(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'type':
            obj_ = linkedTextType.factory()
            obj_.build(child_)
            self.set_type(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'definition':
            definition_ = ''
            for text__content_ in child_.childNodes:
                definition_ += text__content_.nodeValue
            self.definition = definition_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'argsstring':
            argsstring_ = ''
            for text__content_ in child_.childNodes:
                argsstring_ += text__content_.nodeValue
            self.argsstring = argsstring_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'name':
            name_ = ''
            for text__content_ in child_.childNodes:
                name_ += text__content_.nodeValue
            self.name = name_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'read':
            read_ = ''
            for text__content_ in child_.childNodes:
                read_ += text__content_.nodeValue
            self.read = read_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'write':
            write_ = ''
            for text__content_ in child_.childNodes:
                write_ += text__content_.nodeValue
            self.write = write_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'bitfield':
            bitfield_ = ''
            for text__content_ in child_.childNodes:
                bitfield_ += text__content_.nodeValue
            self.bitfield = bitfield_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'reimplements':
            obj_ = reimplementType.factory()
            obj_.build(child_)
            self.reimplements.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'reimplementedby':
            obj_ = reimplementType.factory()
            obj_.build(child_)
            self.reimplementedby.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'param':
            obj_ = paramType.factory()
            obj_.build(child_)
            self.param.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'enumvalue':
            obj_ = enumvalueType.factory()
            obj_.build(child_)
            self.enumvalue.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'initializer':
            obj_ = linkedTextType.factory()
            obj_.build(child_)
            self.set_initializer(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'exceptions':
            obj_ = linkedTextType.factory()
            obj_.build(child_)
            self.set_exceptions(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'briefdescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_briefdescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'detaileddescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_detaileddescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'inbodydescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_inbodydescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'location':
            obj_ = locationType.factory()
            obj_.build(child_)
            self.set_location(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'references':
            obj_ = referenceType.factory()
            obj_.build(child_)
            self.references.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'referencedby':
            obj_ = referenceType.factory()
            obj_.build(child_)
            self.referencedby.append(obj_)
# end class memberdefType


class definition(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if definition.subclass:
            return definition.subclass(*args_, **kwargs_)
        else:
            return definition(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='definition'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='definition')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='definition'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='definition'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='definition'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class definition


class argsstring(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if argsstring.subclass:
            return argsstring.subclass(*args_, **kwargs_)
        else:
            return argsstring(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='argsstring'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='argsstring')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='argsstring'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='argsstring'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='argsstring'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class argsstring


class read(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if read.subclass:
            return read.subclass(*args_, **kwargs_)
        else:
            return read(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='read'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='read')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='read'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='read'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='read'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class read


class write(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if write.subclass:
            return write.subclass(*args_, **kwargs_)
        else:
            return write(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='write'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='write')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='write'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='write'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='write'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class write


class bitfield(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if bitfield.subclass:
            return bitfield.subclass(*args_, **kwargs_)
        else:
            return bitfield(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='bitfield'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='bitfield')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='bitfield'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='bitfield'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='bitfield'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class bitfield


class descriptionType(object):
    subclass = None
    superclass = None
    def __init__(self, title='', para=None, sect1=None, internal=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if descriptionType.subclass:
            return descriptionType.subclass(*args_, **kwargs_)
        else:
            return descriptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect1(self): return self.sect1
    def set_sect1(self, sect1): self.sect1 = sect1
    def add_sect1(self, value): self.sect1.append(value)
    def insert_sect1(self, index, value): self.sect1[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def export(self, outfile, level, namespace_='', name_='descriptionType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='descriptionType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='descriptionType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='descriptionType'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='descriptionType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'title', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect1':
            childobj_ = docSect1Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect1', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            childobj_ = docInternalType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'internal', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class descriptionType


class enumvalueType(object):
    subclass = None
    superclass = None
    def __init__(self, prot=None, id=None, name='', initializer=None, briefdescription=None, detaileddescription=None, mixedclass_=None, content_=None):
        self.prot = prot
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if enumvalueType.subclass:
            return enumvalueType.subclass(*args_, **kwargs_)
        else:
            return enumvalueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_initializer(self): return self.initializer
    def set_initializer(self, initializer): self.initializer = initializer
    def get_briefdescription(self): return self.briefdescription
    def set_briefdescription(self, briefdescription): self.briefdescription = briefdescription
    def get_detaileddescription(self): return self.detaileddescription
    def set_detaileddescription(self, detaileddescription): self.detaileddescription = detaileddescription
    def get_prot(self): return self.prot
    def set_prot(self, prot): self.prot = prot
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='enumvalueType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='enumvalueType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='enumvalueType'):
        if self.get_prot() is not None:
            outfile.write(' prot="%s"' % str(self.get_prot()))
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='enumvalueType'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='enumvalueType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('prot = "%s",\n' % (self.get_prot(),))
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('prot'):
            self.prot = attrs.get('prot').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'name':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'name', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'initializer':
            childobj_ = linkedTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'initializer', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'briefdescription':
            childobj_ = descriptionType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'briefdescription', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'detaileddescription':
            childobj_ = descriptionType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'detaileddescription', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class enumvalueType


class templateparamlistType(object):
    subclass = None
    superclass = None
    def __init__(self, param=None):
        if param is None:
            self.param = []
        else:
            self.param = param
    def factory(*args_, **kwargs_):
        if templateparamlistType.subclass:
            return templateparamlistType.subclass(*args_, **kwargs_)
        else:
            return templateparamlistType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_param(self): return self.param
    def set_param(self, param): self.param = param
    def add_param(self, value): self.param.append(value)
    def insert_param(self, index, value): self.param[index] = value
    def export(self, outfile, level, namespace_='', name_='templateparamlistType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='templateparamlistType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='templateparamlistType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='templateparamlistType'):
        for param_ in self.get_param():
            param_.export(outfile, level, namespace_, name_='param')
    def exportLiteral(self, outfile, level, name_='templateparamlistType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('param=[\n')
        level += 1
        for param in self.param:
            showIndent(outfile, level)
            outfile.write('param(\n')
            param.exportLiteral(outfile, level, name_='param')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'param':
            obj_ = paramType.factory()
            obj_.build(child_)
            self.param.append(obj_)
# end class templateparamlistType


class paramType(object):
    subclass = None
    superclass = None
    def __init__(self, typexx=None, declname='', defname='', array='', defval=None, briefdescription=None):
        self.typexx = typexx
        self.declname = declname
        self.defname = defname
        self.array = array
        self.defval = defval
        self.briefdescription = briefdescription
    def factory(*args_, **kwargs_):
        if paramType.subclass:
            return paramType.subclass(*args_, **kwargs_)
        else:
            return paramType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_type(self): return self.typexx
    def set_type(self, typexx): self.typexx = typexx
    def get_declname(self): return self.declname
    def set_declname(self, declname): self.declname = declname
    def get_defname(self): return self.defname
    def set_defname(self, defname): self.defname = defname
    def get_array(self): return self.array
    def set_array(self, array): self.array = array
    def get_defval(self): return self.defval
    def set_defval(self, defval): self.defval = defval
    def get_briefdescription(self): return self.briefdescription
    def set_briefdescription(self, briefdescription): self.briefdescription = briefdescription
    def export(self, outfile, level, namespace_='', name_='paramType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='paramType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='paramType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='paramType'):
        if self.get_type() != None :
            if self.typexx:
                self.typexx.export(outfile, level, namespace_, name_='type')
        if self.get_declname() != None :
            if self.get_declname() != "" :
                showIndent(outfile, level)
                outfile.write('<%sdeclname>%s</%sdeclname>\n' % (namespace_, quote_xml(self.get_declname()), namespace_))
        if self.get_defname() != None :
            if self.get_defname() != "" :
                showIndent(outfile, level)
                outfile.write('<%sdefname>%s</%sdefname>\n' % (namespace_, quote_xml(self.get_defname()), namespace_))
        if self.get_array() != None :
            if self.get_array() != "" :
                showIndent(outfile, level)
                outfile.write('<%sarray>%s</%sarray>\n' % (namespace_, quote_xml(self.get_array()), namespace_))
        if self.get_defval() != None :
            if self.defval:
                self.defval.export(outfile, level, namespace_, name_='defval')
        if self.get_briefdescription() != None :
            if self.briefdescription:
                self.briefdescription.export(outfile, level, namespace_, name_='briefdescription')
    def exportLiteral(self, outfile, level, name_='paramType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.typexx:
            showIndent(outfile, level)
            outfile.write('typexx=linkedTextType(\n')
            self.typexx.exportLiteral(outfile, level, name_='type')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('declname=%s,\n' % quote_python(self.get_declname()))
        showIndent(outfile, level)
        outfile.write('defname=%s,\n' % quote_python(self.get_defname()))
        showIndent(outfile, level)
        outfile.write('array=%s,\n' % quote_python(self.get_array()))
        if self.defval:
            showIndent(outfile, level)
            outfile.write('defval=linkedTextType(\n')
            self.defval.exportLiteral(outfile, level, name_='defval')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.briefdescription:
            showIndent(outfile, level)
            outfile.write('briefdescription=descriptionType(\n')
            self.briefdescription.exportLiteral(outfile, level, name_='briefdescription')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'type':
            obj_ = linkedTextType.factory()
            obj_.build(child_)
            self.set_type(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'declname':
            declname_ = ''
            for text__content_ in child_.childNodes:
                declname_ += text__content_.nodeValue
            self.declname = declname_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'defname':
            defname_ = ''
            for text__content_ in child_.childNodes:
                defname_ += text__content_.nodeValue
            self.defname = defname_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'array':
            array_ = ''
            for text__content_ in child_.childNodes:
                array_ += text__content_.nodeValue
            self.array = array_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'defval':
            obj_ = linkedTextType.factory()
            obj_.build(child_)
            self.set_defval(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'briefdescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_briefdescription(obj_)
# end class paramType


class declname(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if declname.subclass:
            return declname.subclass(*args_, **kwargs_)
        else:
            return declname(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='declname'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='declname')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='declname'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='declname'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='declname'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class declname


class defname(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if defname.subclass:
            return defname.subclass(*args_, **kwargs_)
        else:
            return defname(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='defname'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='defname')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='defname'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='defname'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='defname'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class defname


class array(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if array.subclass:
            return array.subclass(*args_, **kwargs_)
        else:
            return array(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='array'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='array')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='array'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='array'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='array'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class array


class linkedTextType(object):
    subclass = None
    superclass = None
    def __init__(self, ref=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if linkedTextType.subclass:
            return linkedTextType.subclass(*args_, **kwargs_)
        else:
            return linkedTextType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ref(self): return self.ref
    def set_ref(self, ref): self.ref = ref
    def add_ref(self, value): self.ref.append(value)
    def insert_ref(self, index, value): self.ref[index] = value
    def export(self, outfile, level, namespace_='', name_='linkedTextType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='linkedTextType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='linkedTextType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='linkedTextType'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='linkedTextType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'ref':
            childobj_ = refTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ref', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class linkedTextType


class graphType(object):
    subclass = None
    superclass = None
    def __init__(self, node=None):
        if node is None:
            self.node = []
        else:
            self.node = node
    def factory(*args_, **kwargs_):
        if graphType.subclass:
            return graphType.subclass(*args_, **kwargs_)
        else:
            return graphType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_node(self): return self.node
    def set_node(self, node): self.node = node
    def add_node(self, value): self.node.append(value)
    def insert_node(self, index, value): self.node[index] = value
    def export(self, outfile, level, namespace_='', name_='graphType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='graphType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='graphType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='graphType'):
        for node_ in self.get_node():
            node_.export(outfile, level, namespace_, name_='node')
    def exportLiteral(self, outfile, level, name_='graphType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('node=[\n')
        level += 1
        for node in self.node:
            showIndent(outfile, level)
            outfile.write('node(\n')
            node.exportLiteral(outfile, level, name_='node')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'node':
            obj_ = nodeType.factory()
            obj_.build(child_)
            self.node.append(obj_)
# end class graphType


class nodeType(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, label='', link=None, childnode=None):
        self.id = id
        self.label = label
        self.link = link
        if childnode is None:
            self.childnode = []
        else:
            self.childnode = childnode
    def factory(*args_, **kwargs_):
        if nodeType.subclass:
            return nodeType.subclass(*args_, **kwargs_)
        else:
            return nodeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_label(self): return self.label
    def set_label(self, label): self.label = label
    def get_link(self): return self.link
    def set_link(self, link): self.link = link
    def get_childnode(self): return self.childnode
    def set_childnode(self, childnode): self.childnode = childnode
    def add_childnode(self, value): self.childnode.append(value)
    def insert_childnode(self, index, value): self.childnode[index] = value
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='nodeType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='nodeType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='nodeType'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='nodeType'):
        showIndent(outfile, level)
        outfile.write('<%slabel>%s</%slabel>\n' % (namespace_, quote_xml(self.get_label()), namespace_))
        if self.get_link() != None :
            if self.link:
                self.link.export(outfile, level, namespace_, name_='link')
        for childnode_ in self.get_childnode():
            childnode_.export(outfile, level, namespace_, name_='childnode')
    def exportLiteral(self, outfile, level, name_='nodeType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('label=%s,\n' % quote_python(self.get_label()))
        if self.link:
            showIndent(outfile, level)
            outfile.write('link=linkType(\n')
            self.link.exportLiteral(outfile, level, name_='link')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('childnode=[\n')
        level += 1
        for childnode in self.childnode:
            showIndent(outfile, level)
            outfile.write('childnode(\n')
            childnode.exportLiteral(outfile, level, name_='childnode')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'label':
            label_ = ''
            for text__content_ in child_.childNodes:
                label_ += text__content_.nodeValue
            self.label = label_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'link':
            obj_ = linkType.factory()
            obj_.build(child_)
            self.set_link(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'childnode':
            obj_ = childnodeType.factory()
            obj_.build(child_)
            self.childnode.append(obj_)
# end class nodeType


class label(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if label.subclass:
            return label.subclass(*args_, **kwargs_)
        else:
            return label(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='label'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='label')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='label'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='label'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='label'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class label


class childnodeType(object):
    subclass = None
    superclass = None
    def __init__(self, relation=None, refid=None, edgelabel=None):
        self.relation = relation
        self.refid = refid
        if edgelabel is None:
            self.edgelabel = []
        else:
            self.edgelabel = edgelabel
    def factory(*args_, **kwargs_):
        if childnodeType.subclass:
            return childnodeType.subclass(*args_, **kwargs_)
        else:
            return childnodeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_edgelabel(self): return self.edgelabel
    def set_edgelabel(self, edgelabel): self.edgelabel = edgelabel
    def add_edgelabel(self, value): self.edgelabel.append(value)
    def insert_edgelabel(self, index, value): self.edgelabel[index] = value
    def get_relation(self): return self.relation
    def set_relation(self, relation): self.relation = relation
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def export(self, outfile, level, namespace_='', name_='childnodeType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='childnodeType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='childnodeType'):
        if self.get_relation() is not None:
            outfile.write(' relation="%s"' % str(self.get_relation()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='childnodeType'):
        for edgelabel_ in self.get_edgelabel():
            showIndent(outfile, level)
            outfile.write('<%sedgelabel>%s</%sedgelabel>\n' % (namespace_, quote_xml(edgelabel_), namespace_))
    def exportLiteral(self, outfile, level, name_='childnodeType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('relation = "%s",\n' % (self.get_relation(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('edgelabel=[\n')
        level += 1
        for edgelabel in self.edgelabel:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(edgelabel))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('relation'):
            self.relation = attrs.get('relation').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'edgelabel':
            edgelabel_ = ''
            for text__content_ in child_.childNodes:
                edgelabel_ += text__content_.nodeValue
            self.edgelabel.append(edgelabel_)
# end class childnodeType


class edgelabel(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if edgelabel.subclass:
            return edgelabel.subclass(*args_, **kwargs_)
        else:
            return edgelabel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='edgelabel'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='edgelabel')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='edgelabel'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='edgelabel'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='edgelabel'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class edgelabel


class linkType(object):
    subclass = None
    superclass = None
    def __init__(self, refid=None, external=None, valueOf_=''):
        self.refid = refid
        self.external = external
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if linkType.subclass:
            return linkType.subclass(*args_, **kwargs_)
        else:
            return linkType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def get_external(self): return self.external
    def set_external(self, external): self.external = external
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='linkType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='linkType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='linkType'):
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
        if self.get_external() is not None:
            outfile.write(' external="%s"' % (quote_attrib(self.get_external()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='linkType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='linkType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
        showIndent(outfile, level)
        wrt('external = "%s",\n' % (self.get_external(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
        if attrs.get('external'):
            self.external = attrs.get('external').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class linkType


class listingType(object):
    subclass = None
    superclass = None
    def __init__(self, codeline=None):
        if codeline is None:
            self.codeline = []
        else:
            self.codeline = codeline
    def factory(*args_, **kwargs_):
        if listingType.subclass:
            return listingType.subclass(*args_, **kwargs_)
        else:
            return listingType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_codeline(self): return self.codeline
    def set_codeline(self, codeline): self.codeline = codeline
    def add_codeline(self, value): self.codeline.append(value)
    def insert_codeline(self, index, value): self.codeline[index] = value
    def export(self, outfile, level, namespace_='', name_='listingType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='listingType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='listingType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='listingType'):
        for codeline_ in self.get_codeline():
            codeline_.export(outfile, level, namespace_, name_='codeline')
    def exportLiteral(self, outfile, level, name_='listingType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('codeline=[\n')
        level += 1
        for codeline in self.codeline:
            showIndent(outfile, level)
            outfile.write('codeline(\n')
            codeline.exportLiteral(outfile, level, name_='codeline')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'codeline':
            obj_ = codelineType.factory()
            obj_.build(child_)
            self.codeline.append(obj_)
# end class listingType


class codelineType(object):
    subclass = None
    superclass = None
    def __init__(self, external=None, lineno=None, refkind=None, refid=None, highlight=None):
        self.external = external
        self.lineno = lineno
        self.refkind = refkind
        self.refid = refid
        if highlight is None:
            self.highlight = []
        else:
            self.highlight = highlight
    def factory(*args_, **kwargs_):
        if codelineType.subclass:
            return codelineType.subclass(*args_, **kwargs_)
        else:
            return codelineType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_highlight(self): return self.highlight
    def set_highlight(self, highlight): self.highlight = highlight
    def add_highlight(self, value): self.highlight.append(value)
    def insert_highlight(self, index, value): self.highlight[index] = value
    def get_external(self): return self.external
    def set_external(self, external): self.external = external
    def get_lineno(self): return self.lineno
    def set_lineno(self, lineno): self.lineno = lineno
    def get_refkind(self): return self.refkind
    def set_refkind(self, refkind): self.refkind = refkind
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def export(self, outfile, level, namespace_='', name_='codelineType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='codelineType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='codelineType'):
        if self.get_external() is not None:
            outfile.write(' external="%s"' % str(self.get_external()))
        if self.get_lineno() is not None:
            outfile.write(' lineno="%d"' % self.get_lineno())
        if self.get_refkind() is not None:
            outfile.write(' refkind="%s"' % str(self.get_refkind()))
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='codelineType'):
        for highlight_ in self.get_highlight():
            highlight_.export(outfile, level, namespace_, name_='highlight')
    def exportLiteral(self, outfile, level, name_='codelineType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('external = "%s",\n' % (self.get_external(),))
        showIndent(outfile, level)
        wrt('lineno = "%s",\n' % (self.get_lineno(),))
        showIndent(outfile, level)
        wrt('refkind = "%s",\n' % (self.get_refkind(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('highlight=[\n')
        level += 1
        for highlight in self.highlight:
            showIndent(outfile, level)
            outfile.write('highlight(\n')
            highlight.exportLiteral(outfile, level, name_='highlight')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('external'):
            self.external = attrs.get('external').value
        if attrs.get('lineno'):
            try:
                self.lineno = int(attrs.get('lineno').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (lineno): %s' % exp)
        if attrs.get('refkind'):
            self.refkind = attrs.get('refkind').value
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'highlight':
            obj_ = highlightType.factory()
            obj_.build(child_)
            self.highlight.append(obj_)
# end class codelineType


class highlightType(object):
    subclass = None
    superclass = None
    def __init__(self, classxx=None, sp=None, ref=None, mixedclass_=None, content_=None):
        self.classxx = classxx
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if highlightType.subclass:
            return highlightType.subclass(*args_, **kwargs_)
        else:
            return highlightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_sp(self): return self.sp
    def set_sp(self, sp): self.sp = sp
    def add_sp(self, value): self.sp.append(value)
    def insert_sp(self, index, value): self.sp[index] = value
    def get_ref(self): return self.ref
    def set_ref(self, ref): self.ref = ref
    def add_ref(self, value): self.ref.append(value)
    def insert_ref(self, index, value): self.ref[index] = value
    def get_class(self): return self.classxx
    def set_class(self, classxx): self.classxx = classxx
    def export(self, outfile, level, namespace_='', name_='highlightType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='highlightType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='highlightType'):
        if self.get_class() is not None:
            outfile.write(' class="%s"' % str(self.get_class()))
    def exportChildren(self, outfile, level, namespace_='', name_='highlightType'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='highlightType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('classxx = "%s",\n' % (self.get_class(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('class'):
            self.classxx = attrs.get('class').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sp':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'sp', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'ref':
            childobj_ = refTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ref', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class highlightType


class sp(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if sp.subclass:
            return sp.subclass(*args_, **kwargs_)
        else:
            return sp(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='sp'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='sp')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='sp'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='sp'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='sp'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class sp


class referenceType(object):
    subclass = None
    superclass = None
    def __init__(self, endline=None, startline=None, refid=None, compoundref=None, valueOf_='', mixedclass_=None, content_=None):
        self.endline = endline
        self.startline = startline
        self.refid = refid
        self.compoundref = compoundref
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if referenceType.subclass:
            return referenceType.subclass(*args_, **kwargs_)
        else:
            return referenceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_endline(self): return self.endline
    def set_endline(self, endline): self.endline = endline
    def get_startline(self): return self.startline
    def set_startline(self, startline): self.startline = startline
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def get_compoundref(self): return self.compoundref
    def set_compoundref(self, compoundref): self.compoundref = compoundref
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='referenceType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='referenceType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='referenceType'):
        if self.get_endline() is not None:
            outfile.write(' endline="%d"' % self.get_endline())
        if self.get_startline() is not None:
            outfile.write(' startline="%d"' % self.get_startline())
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
        if self.get_compoundref() is not None:
            outfile.write(' compoundref="%s"' % (quote_attrib(self.get_compoundref()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='referenceType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='referenceType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('endline = "%s",\n' % (self.get_endline(),))
        showIndent(outfile, level)
        wrt('startline = "%s",\n' % (self.get_startline(),))
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
        showIndent(outfile, level)
        wrt('compoundref = "%s",\n' % (self.get_compoundref(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('endline'):
            try:
                self.endline = int(attrs.get('endline').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (endline): %s' % exp)
        if attrs.get('startline'):
            try:
                self.startline = int(attrs.get('startline').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (startline): %s' % exp)
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
        if attrs.get('compoundref'):
            self.compoundref = attrs.get('compoundref').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class referenceType


class locationType(object):
    subclass = None
    superclass = None
    def __init__(self, bodystart=None, line=None, bodyend=None, bodyfile=None, file=None, valueOf_=''):
        self.bodystart = bodystart
        self.line = line
        self.bodyend = bodyend
        self.bodyfile = bodyfile
        self.file = file
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if locationType.subclass:
            return locationType.subclass(*args_, **kwargs_)
        else:
            return locationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_bodystart(self): return self.bodystart
    def set_bodystart(self, bodystart): self.bodystart = bodystart
    def get_line(self): return self.line
    def set_line(self, line): self.line = line
    def get_bodyend(self): return self.bodyend
    def set_bodyend(self, bodyend): self.bodyend = bodyend
    def get_bodyfile(self): return self.bodyfile
    def set_bodyfile(self, bodyfile): self.bodyfile = bodyfile
    def get_file(self): return self.file
    def set_file(self, file): self.file = file
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='locationType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='locationType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='locationType'):
        if self.get_bodystart() is not None:
            outfile.write(' bodystart="%d"' % self.get_bodystart())
        if self.get_line() is not None:
            outfile.write(' line="%d"' % self.get_line())
        if self.get_bodyend() is not None:
            outfile.write(' bodyend="%d"' % self.get_bodyend())
        if self.get_bodyfile() is not None:
            outfile.write(' bodyfile="%s"' % (quote_attrib(self.get_bodyfile()), ))
        if self.get_file() is not None:
            outfile.write(' file="%s"' % (quote_attrib(self.get_file()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='locationType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='locationType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('bodystart = "%s",\n' % (self.get_bodystart(),))
        showIndent(outfile, level)
        wrt('line = "%s",\n' % (self.get_line(),))
        showIndent(outfile, level)
        wrt('bodyend = "%s",\n' % (self.get_bodyend(),))
        showIndent(outfile, level)
        wrt('bodyfile = "%s",\n' % (self.get_bodyfile(),))
        showIndent(outfile, level)
        wrt('file = "%s",\n' % (self.get_file(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('bodystart'):
            try:
                self.bodystart = int(attrs.get('bodystart').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (bodystart): %s' % exp)
        if attrs.get('line'):
            try:
                self.line = int(attrs.get('line').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (line): %s' % exp)
        if attrs.get('bodyend'):
            try:
                self.bodyend = int(attrs.get('bodyend').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (bodyend): %s' % exp)
        if attrs.get('bodyfile'):
            self.bodyfile = attrs.get('bodyfile').value
        if attrs.get('file'):
            self.file = attrs.get('file').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class locationType


class docSect1Type(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, title='', para=None, sect2=None, internal=None, mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docSect1Type.subclass:
            return docSect1Type.subclass(*args_, **kwargs_)
        else:
            return docSect1Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect2(self): return self.sect2
    def set_sect2(self, sect2): self.sect2 = sect2
    def add_sect2(self, value): self.sect2.append(value)
    def insert_sect2(self, index, value): self.sect2[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='docSect1Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docSect1Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docSect1Type'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docSect1Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docSect1Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'title', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect2':
            childobj_ = docSect2Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect2', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            childobj_ = docInternalS1Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'internal', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docSect1Type


class docSect2Type(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, title='', para=None, sect3=None, internal=None, mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docSect2Type.subclass:
            return docSect2Type.subclass(*args_, **kwargs_)
        else:
            return docSect2Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect3(self): return self.sect3
    def set_sect3(self, sect3): self.sect3 = sect3
    def add_sect3(self, value): self.sect3.append(value)
    def insert_sect3(self, index, value): self.sect3[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='docSect2Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docSect2Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docSect2Type'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docSect2Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docSect2Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'title', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect3':
            childobj_ = docSect3Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect3', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            childobj_ = docInternalS2Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'internal', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docSect2Type


class docSect3Type(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, title='', para=None, sect4=None, internal=None, mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docSect3Type.subclass:
            return docSect3Type.subclass(*args_, **kwargs_)
        else:
            return docSect3Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect4(self): return self.sect4
    def set_sect4(self, sect4): self.sect4 = sect4
    def add_sect4(self, value): self.sect4.append(value)
    def insert_sect4(self, index, value): self.sect4[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='docSect3Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docSect3Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docSect3Type'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docSect3Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docSect3Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'title', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect4':
            childobj_ = docSect4Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect4', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            childobj_ = docInternalS3Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'internal', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docSect3Type


class docSect4Type(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, title='', para=None, internal=None, mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docSect4Type.subclass:
            return docSect4Type.subclass(*args_, **kwargs_)
        else:
            return docSect4Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='docSect4Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docSect4Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docSect4Type'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docSect4Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docSect4Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'title', valuestr_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            childobj_ = docInternalS4Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'internal', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docSect4Type


class docInternalType(object):
    subclass = None
    superclass = None
    def __init__(self, para=None, sect1=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docInternalType.subclass:
            return docInternalType.subclass(*args_, **kwargs_)
        else:
            return docInternalType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect1(self): return self.sect1
    def set_sect1(self, sect1): self.sect1 = sect1
    def add_sect1(self, value): self.sect1.append(value)
    def insert_sect1(self, index, value): self.sect1[index] = value
    def export(self, outfile, level, namespace_='', name_='docInternalType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docInternalType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docInternalType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docInternalType'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docInternalType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect1':
            childobj_ = docSect1Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect1', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docInternalType


class docInternalS1Type(object):
    subclass = None
    superclass = None
    def __init__(self, para=None, sect2=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docInternalS1Type.subclass:
            return docInternalS1Type.subclass(*args_, **kwargs_)
        else:
            return docInternalS1Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect2(self): return self.sect2
    def set_sect2(self, sect2): self.sect2 = sect2
    def add_sect2(self, value): self.sect2.append(value)
    def insert_sect2(self, index, value): self.sect2[index] = value
    def export(self, outfile, level, namespace_='', name_='docInternalS1Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docInternalS1Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docInternalS1Type'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docInternalS1Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docInternalS1Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect2':
            childobj_ = docSect2Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect2', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docInternalS1Type


class docInternalS2Type(object):
    subclass = None
    superclass = None
    def __init__(self, para=None, sect3=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docInternalS2Type.subclass:
            return docInternalS2Type.subclass(*args_, **kwargs_)
        else:
            return docInternalS2Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect3(self): return self.sect3
    def set_sect3(self, sect3): self.sect3 = sect3
    def add_sect3(self, value): self.sect3.append(value)
    def insert_sect3(self, index, value): self.sect3[index] = value
    def export(self, outfile, level, namespace_='', name_='docInternalS2Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docInternalS2Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docInternalS2Type'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docInternalS2Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docInternalS2Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect3':
            childobj_ = docSect3Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect3', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docInternalS2Type


class docInternalS3Type(object):
    subclass = None
    superclass = None
    def __init__(self, para=None, sect3=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docInternalS3Type.subclass:
            return docInternalS3Type.subclass(*args_, **kwargs_)
        else:
            return docInternalS3Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect3(self): return self.sect3
    def set_sect3(self, sect3): self.sect3 = sect3
    def add_sect3(self, value): self.sect3.append(value)
    def insert_sect3(self, index, value): self.sect3[index] = value
    def export(self, outfile, level, namespace_='', name_='docInternalS3Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docInternalS3Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docInternalS3Type'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docInternalS3Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docInternalS3Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect3':
            childobj_ = docSect4Type.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sect3', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docInternalS3Type


class docInternalS4Type(object):
    subclass = None
    superclass = None
    def __init__(self, para=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docInternalS4Type.subclass:
            return docInternalS4Type.subclass(*args_, **kwargs_)
        else:
            return docInternalS4Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def export(self, outfile, level, namespace_='', name_='docInternalS4Type'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docInternalS4Type')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docInternalS4Type'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docInternalS4Type'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docInternalS4Type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            childobj_ = docParaType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'para', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docInternalS4Type


class docTitleType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docTitleType.subclass:
            return docTitleType.subclass(*args_, **kwargs_)
        else:
            return docTitleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docTitleType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docTitleType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docTitleType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docTitleType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docTitleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docTitleType


class docParaType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docParaType.subclass:
            return docParaType.subclass(*args_, **kwargs_)
        else:
            return docParaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docParaType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docParaType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docParaType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docParaType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docParaType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docParaType


class docMarkupType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docMarkupType.subclass:
            return docMarkupType.subclass(*args_, **kwargs_)
        else:
            return docMarkupType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docMarkupType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docMarkupType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docMarkupType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docMarkupType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docMarkupType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docMarkupType


class docURLLink(object):
    subclass = None
    superclass = None
    def __init__(self, url=None, valueOf_='', mixedclass_=None, content_=None):
        self.url = url
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docURLLink.subclass:
            return docURLLink.subclass(*args_, **kwargs_)
        else:
            return docURLLink(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_url(self): return self.url
    def set_url(self, url): self.url = url
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docURLLink'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docURLLink')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docURLLink'):
        if self.get_url() is not None:
            outfile.write(' url="%s"' % (quote_attrib(self.get_url()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docURLLink'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docURLLink'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('url = "%s",\n' % (self.get_url(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('url'):
            self.url = attrs.get('url').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docURLLink


class docAnchorType(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docAnchorType.subclass:
            return docAnchorType.subclass(*args_, **kwargs_)
        else:
            return docAnchorType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docAnchorType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docAnchorType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docAnchorType'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docAnchorType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docAnchorType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docAnchorType


class docFormulaType(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docFormulaType.subclass:
            return docFormulaType.subclass(*args_, **kwargs_)
        else:
            return docFormulaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docFormulaType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docFormulaType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docFormulaType'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docFormulaType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docFormulaType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docFormulaType


class docIndexEntryType(object):
    subclass = None
    superclass = None
    def __init__(self, primaryie='', secondaryie=''):
        self.primaryie = primaryie
        self.secondaryie = secondaryie
    def factory(*args_, **kwargs_):
        if docIndexEntryType.subclass:
            return docIndexEntryType.subclass(*args_, **kwargs_)
        else:
            return docIndexEntryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_primaryie(self): return self.primaryie
    def set_primaryie(self, primaryie): self.primaryie = primaryie
    def get_secondaryie(self): return self.secondaryie
    def set_secondaryie(self, secondaryie): self.secondaryie = secondaryie
    def export(self, outfile, level, namespace_='', name_='docIndexEntryType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docIndexEntryType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docIndexEntryType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docIndexEntryType'):
        showIndent(outfile, level)
        outfile.write('<%sprimaryie>%s</%sprimaryie>\n' % (namespace_, quote_xml(self.get_primaryie()), namespace_))
        showIndent(outfile, level)
        outfile.write('<%ssecondaryie>%s</%ssecondaryie>\n' % (namespace_, quote_xml(self.get_secondaryie()), namespace_))
    def exportLiteral(self, outfile, level, name_='docIndexEntryType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('primaryie=%s,\n' % quote_python(self.get_primaryie()))
        showIndent(outfile, level)
        outfile.write('secondaryie=%s,\n' % quote_python(self.get_secondaryie()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'primaryie':
            primaryie_ = ''
            for text__content_ in child_.childNodes:
                primaryie_ += text__content_.nodeValue
            self.primaryie = primaryie_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'secondaryie':
            secondaryie_ = ''
            for text__content_ in child_.childNodes:
                secondaryie_ += text__content_.nodeValue
            self.secondaryie = secondaryie_
# end class docIndexEntryType


class docListType(object):
    subclass = None
    superclass = None
    def __init__(self, listitem=None):
        if listitem is None:
            self.listitem = []
        else:
            self.listitem = listitem
    def factory(*args_, **kwargs_):
        if docListType.subclass:
            return docListType.subclass(*args_, **kwargs_)
        else:
            return docListType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_listitem(self): return self.listitem
    def set_listitem(self, listitem): self.listitem = listitem
    def add_listitem(self, value): self.listitem.append(value)
    def insert_listitem(self, index, value): self.listitem[index] = value
    def export(self, outfile, level, namespace_='', name_='docListType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docListType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docListType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docListType'):
        for listitem_ in self.get_listitem():
            listitem_.export(outfile, level, namespace_, name_='listitem')
    def exportLiteral(self, outfile, level, name_='docListType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('listitem=[\n')
        level += 1
        for listitem in self.listitem:
            showIndent(outfile, level)
            outfile.write('listitem(\n')
            listitem.exportLiteral(outfile, level, name_='listitem')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'listitem':
            obj_ = docListItemType.factory()
            obj_.build(child_)
            self.listitem.append(obj_)
# end class docListType


class docListItemType(object):
    subclass = None
    superclass = None
    def __init__(self, para=None):
        if para is None:
            self.para = []
        else:
            self.para = para
    def factory(*args_, **kwargs_):
        if docListItemType.subclass:
            return docListItemType.subclass(*args_, **kwargs_)
        else:
            return docListItemType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def export(self, outfile, level, namespace_='', name_='docListItemType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docListItemType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docListItemType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docListItemType'):
        for para_ in self.get_para():
            para_.export(outfile, level, namespace_, name_='para')
    def exportLiteral(self, outfile, level, name_='docListItemType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('para=[\n')
        level += 1
        for para in self.para:
            showIndent(outfile, level)
            outfile.write('para(\n')
            para.exportLiteral(outfile, level, name_='para')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            obj_ = docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)
# end class docListItemType


class docSimpleSectType(object):
    subclass = None
    superclass = None
    def __init__(self, kind=None, title=None, para=None):
        self.kind = kind
        self.title = title
        if para is None:
            self.para = []
        else:
            self.para = para
    def factory(*args_, **kwargs_):
        if docSimpleSectType.subclass:
            return docSimpleSectType.subclass(*args_, **kwargs_)
        else:
            return docSimpleSectType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_kind(self): return self.kind
    def set_kind(self, kind): self.kind = kind
    def export(self, outfile, level, namespace_='', name_='docSimpleSectType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docSimpleSectType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docSimpleSectType'):
        if self.get_kind() is not None:
            outfile.write(' kind="%s"' % str(self.get_kind()))
    def exportChildren(self, outfile, level, namespace_='', name_='docSimpleSectType'):
        if self.get_title() != None :
            if self.title:
                self.title.export(outfile, level, namespace_, name_='title')
        for para_ in self.get_para():
            para_.export(outfile, level, namespace_, name_='para')
    def exportLiteral(self, outfile, level, name_='docSimpleSectType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('kind = "%s",\n' % (self.get_kind(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title:
            showIndent(outfile, level)
            outfile.write('title=docTitleType(\n')
            self.title.exportLiteral(outfile, level, name_='title')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('para=[\n')
        level += 1
        for para in self.para:
            showIndent(outfile, level)
            outfile.write('para(\n')
            para.exportLiteral(outfile, level, name_='para')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('kind'):
            self.kind = attrs.get('kind').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = docTitleType.factory()
            obj_.build(child_)
            self.set_title(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            obj_ = docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)
# end class docSimpleSectType


class docVarListEntryType(object):
    subclass = None
    superclass = None
    def __init__(self, term=None):
        self.term = term
    def factory(*args_, **kwargs_):
        if docVarListEntryType.subclass:
            return docVarListEntryType.subclass(*args_, **kwargs_)
        else:
            return docVarListEntryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_term(self): return self.term
    def set_term(self, term): self.term = term
    def export(self, outfile, level, namespace_='', name_='docVarListEntryType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docVarListEntryType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docVarListEntryType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docVarListEntryType'):
        if self.term:
            self.term.export(outfile, level, namespace_, name_='term', )
    def exportLiteral(self, outfile, level, name_='docVarListEntryType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.term:
            showIndent(outfile, level)
            outfile.write('term=docTitleType(\n')
            self.term.exportLiteral(outfile, level, name_='term')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'term':
            obj_ = docTitleType.factory()
            obj_.build(child_)
            self.set_term(obj_)
# end class docVarListEntryType


class docVariableListType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if docVariableListType.subclass:
            return docVariableListType.subclass(*args_, **kwargs_)
        else:
            return docVariableListType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docVariableListType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docVariableListType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docVariableListType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docVariableListType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docVariableListType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docVariableListType


class docRefTextType(object):
    subclass = None
    superclass = None
    def __init__(self, refid=None, kindref=None, external=None, valueOf_='', mixedclass_=None, content_=None):
        self.refid = refid
        self.kindref = kindref
        self.external = external
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docRefTextType.subclass:
            return docRefTextType.subclass(*args_, **kwargs_)
        else:
            return docRefTextType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_refid(self): return self.refid
    def set_refid(self, refid): self.refid = refid
    def get_kindref(self): return self.kindref
    def set_kindref(self, kindref): self.kindref = kindref
    def get_external(self): return self.external
    def set_external(self, external): self.external = external
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docRefTextType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docRefTextType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docRefTextType'):
        if self.get_refid() is not None:
            outfile.write(' refid="%s"' % (quote_attrib(self.get_refid()), ))
        if self.get_kindref() is not None:
            outfile.write(' kindref="%s"' % str(self.get_kindref()))
        if self.get_external() is not None:
            outfile.write(' external="%s"' % (quote_attrib(self.get_external()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docRefTextType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docRefTextType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('refid = "%s",\n' % (self.get_refid(),))
        showIndent(outfile, level)
        wrt('kindref = "%s",\n' % (self.get_kindref(),))
        showIndent(outfile, level)
        wrt('external = "%s",\n' % (self.get_external(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('refid'):
            self.refid = attrs.get('refid').value
        if attrs.get('kindref'):
            self.kindref = attrs.get('kindref').value
        if attrs.get('external'):
            self.external = attrs.get('external').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docRefTextType


class docTableType(object):
    subclass = None
    superclass = None
    def __init__(self, rows=None, cols=None, row=None, caption=None):
        self.rows = rows
        self.cols = cols
        if row is None:
            self.row = []
        else:
            self.row = row
        self.caption = caption
    def factory(*args_, **kwargs_):
        if docTableType.subclass:
            return docTableType.subclass(*args_, **kwargs_)
        else:
            return docTableType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_row(self): return self.row
    def set_row(self, row): self.row = row
    def add_row(self, value): self.row.append(value)
    def insert_row(self, index, value): self.row[index] = value
    def get_caption(self): return self.caption
    def set_caption(self, caption): self.caption = caption
    def get_rows(self): return self.rows
    def set_rows(self, rows): self.rows = rows
    def get_cols(self): return self.cols
    def set_cols(self, cols): self.cols = cols
    def export(self, outfile, level, namespace_='', name_='docTableType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docTableType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docTableType'):
        if self.get_rows() is not None:
            outfile.write(' rows="%d"' % self.get_rows())
        if self.get_cols() is not None:
            outfile.write(' cols="%d"' % self.get_cols())
    def exportChildren(self, outfile, level, namespace_='', name_='docTableType'):
        for row_ in self.get_row():
            row_.export(outfile, level, namespace_, name_='row')
        if self.get_caption() != None :
            if self.caption:
                self.caption.export(outfile, level, namespace_, name_='caption')
    def exportLiteral(self, outfile, level, name_='docTableType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('rows = "%s",\n' % (self.get_rows(),))
        showIndent(outfile, level)
        wrt('cols = "%s",\n' % (self.get_cols(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('row=[\n')
        level += 1
        for row in self.row:
            showIndent(outfile, level)
            outfile.write('row(\n')
            row.exportLiteral(outfile, level, name_='row')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.caption:
            showIndent(outfile, level)
            outfile.write('caption=docCaptionType(\n')
            self.caption.exportLiteral(outfile, level, name_='caption')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('rows'):
            try:
                self.rows = int(attrs.get('rows').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (rows): %s' % exp)
        if attrs.get('cols'):
            try:
                self.cols = int(attrs.get('cols').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (cols): %s' % exp)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'row':
            obj_ = docRowType.factory()
            obj_.build(child_)
            self.row.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'caption':
            obj_ = docCaptionType.factory()
            obj_.build(child_)
            self.set_caption(obj_)
# end class docTableType


class docRowType(object):
    subclass = None
    superclass = None
    def __init__(self, entry=None):
        if entry is None:
            self.entry = []
        else:
            self.entry = entry
    def factory(*args_, **kwargs_):
        if docRowType.subclass:
            return docRowType.subclass(*args_, **kwargs_)
        else:
            return docRowType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_entry(self): return self.entry
    def set_entry(self, entry): self.entry = entry
    def add_entry(self, value): self.entry.append(value)
    def insert_entry(self, index, value): self.entry[index] = value
    def export(self, outfile, level, namespace_='', name_='docRowType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docRowType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docRowType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docRowType'):
        for entry_ in self.get_entry():
            entry_.export(outfile, level, namespace_, name_='entry')
    def exportLiteral(self, outfile, level, name_='docRowType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('entry=[\n')
        level += 1
        for entry in self.entry:
            showIndent(outfile, level)
            outfile.write('entry(\n')
            entry.exportLiteral(outfile, level, name_='entry')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'entry':
            obj_ = docEntryType.factory()
            obj_.build(child_)
            self.entry.append(obj_)
# end class docRowType


class docEntryType(object):
    subclass = None
    superclass = None
    def __init__(self, thead=None, para=None):
        self.thead = thead
        if para is None:
            self.para = []
        else:
            self.para = para
    def factory(*args_, **kwargs_):
        if docEntryType.subclass:
            return docEntryType.subclass(*args_, **kwargs_)
        else:
            return docEntryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_thead(self): return self.thead
    def set_thead(self, thead): self.thead = thead
    def export(self, outfile, level, namespace_='', name_='docEntryType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docEntryType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docEntryType'):
        if self.get_thead() is not None:
            outfile.write(' thead="%s"' % str(self.get_thead()))
    def exportChildren(self, outfile, level, namespace_='', name_='docEntryType'):
        for para_ in self.get_para():
            para_.export(outfile, level, namespace_, name_='para')
    def exportLiteral(self, outfile, level, name_='docEntryType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('thead = "%s",\n' % (self.get_thead(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('para=[\n')
        level += 1
        for para in self.para:
            showIndent(outfile, level)
            outfile.write('para(\n')
            para.exportLiteral(outfile, level, name_='para')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('thead'):
            self.thead = attrs.get('thead').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            obj_ = docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)
# end class docEntryType


class docCaptionType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docCaptionType.subclass:
            return docCaptionType.subclass(*args_, **kwargs_)
        else:
            return docCaptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docCaptionType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docCaptionType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docCaptionType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docCaptionType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docCaptionType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docCaptionType


class docHeadingType(object):
    subclass = None
    superclass = None
    def __init__(self, level=None, valueOf_='', mixedclass_=None, content_=None):
        self.level = level
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docHeadingType.subclass:
            return docHeadingType.subclass(*args_, **kwargs_)
        else:
            return docHeadingType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_level(self): return self.level
    def set_level(self, level): self.level = level
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docHeadingType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docHeadingType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docHeadingType'):
        if self.get_level() is not None:
            outfile.write(' level="%d"' % self.get_level())
    def exportChildren(self, outfile, level, namespace_='', name_='docHeadingType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docHeadingType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('level = "%s",\n' % (self.get_level(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('level'):
            try:
                self.level = int(attrs.get('level').value)
            except ValueError, exp:
                raise ValueError('Bad integer attribute (level): %s' % exp)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docHeadingType


class docImageType(object):
    subclass = None
    superclass = None
    def __init__(self, width=None, typexx=None, name=None, height=None, valueOf_='', mixedclass_=None, content_=None):
        self.width = width
        self.typexx = typexx
        self.name = name
        self.height = height
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docImageType.subclass:
            return docImageType.subclass(*args_, **kwargs_)
        else:
            return docImageType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_width(self): return self.width
    def set_width(self, width): self.width = width
    def get_type(self): return self.typexx
    def set_type(self, typexx): self.typexx = typexx
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_height(self): return self.height
    def set_height(self, height): self.height = height
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docImageType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docImageType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docImageType'):
        if self.get_width() is not None:
            outfile.write(' width="%s"' % (quote_attrib(self.get_width()), ))
        if self.get_type() is not None:
            outfile.write(' type="%s"' % str(self.get_type()))
        if self.get_name() is not None:
            outfile.write(' name="%s"' % (quote_attrib(self.get_name()), ))
        if self.get_height() is not None:
            outfile.write(' height="%s"' % (quote_attrib(self.get_height()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docImageType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docImageType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('width = "%s",\n' % (self.get_width(),))
        showIndent(outfile, level)
        wrt('typexx = "%s",\n' % (self.get_type(),))
        showIndent(outfile, level)
        wrt('name = "%s",\n' % (self.get_name(),))
        showIndent(outfile, level)
        wrt('height = "%s",\n' % (self.get_height(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('width'):
            self.width = attrs.get('width').value
        if attrs.get('type'):
            self.typexx = attrs.get('type').value
        if attrs.get('name'):
            self.name = attrs.get('name').value
        if attrs.get('height'):
            self.height = attrs.get('height').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docImageType


class docDotFileType(object):
    subclass = None
    superclass = None
    def __init__(self, name=None, valueOf_='', mixedclass_=None, content_=None):
        self.name = name
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docDotFileType.subclass:
            return docDotFileType.subclass(*args_, **kwargs_)
        else:
            return docDotFileType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docDotFileType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docDotFileType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docDotFileType'):
        if self.get_name() is not None:
            outfile.write(' name="%s"' % (quote_attrib(self.get_name()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docDotFileType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docDotFileType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('name = "%s",\n' % (self.get_name(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('name'):
            self.name = attrs.get('name').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docDotFileType


class docTocItemType(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docTocItemType.subclass:
            return docTocItemType.subclass(*args_, **kwargs_)
        else:
            return docTocItemType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docTocItemType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docTocItemType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docTocItemType'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docTocItemType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docTocItemType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docTocItemType


class docTocListType(object):
    subclass = None
    superclass = None
    def __init__(self, tocitem=None):
        if tocitem is None:
            self.tocitem = []
        else:
            self.tocitem = tocitem
    def factory(*args_, **kwargs_):
        if docTocListType.subclass:
            return docTocListType.subclass(*args_, **kwargs_)
        else:
            return docTocListType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_tocitem(self): return self.tocitem
    def set_tocitem(self, tocitem): self.tocitem = tocitem
    def add_tocitem(self, value): self.tocitem.append(value)
    def insert_tocitem(self, index, value): self.tocitem[index] = value
    def export(self, outfile, level, namespace_='', name_='docTocListType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docTocListType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docTocListType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docTocListType'):
        for tocitem_ in self.get_tocitem():
            tocitem_.export(outfile, level, namespace_, name_='tocitem')
    def exportLiteral(self, outfile, level, name_='docTocListType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('tocitem=[\n')
        level += 1
        for tocitem in self.tocitem:
            showIndent(outfile, level)
            outfile.write('tocitem(\n')
            tocitem.exportLiteral(outfile, level, name_='tocitem')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'tocitem':
            obj_ = docTocItemType.factory()
            obj_.build(child_)
            self.tocitem.append(obj_)
# end class docTocListType


class docLanguageType(object):
    subclass = None
    superclass = None
    def __init__(self, langid=None, para=None):
        self.langid = langid
        if para is None:
            self.para = []
        else:
            self.para = para
    def factory(*args_, **kwargs_):
        if docLanguageType.subclass:
            return docLanguageType.subclass(*args_, **kwargs_)
        else:
            return docLanguageType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_langid(self): return self.langid
    def set_langid(self, langid): self.langid = langid
    def export(self, outfile, level, namespace_='', name_='docLanguageType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docLanguageType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docLanguageType'):
        if self.get_langid() is not None:
            outfile.write(' langid="%s"' % (quote_attrib(self.get_langid()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docLanguageType'):
        for para_ in self.get_para():
            para_.export(outfile, level, namespace_, name_='para')
    def exportLiteral(self, outfile, level, name_='docLanguageType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('langid = "%s",\n' % (self.get_langid(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('para=[\n')
        level += 1
        for para in self.para:
            showIndent(outfile, level)
            outfile.write('para(\n')
            para.exportLiteral(outfile, level, name_='para')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('langid'):
            self.langid = attrs.get('langid').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            obj_ = docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)
# end class docLanguageType


class docParamListType(object):
    subclass = None
    superclass = None
    def __init__(self, kind=None, parameteritem=None):
        self.kind = kind
        if parameteritem is None:
            self.parameteritem = []
        else:
            self.parameteritem = parameteritem
    def factory(*args_, **kwargs_):
        if docParamListType.subclass:
            return docParamListType.subclass(*args_, **kwargs_)
        else:
            return docParamListType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_parameteritem(self): return self.parameteritem
    def set_parameteritem(self, parameteritem): self.parameteritem = parameteritem
    def add_parameteritem(self, value): self.parameteritem.append(value)
    def insert_parameteritem(self, index, value): self.parameteritem[index] = value
    def get_kind(self): return self.kind
    def set_kind(self, kind): self.kind = kind
    def export(self, outfile, level, namespace_='', name_='docParamListType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docParamListType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docParamListType'):
        if self.get_kind() is not None:
            outfile.write(' kind="%s"' % str(self.get_kind()))
    def exportChildren(self, outfile, level, namespace_='', name_='docParamListType'):
        for parameteritem_ in self.get_parameteritem():
            parameteritem_.export(outfile, level, namespace_, name_='parameteritem')
    def exportLiteral(self, outfile, level, name_='docParamListType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('kind = "%s",\n' % (self.get_kind(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('parameteritem=[\n')
        level += 1
        for parameteritem in self.parameteritem:
            showIndent(outfile, level)
            outfile.write('parameteritem(\n')
            parameteritem.exportLiteral(outfile, level, name_='parameteritem')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('kind'):
            self.kind = attrs.get('kind').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'parameteritem':
            obj_ = docParamListItem.factory()
            obj_.build(child_)
            self.parameteritem.append(obj_)
# end class docParamListType


class docParamListItem(object):
    subclass = None
    superclass = None
    def __init__(self, parameternamelist=None, parameterdescription=None):
        if parameternamelist is None:
            self.parameternamelist = []
        else:
            self.parameternamelist = parameternamelist
        self.parameterdescription = parameterdescription
    def factory(*args_, **kwargs_):
        if docParamListItem.subclass:
            return docParamListItem.subclass(*args_, **kwargs_)
        else:
            return docParamListItem(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_parameternamelist(self): return self.parameternamelist
    def set_parameternamelist(self, parameternamelist): self.parameternamelist = parameternamelist
    def add_parameternamelist(self, value): self.parameternamelist.append(value)
    def insert_parameternamelist(self, index, value): self.parameternamelist[index] = value
    def get_parameterdescription(self): return self.parameterdescription
    def set_parameterdescription(self, parameterdescription): self.parameterdescription = parameterdescription
    def export(self, outfile, level, namespace_='', name_='docParamListItem'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docParamListItem')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docParamListItem'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docParamListItem'):
        for parameternamelist_ in self.get_parameternamelist():
            parameternamelist_.export(outfile, level, namespace_, name_='parameternamelist')
        if self.parameterdescription:
            self.parameterdescription.export(outfile, level, namespace_, name_='parameterdescription', )
    def exportLiteral(self, outfile, level, name_='docParamListItem'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('parameternamelist=[\n')
        level += 1
        for parameternamelist in self.parameternamelist:
            showIndent(outfile, level)
            outfile.write('parameternamelist(\n')
            parameternamelist.exportLiteral(outfile, level, name_='parameternamelist')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.parameterdescription:
            showIndent(outfile, level)
            outfile.write('parameterdescription=descriptionType(\n')
            self.parameterdescription.exportLiteral(outfile, level, name_='parameterdescription')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'parameternamelist':
            obj_ = docParamNameList.factory()
            obj_.build(child_)
            self.parameternamelist.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'parameterdescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_parameterdescription(obj_)
# end class docParamListItem


class docParamNameList(object):
    subclass = None
    superclass = None
    def __init__(self, parametername=None):
        if parametername is None:
            self.parametername = []
        else:
            self.parametername = parametername
    def factory(*args_, **kwargs_):
        if docParamNameList.subclass:
            return docParamNameList.subclass(*args_, **kwargs_)
        else:
            return docParamNameList(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_parametername(self): return self.parametername
    def set_parametername(self, parametername): self.parametername = parametername
    def add_parametername(self, value): self.parametername.append(value)
    def insert_parametername(self, index, value): self.parametername[index] = value
    def export(self, outfile, level, namespace_='', name_='docParamNameList'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docParamNameList')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docParamNameList'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docParamNameList'):
        for parametername_ in self.get_parametername():
            parametername_.export(outfile, level, namespace_, name_='parametername')
    def exportLiteral(self, outfile, level, name_='docParamNameList'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('parametername=[\n')
        level += 1
        for parametername in self.parametername:
            showIndent(outfile, level)
            outfile.write('parametername(\n')
            parametername.exportLiteral(outfile, level, name_='parametername')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'parametername':
            obj_ = docParamName.factory()
            obj_.build(child_)
            self.parametername.append(obj_)
# end class docParamNameList


class docParamName(object):
    subclass = None
    superclass = None
    def __init__(self, direction=None, ref=None, mixedclass_=None, content_=None):
        self.direction = direction
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if docParamName.subclass:
            return docParamName.subclass(*args_, **kwargs_)
        else:
            return docParamName(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ref(self): return self.ref
    def set_ref(self, ref): self.ref = ref
    def get_direction(self): return self.direction
    def set_direction(self, direction): self.direction = direction
    def export(self, outfile, level, namespace_='', name_='docParamName'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docParamName')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docParamName'):
        if self.get_direction() is not None:
            outfile.write(' direction="%s"' % str(self.get_direction()))
    def exportChildren(self, outfile, level, namespace_='', name_='docParamName'):
        for item_ in self.content_:
            item_.export(outfile, level, namespace_, name_)
    def exportLiteral(self, outfile, level, name_='docParamName'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('direction = "%s",\n' % (self.get_direction(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('direction'):
            self.direction = attrs.get('direction').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'ref':
            childobj_ = refTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ref', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class docParamName


class docXRefSectType(object):
    subclass = None
    superclass = None
    def __init__(self, id=None, xreftitle=None, xrefdescription=None):
        self.id = id
        if xreftitle is None:
            self.xreftitle = []
        else:
            self.xreftitle = xreftitle
        self.xrefdescription = xrefdescription
    def factory(*args_, **kwargs_):
        if docXRefSectType.subclass:
            return docXRefSectType.subclass(*args_, **kwargs_)
        else:
            return docXRefSectType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_xreftitle(self): return self.xreftitle
    def set_xreftitle(self, xreftitle): self.xreftitle = xreftitle
    def add_xreftitle(self, value): self.xreftitle.append(value)
    def insert_xreftitle(self, index, value): self.xreftitle[index] = value
    def get_xrefdescription(self): return self.xrefdescription
    def set_xrefdescription(self, xrefdescription): self.xrefdescription = xrefdescription
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='docXRefSectType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docXRefSectType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docXRefSectType'):
        if self.get_id() is not None:
            outfile.write(' id="%s"' % (quote_attrib(self.get_id()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docXRefSectType'):
        for xreftitle_ in self.get_xreftitle():
            showIndent(outfile, level)
            outfile.write('<%sxreftitle>%s</%sxreftitle>\n' % (namespace_, quote_xml(xreftitle_), namespace_))
        if self.xrefdescription:
            self.xrefdescription.export(outfile, level, namespace_, name_='xrefdescription', )
    def exportLiteral(self, outfile, level, name_='docXRefSectType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('id = "%s",\n' % (self.get_id(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('xreftitle=[\n')
        level += 1
        for xreftitle in self.xreftitle:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(xreftitle))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.xrefdescription:
            showIndent(outfile, level)
            outfile.write('xrefdescription=descriptionType(\n')
            self.xrefdescription.exportLiteral(outfile, level, name_='xrefdescription')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'xreftitle':
            xreftitle_ = ''
            for text__content_ in child_.childNodes:
                xreftitle_ += text__content_.nodeValue
            self.xreftitle.append(xreftitle_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'xrefdescription':
            obj_ = descriptionType.factory()
            obj_.build(child_)
            self.set_xrefdescription(obj_)
# end class docXRefSectType


class docCopyType(object):
    subclass = None
    superclass = None
    def __init__(self, link=None, para=None, sect1=None, internal=None):
        self.link = link
        if para is None:
            self.para = []
        else:
            self.para = para
        if sect1 is None:
            self.sect1 = []
        else:
            self.sect1 = sect1
        self.internal = internal
    def factory(*args_, **kwargs_):
        if docCopyType.subclass:
            return docCopyType.subclass(*args_, **kwargs_)
        else:
            return docCopyType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_para(self): return self.para
    def set_para(self, para): self.para = para
    def add_para(self, value): self.para.append(value)
    def insert_para(self, index, value): self.para[index] = value
    def get_sect1(self): return self.sect1
    def set_sect1(self, sect1): self.sect1 = sect1
    def add_sect1(self, value): self.sect1.append(value)
    def insert_sect1(self, index, value): self.sect1[index] = value
    def get_internal(self): return self.internal
    def set_internal(self, internal): self.internal = internal
    def get_link(self): return self.link
    def set_link(self, link): self.link = link
    def export(self, outfile, level, namespace_='', name_='docCopyType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docCopyType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docCopyType'):
        if self.get_link() is not None:
            outfile.write(' link="%s"' % (quote_attrib(self.get_link()), ))
    def exportChildren(self, outfile, level, namespace_='', name_='docCopyType'):
        for para_ in self.get_para():
            para_.export(outfile, level, namespace_, name_='para')
        for sect1_ in self.get_sect1():
            sect1_.export(outfile, level, namespace_, name_='sect1')
        if self.get_internal() != None :
            if self.internal:
                self.internal.export(outfile, level, namespace_, name_='internal')
    def exportLiteral(self, outfile, level, name_='docCopyType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('link = "%s",\n' % (self.get_link(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('para=[\n')
        level += 1
        for para in self.para:
            showIndent(outfile, level)
            outfile.write('para(\n')
            para.exportLiteral(outfile, level, name_='para')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('sect1=[\n')
        level += 1
        for sect1 in self.sect1:
            showIndent(outfile, level)
            outfile.write('sect1(\n')
            sect1.exportLiteral(outfile, level, name_='sect1')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.internal:
            showIndent(outfile, level)
            outfile.write('internal=docInternalType(\n')
            self.internal.exportLiteral(outfile, level, name_='internal')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('link'):
            self.link = attrs.get('link').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'para':
            obj_ = docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sect1':
            obj_ = docSect1Type.factory()
            obj_.build(child_)
            self.sect1.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'internal':
            obj_ = docInternalType.factory()
            obj_.build(child_)
            self.set_internal(obj_)
# end class docCopyType


class docCharType(object):
    subclass = None
    superclass = None
    def __init__(self, char=None, valueOf_=''):
        self.char = char
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if docCharType.subclass:
            return docCharType.subclass(*args_, **kwargs_)
        else:
            return docCharType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_char(self): return self.char
    def set_char(self, char): self.char = char
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docCharType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docCharType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docCharType'):
        if self.get_char() is not None:
            outfile.write(' char="%s"' % str(self.get_char()))
    def exportChildren(self, outfile, level, namespace_='', name_='docCharType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docCharType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        wrt('char = "%s",\n' % (self.get_char(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('char'):
            self.char = attrs.get('char').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docCharType


class docEmptyType(object):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if docEmptyType.subclass:
            return docEmptyType.subclass(*args_, **kwargs_)
        else:
            return docEmptyType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='docEmptyType'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='docEmptyType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='docEmptyType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='docEmptyType'):
        outfile.write(quote_xml('%s' % self.valueOf_))
    def exportLiteral(self, outfile, level, name_='docEmptyType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class docEmptyType


from xml.sax import handler, make_parser

class SaxStackElement:
    def __init__(self, name='', obj=None):
        self.name = name
        self.obj = obj
        self.content = ''

#
# SAX handler
#
class Sax_doxygenHandler(handler.ContentHandler):
    def __init__(self):
        self.stack = []
        self.root = None

    def getRoot(self):
        return self.root

    def setDocumentLocator(self, locator):
        self.locator = locator
    
    def showError(self, msg):
        print '*** (showError):', msg
        sys.exit(-1)

    def startElement(self, name, attrs):
        done = 0
        if name == 'doxygen':
            obj = doxygen.factory()
            stackObj = SaxStackElement('doxygen', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'compounddef':
            obj = compounddefType.factory()
            stackObj = SaxStackElement('compounddef', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'compoundname':
            stackObj = SaxStackElement('compoundname', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'title':
            stackObj = SaxStackElement('title', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'basecompoundref':
            obj = compoundRefType.factory()
            stackObj = SaxStackElement('basecompoundref', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'derivedcompoundref':
            obj = compoundRefType.factory()
            stackObj = SaxStackElement('derivedcompoundref', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'includes':
            obj = incType.factory()
            stackObj = SaxStackElement('includes', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'includedby':
            obj = incType.factory()
            stackObj = SaxStackElement('includedby', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'incdepgraph':
            obj = graphType.factory()
            stackObj = SaxStackElement('incdepgraph', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'invincdepgraph':
            obj = graphType.factory()
            stackObj = SaxStackElement('invincdepgraph', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innerdir':
            obj = refType.factory()
            stackObj = SaxStackElement('innerdir', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innerfile':
            obj = refType.factory()
            stackObj = SaxStackElement('innerfile', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innerclass':
            obj = refType.factory()
            stackObj = SaxStackElement('innerclass', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innernamespace':
            obj = refType.factory()
            stackObj = SaxStackElement('innernamespace', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innerpage':
            obj = refType.factory()
            stackObj = SaxStackElement('innerpage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'innergroup':
            obj = refType.factory()
            stackObj = SaxStackElement('innergroup', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'templateparamlist':
            obj = templateparamlistType.factory()
            stackObj = SaxStackElement('templateparamlist', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sectiondef':
            obj = sectiondefType.factory()
            stackObj = SaxStackElement('sectiondef', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'briefdescription':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('briefdescription', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'detaileddescription':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('detaileddescription', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'inheritancegraph':
            obj = graphType.factory()
            stackObj = SaxStackElement('inheritancegraph', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'collaborationgraph':
            obj = graphType.factory()
            stackObj = SaxStackElement('collaborationgraph', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'programlisting':
            obj = listingType.factory()
            stackObj = SaxStackElement('programlisting', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'location':
            obj = locationType.factory()
            stackObj = SaxStackElement('location', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'listofallmembers':
            obj = listofallmembersType.factory()
            stackObj = SaxStackElement('listofallmembers', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'member':
            obj = memberRefType.factory()
            stackObj = SaxStackElement('member', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'scope':
            stackObj = SaxStackElement('scope', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'name':
            stackObj = SaxStackElement('name', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'header':
            stackObj = SaxStackElement('header', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'description':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('description', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'memberdef':
            obj = memberdefType.factory()
            stackObj = SaxStackElement('memberdef', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'type':
            obj = linkedTextType.factory()
            stackObj = SaxStackElement('typexx', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'definition':
            stackObj = SaxStackElement('definition', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'argsstring':
            stackObj = SaxStackElement('argsstring', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'read':
            stackObj = SaxStackElement('read', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'write':
            stackObj = SaxStackElement('write', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'bitfield':
            stackObj = SaxStackElement('bitfield', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'reimplements':
            obj = reimplementType.factory()
            stackObj = SaxStackElement('reimplements', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'reimplementedby':
            obj = reimplementType.factory()
            stackObj = SaxStackElement('reimplementedby', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'param':
            obj = paramType.factory()
            stackObj = SaxStackElement('param', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'enumvalue':
            obj = enumvalueType.factory()
            stackObj = SaxStackElement('enumvalue', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'initializer':
            obj = linkedTextType.factory()
            stackObj = SaxStackElement('initializer', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'exceptions':
            obj = linkedTextType.factory()
            stackObj = SaxStackElement('exceptions', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'inbodydescription':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('inbodydescription', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'references':
            obj = referenceType.factory()
            stackObj = SaxStackElement('references', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'referencedby':
            obj = referenceType.factory()
            stackObj = SaxStackElement('referencedby', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'para':
            obj = docParaType.factory()
            stackObj = SaxStackElement('para', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sect1':
            obj = docSect1Type.factory()
            stackObj = SaxStackElement('sect1', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'internal':
            obj = docInternalType.factory()
            stackObj = SaxStackElement('internal', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'declname':
            stackObj = SaxStackElement('declname', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'defname':
            stackObj = SaxStackElement('defname', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'array':
            stackObj = SaxStackElement('array', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'defval':
            obj = linkedTextType.factory()
            stackObj = SaxStackElement('defval', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'ref':
            obj = refTextType.factory()
            stackObj = SaxStackElement('ref', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'node':
            obj = nodeType.factory()
            stackObj = SaxStackElement('node', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'label':
            stackObj = SaxStackElement('label', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'link':
            obj = linkType.factory()
            stackObj = SaxStackElement('link', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'childnode':
            obj = childnodeType.factory()
            stackObj = SaxStackElement('childnode', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'edgelabel':
            stackObj = SaxStackElement('edgelabel', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'codeline':
            obj = codelineType.factory()
            stackObj = SaxStackElement('codeline', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'highlight':
            obj = highlightType.factory()
            stackObj = SaxStackElement('highlight', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sp':
            stackObj = SaxStackElement('sp', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sect2':
            obj = docSect2Type.factory()
            stackObj = SaxStackElement('sect2', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sect3':
            obj = docSect3Type.factory()
            stackObj = SaxStackElement('sect3', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sect4':
            obj = docSect4Type.factory()
            stackObj = SaxStackElement('sect4', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'primaryie':
            stackObj = SaxStackElement('primaryie', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'secondaryie':
            stackObj = SaxStackElement('secondaryie', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'listitem':
            obj = docListItemType.factory()
            stackObj = SaxStackElement('listitem', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'term':
            obj = docTitleType.factory()
            stackObj = SaxStackElement('term', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'row':
            obj = docRowType.factory()
            stackObj = SaxStackElement('row', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'caption':
            obj = docCaptionType.factory()
            stackObj = SaxStackElement('caption', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'entry':
            obj = docEntryType.factory()
            stackObj = SaxStackElement('entry', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'tocitem':
            obj = docTocItemType.factory()
            stackObj = SaxStackElement('tocitem', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'parameteritem':
            obj = docParamListItem.factory()
            stackObj = SaxStackElement('parameteritem', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'parameternamelist':
            obj = docParamNameList.factory()
            stackObj = SaxStackElement('parameternamelist', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'parameterdescription':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('parameterdescription', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'parametername':
            obj = docParamName.factory()
            stackObj = SaxStackElement('parametername', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'xreftitle':
            stackObj = SaxStackElement('xreftitle', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'xrefdescription':
            obj = descriptionType.factory()
            stackObj = SaxStackElement('xrefdescription', obj)
            self.stack.append(stackObj)
            done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def endElement(self, name):
        done = 0
        if name == 'doxygen':
            if len(self.stack) == 1:
                self.root = self.stack[-1].obj
                self.stack.pop()
                done = 1
        elif name == 'compounddef':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_compounddef(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'compoundname':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_compoundname(content)
                self.stack.pop()
                done = 1
        elif name == 'title':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_title(content)
                self.stack.pop()
                done = 1
        elif name == 'basecompoundref':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_basecompoundref(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'derivedcompoundref':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_derivedcompoundref(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'includes':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_includes(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'includedby':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_includedby(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'incdepgraph':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_incdepgraph(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'invincdepgraph':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_invincdepgraph(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innerdir':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innerdir(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innerfile':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innerfile(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innerclass':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innerclass(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innernamespace':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innernamespace(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innerpage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innerpage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'innergroup':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_innergroup(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'templateparamlist':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_templateparamlist(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sectiondef':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_sectiondef(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'briefdescription':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_briefdescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'detaileddescription':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_detaileddescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'inheritancegraph':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_inheritancegraph(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'collaborationgraph':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_collaborationgraph(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'programlisting':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_programlisting(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'location':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_location(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'listofallmembers':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_listofallmembers(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'member':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_member(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'scope':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_scope(content)
                self.stack.pop()
                done = 1
        elif name == 'name':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_name(content)
                self.stack.pop()
                done = 1
        elif name == 'header':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_header(content)
                self.stack.pop()
                done = 1
        elif name == 'description':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_description(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'memberdef':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_memberdef(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'type':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_type(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'definition':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_definition(content)
                self.stack.pop()
                done = 1
        elif name == 'argsstring':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_argsstring(content)
                self.stack.pop()
                done = 1
        elif name == 'read':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_read(content)
                self.stack.pop()
                done = 1
        elif name == 'write':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_write(content)
                self.stack.pop()
                done = 1
        elif name == 'bitfield':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_bitfield(content)
                self.stack.pop()
                done = 1
        elif name == 'reimplements':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_reimplements(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'reimplementedby':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_reimplementedby(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'param':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_param(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'enumvalue':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_enumvalue(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'initializer':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_initializer(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'exceptions':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_exceptions(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'inbodydescription':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_inbodydescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'references':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_references(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'referencedby':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_referencedby(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'para':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_para(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sect1':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_sect1(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'internal':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_internal(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'declname':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_declname(content)
                self.stack.pop()
                done = 1
        elif name == 'defname':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_defname(content)
                self.stack.pop()
                done = 1
        elif name == 'array':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_array(content)
                self.stack.pop()
                done = 1
        elif name == 'defval':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_defval(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'ref':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_ref(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'node':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_node(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'label':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_label(content)
                self.stack.pop()
                done = 1
        elif name == 'link':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_link(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'childnode':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_childnode(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'edgelabel':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.add_edgelabel(content)
                self.stack.pop()
                done = 1
        elif name == 'codeline':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_codeline(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'highlight':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_highlight(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sp':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.add_sp(content)
                self.stack.pop()
                done = 1
        elif name == 'sect2':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_sect2(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sect3':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_sect3(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sect4':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_sect4(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'primaryie':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_primaryie(content)
                self.stack.pop()
                done = 1
        elif name == 'secondaryie':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_secondaryie(content)
                self.stack.pop()
                done = 1
        elif name == 'listitem':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_listitem(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'term':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_term(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'row':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_row(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'caption':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_caption(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'entry':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_entry(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'tocitem':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_tocitem(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'parameteritem':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_parameteritem(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'parameternamelist':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_parameternamelist(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'parameterdescription':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_parameterdescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'parametername':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_parametername(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'xreftitle':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.add_xreftitle(content)
                self.stack.pop()
                done = 1
        elif name == 'xrefdescription':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_xrefdescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def characters(self, chrs, start, end):
        if len(self.stack) > 0:
            self.stack[-1].content += chrs[start:end]

    def reportError(self, mesg):
        locator = self.locator
        sys.stderr.write('Doc: %s  Line: %d  Column: %d\n' % \
            (locator.getSystemId(), locator.getLineNumber(), 
            locator.getColumnNumber() + 1))
        sys.stderr.write(mesg)
        sys.stderr.write('\n')
        sys.exit(-1)
        #raise RuntimeError

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
Options:
    -s        Use the SAX parser, not the minidom parser.
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


#
# SAX handler used to determine the top level element.
#
class SaxSelectorHandler(handler.ContentHandler):
    def __init__(self):
        self.topElementName = None
    def getTopElementName(self):
        return self.topElementName
    def startElement(self, name, attrs):
        self.topElementName = name
        raise StopIteration


def parseSelect(inFileName):
    infile = file(inFileName, 'r')
    topElementName = None
    parser = make_parser()
    documentHandler = SaxSelectorHandler()
    parser.setContentHandler(documentHandler)
    try:
        try:
            parser.parse(infile)
        except StopIteration:
            topElementName = documentHandler.getTopElementName()
        if topElementName is None:
            raise RuntimeError, 'no top level element'
        topElementName = topElementName.replace('-', '_').replace(':', '_')
        if topElementName not in globals():
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = globals()[topElementName]
        infile.seek(0)
        doc = minidom.parse(infile)
    finally:
        infile.close()
    rootNode = doc.childNodes[0]
    rootObj = topElement.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParse(inFileName):
    parser = make_parser()
    documentHandler = Sax_doxygenHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    rootObj = documentHandler.getRoot()
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParseString(inString):
    parser = make_parser()
    documentHandler = Sax_doxygenHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = DoxygenType.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="doxygen")
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = DoxygenType.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="doxygen")
    return rootObj


def parseLiteral(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = DoxygenType.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('from compoundsuper import *\n\n')
    sys.stdout.write('rootObj = doxygen(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="doxygen")
    sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-s':
        saxParse(args[1])
    elif len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')

