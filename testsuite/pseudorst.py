#!/usr/bin/env python


import sys

sys.path.insert(0, "../")
sys.path.insert(0, "source")

from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.domains.cpp import DefinitionParser
#from breathe.finder import FinderFactory, NoMatchesError, MultipleMatchesError
#from breathe.parser import DoxygenParserFactory, ParserError, CacheFactory, DoxygenIndexParser
#from breathe.renderer.rst.doxygen import DoxygenToRstRendererFactoryCreator
#from breathe.finder.doxygen import DoxygenItemFinderFactoryCreator, ItemMatcherFactory

from breathe.finder import FinderFactory, NoMatchesError, MultipleMatchesError
from breathe.parser import DoxygenParserFactory, CacheFactory, ParserError, DoxygenIndexParser
from breathe.renderer.rst.doxygen import DoxygenToRstRendererFactoryCreatorConstructor, RstContentCreator
from breathe.renderer.rst.doxygen.domain import DomainHandlerFactoryCreator, NullDomainHandler
from breathe.renderer.rst.doxygen.domain import CppDomainHelper, CDomainHelper
from breathe.renderer.rst.doxygen.filter import FilterFactory, GlobFactory
from breathe.renderer.rst.doxygen.target import TargetHandlerFactory
from breathe.finder.doxygen import DoxygenItemFinderFactoryCreator, ItemMatcherFactory

from breathe import NodeFactory, ProjectInfoFactory, DoxygenDirectiveFactory, PathHandler, RootDataObject

import docutils.nodes
import sphinx.addnodes
import textwrap
import fnmatch
import os
import re

# Sphinx source/conf.py file
import conf


cache_factory = CacheFactory()
cache = cache_factory.create_cache()
path_handler = PathHandler(os.sep, os.path.basename, os.path.join)
parser_factory = DoxygenParserFactory(cache, path_handler)
matcher_factory = ItemMatcherFactory()
item_finder_factory_creator = DoxygenItemFinderFactoryCreator(parser_factory, matcher_factory)
index_parser = DoxygenIndexParser(cache, path_handler)
finder_factory = FinderFactory(index_parser, item_finder_factory_creator)

node_factory = NodeFactory(docutils.nodes, sphinx.addnodes)

cpp_domain_helper = CppDomainHelper(DefinitionParser, re.sub)
c_domain_helper = CDomainHelper()
domain_helpers = {"c": c_domain_helper, "cpp": cpp_domain_helper}
domain_handler_factory_creator = DomainHandlerFactoryCreator(node_factory, domain_helpers)

rst_content_creator = RstContentCreator(ViewList, textwrap.dedent)
default_domain_handler = NullDomainHandler()

renderer_factory_creator_constructor = DoxygenToRstRendererFactoryCreatorConstructor(
        node_factory,
        parser_factory,
        default_domain_handler,
        domain_handler_factory_creator,
        rst_content_creator
        )

project_info_factory = ProjectInfoFactory(fnmatch.fnmatch)
project_info_factory.update(
        conf.breathe_projects,
        conf.breathe_default_project,
        conf.breathe_domain_by_extension,
        conf.breathe_domain_by_file_pattern
        )

glob_factory = GlobFactory(fnmatch.fnmatch)
filter_factory = FilterFactory(glob_factory, path_handler)
target_handler_factory = TargetHandlerFactory(node_factory)

root_data_object = RootDataObject()

directive_factory = DoxygenDirectiveFactory(
        root_data_object,
        renderer_factory_creator_constructor,
        finder_factory,
        matcher_factory,
        project_info_factory,
        filter_factory,
        target_handler_factory
        )

from docutils.core import publish_cmdline, default_description

from docutils.parsers.rst import directives
directives.register_directive("doxygenindex", directive_factory.create_index_directive_container())

description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish_cmdline(description=description)

