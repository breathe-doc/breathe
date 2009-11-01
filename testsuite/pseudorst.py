#!/usr/bin/env python2.5

import sys

sys.path.insert(0, "../")
sys.path.insert(0, "source")

import breathe
import docutils

# Sphinx source/conf.py file
import conf

breathe.DoxygenBase.projects = conf.breathe_projects
breathe.DoxygenBase.default_project = conf.breathe_default_project

from docutils.core import publish_cmdline, default_description

from docutils.parsers.rst import directives
directives.register_directive("doxygenindex", breathe.DoxygenIndexDirective)

description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish_cmdline(description=description)
