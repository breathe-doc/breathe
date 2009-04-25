#!/usr/bin/env python

"""
Generated Mon Feb  9 19:08:05 2009 by generateDS.py.
"""

from xml.dom import minidom
from docutils import nodes

import os
import sys
import breathe.doxparsers.compound

import indexsuper as supermod

class DoxygenTypeSub(supermod.DoxygenType):
    def __init__(self, version=None, compound=None):
        supermod.DoxygenType.__init__(self, version, compound)

    def rst_nodes(self, path):

        nodelist = []

        # Process all the compound children
        for compound in self.compound:
            nodelist.extend(compound.rst_nodes(path))

        return nodelist

supermod.DoxygenType.subclass = DoxygenTypeSub
# end class DoxygenTypeSub


class CompoundTypeSub(supermod.CompoundType):
    def __init__(self, kind=None, refid=None, name='', member=None):
        supermod.CompoundType.__init__(self, kind, refid, name, member)

    def rst_nodes(self, path):
        
        # Set up the title and a reference for it (refid)
        kind = nodes.emphasis(text=self.kind)
        name = nodes.strong(text=self.name)
        nodelist = [nodes.paragraph("", "", kind, nodes.Text(" "), name, ids=[self.refid])]

        # Read in the corresponding xml file and process
        ref_xml_path = os.path.join( path, "%s.xml" % self.refid )
        root_object = breathe.doxparsers.compound.parse( ref_xml_path )

        nodelist.extend(root_object.rst_nodes())

        return nodelist

supermod.CompoundType.subclass = CompoundTypeSub
# end class CompoundTypeSub


class MemberTypeSub(supermod.MemberType):

    def __init__(self, kind=None, refid=None, name=''):
        supermod.MemberType.__init__(self, kind, refid, name)

supermod.MemberType.subclass = MemberTypeSub
# end class MemberTypeSub


def parse(inFilename):

    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.DoxygenType.factory()
    rootObj.build(rootNode)

    return rootObj

