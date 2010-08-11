#!/usr/bin/env python


import sys

sys.path.insert(0, "../")
sys.path.insert(0, "source")

from docutils.parsers import rst
from breathe.builder import RstBuilder, BuilderFactory
from breathe.finder import FinderFactory, NoMatchesError, MultipleMatchesError
from breathe.parser import DoxygenParserFactory, DoxygenIndexParser
from breathe.renderer.rst.doxygen import DoxygenToRstRendererFactoryCreator
from breathe.finder.doxygen import DoxygenItemFinderFactoryCreator, ItemMatcherFactory

from breathe import NodeFactory, ProjectInfoFactory, DoxygenDirectiveFactory

import docutils.nodes
import sphinx.addnodes


# Sphinx source/conf.py file
import conf

parser_factory = DoxygenParserFactory()
matcher_factory = ItemMatcherFactory()
item_finder_factory_creator = DoxygenItemFinderFactoryCreator(parser_factory, matcher_factory)
index_parser = DoxygenIndexParser()
finder_factory = FinderFactory(index_parser, item_finder_factory_creator)

node_factory = NodeFactory(docutils.nodes, sphinx.addnodes)
renderer_factory_creator = DoxygenToRstRendererFactoryCreator(node_factory, parser_factory)
builder_factory = BuilderFactory(RstBuilder, renderer_factory_creator)

project_info_factory = ProjectInfoFactory()
project_info_factory.update(conf.breathe_projects, conf.breathe_default_project)

directive_factory = DoxygenDirectiveFactory(builder_factory, finder_factory, matcher_factory, project_info_factory)

from docutils.core import publish_cmdline, default_description

from docutils.parsers.rst import directives
directives.register_directive("doxygenindex", directive_factory.create_index_directive_container())

description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish_cmdline(description=description)

