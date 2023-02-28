# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

import sys

# Keep in sync with breathe/__init__.py __version__
__version__ = "4.35.0"

long_desc = """
Breathe is an extension to reStructuredText and Sphinx to be able to read and
 render `Doxygen <http://www.doxygen.org>`__ xml output.
"""

requires = ["Sphinx>=4.0,!=5.0.0", "docutils>=0.12"]

if sys.version_info < (3, 7):
    print("ERROR: Sphinx requires at least Python 3.7 to run.")
    sys.exit(1)


setup(
    name="breathe",
    version=__version__,
    url="https://github.com/michaeljones/breathe",
    download_url="https://github.com/michaeljones/breathe",
    license="BSD",
    author="Michael Jones",
    author_email="m.pricejones@gmail.com",
    description="Sphinx Doxygen renderer",
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    platforms="any",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "breathe-apidoc = breathe.apidoc:main",
        ],
    },
    install_requires=requires,
)
