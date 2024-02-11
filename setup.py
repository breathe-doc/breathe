# -*- coding: utf-8 -*-
import sys
import os.path
from setuptools import setup


# add xml_parser_generator to the import path list
base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(base_dir, "xml_parser_generator"))

from setuptools_builder import CustomBuildPy


long_desc = """
Breathe is an extension to reStructuredText and Sphinx to be able to read and
 render `Doxygen <http://www.doxygen.org>`__ xml output.
"""

setup(
    long_description=long_desc,
    cmdclass={"build_py": CustomBuildPy},
)
