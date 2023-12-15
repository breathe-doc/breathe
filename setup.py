# -*- coding: utf-8 -*-
import sys
import os.path
from setuptools import setup, find_packages, Extension
from setuptools.command.build import build
from setuptools.command.build_ext import build_ext
try:
    from setuptools.dep_util import newer_group
except ImportError:
    from distutils.dep_util import newer_group
from distutils import log
from distutils.dir_util import mkpath
from distutils.util import split_quoted

# add xml_parser_generator to the import path list
base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(base_dir, "xml_parser_generator"))

import make_parser

# Keep in sync with breathe/__init__.py __version__
__version__ = "4.35.0"

long_desc = """
Breathe is an extension to reStructuredText and Sphinx to be able to read and
 render `Doxygen <http://www.doxygen.org>`__ xml output.
"""

requires = ["Sphinx>=4.0,!=5.0.0", "docutils>=0.12"]

if sys.version_info < (3, 8):
    print("ERROR: Breathe requires at least Python 3.8 to run.")
    sys.exit(1)


extra_user_options = [
    ("cpp-opts=", None, "extra command line arguments for the compiler"),
    ("ld-opts=", None, "extra command line arguments for the linker"),
]


class CustomBuild(build):
    """Add extra parameters for 'build' to pass to 'build_ext'"""

    user_options = build.user_options + extra_user_options

    def initialize_options(self):
        super().initialize_options()
        self.cpp_opts = ""
        self.ld_opts = ""

    def finalize_options(self):
        super().finalize_options()
        self.cpp_opts = split_quoted(self.cpp_opts)
        self.ld_opts = split_quoted(self.ld_opts)


class CustomBuildExt(build_ext):
    """Extend build_ext to automatically generate _parser.c"""

    user_options = build_ext.user_options + extra_user_options

    SCHEMA_FILE = os.path.join("xml_parser_generator", "schema.json")
    MODULE_TEMPLATE = os.path.join("xml_parser_generator", "module_template.c.in")
    STUBS_TEMPLATE = os.path.join("xml_parser_generator", "stubs_template.pyi.in")
    MAKER_SOURCE = os.path.join("xml_parser_generator", "make_parser.py")

    DEPENDENCIES = [SCHEMA_FILE, MODULE_TEMPLATE, STUBS_TEMPLATE, MAKER_SOURCE]

    def initialize_options(self):
        super().initialize_options()
        self.cpp_opts = None
        self.ld_opts = None

    def finalize_options(self):
        if self.cpp_opts is not None:
            self.cpp_opts = split_quoted(self.cpp_opts)
        if self.ld_opts is not None:
            self.ld_opts = split_quoted(self.ld_opts)

        self.set_undefined_options("build", ("cpp_opts", "cpp_opts"), ("ld_opts", "ld_opts"))
        super().finalize_options()

    def build_extensions(self):
        assert len(self.extensions) == 1

        if not self.debug:
            # The parser doesn't do any complicated calculation; its speed will
            # mostly depend on file read and memory allocation speed. Thus it's
            # better to optimize for size.
            c = self.compiler.compiler_type
            if c == "msvc":
                self.extensions[0].extra_compile_args = ["/O1"]
            elif c in {"unix", "cygwin", "mingw32"}:
                self.extensions[0].extra_compile_args = ["-Os"]
                self.extensions[0].extra_link_args = ["-s"]

        source = os.path.join(self.build_temp, self.extensions[0].name + ".c")

        # put the stub file in the same place that the extension module will be
        ext_dest = self.get_ext_fullpath(self.extensions[0].name)
        libdir = os.path.dirname(ext_dest)
        stub = os.path.join(libdir, self.extensions[0].name + ".pyi")

        mkpath(self.build_temp, dry_run=self.dry_run)
        mkpath(libdir, dry_run=self.dry_run)

        if (
            self.force
            or newer_group(self.DEPENDENCIES, source)
            or newer_group(self.DEPENDENCIES, stub)
        ):
            log.info(f'generating "{source}" and "{stub}" from templates')
            if not self.dry_run:
                make_parser.generate_from_json(
                    self.SCHEMA_FILE, self.MODULE_TEMPLATE, self.STUBS_TEMPLATE, source, stub
                )
        else:
            log.debug(f'"{source}" and "{stub}" are up-to-date')

        self.extensions[0].sources.append(source)

        super().build_extensions()


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
    ext_package="breathe",
    ext_modules=[
        Extension(
            "_parser",
            [],  # source is generated by CustomBuildExt
            depends=CustomBuildExt.DEPENDENCIES,
            libraries=["expat"],
            define_macros=[
                ("PARSER_PY_LIMITED_API", "0x03080000"),  # set Stable ABI version to 3.8
                ("MODULE_NAME", "_parser"),
                ("FULL_MODULE_STR", '"breathe._parser"'),
            ],
            py_limited_api=True,
        )
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "breathe-apidoc = breathe.apidoc:main",
        ],
    },
    install_requires=requires,
    cmdclass={"build": CustomBuild, "build_ext": CustomBuildExt},
)
