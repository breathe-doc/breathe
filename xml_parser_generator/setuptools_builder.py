# -*- coding: utf-8 -*-

import os.path

# try:
#     from setuptools.command.build import build
# except ImportError:
#     from distutils.command.build import build

# from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

try:
    from setuptools.modified import newer_group
except ImportError:
    from distutils.dep_util import newer_group

from distutils import log
from distutils.dir_util import mkpath

# from distutils.util import split_quoted


import make_parser


# extra_user_options = [
#     ("cpp-opts=", None, "extra command line arguments for the compiler"),
#     ("ld-opts=", None, "extra command line arguments for the linker"),
# ]


# class CustomBuild(build):
#     """Add extra parameters for 'build' to pass to 'build_ext'"""
#
#     user_options = build.user_options + extra_user_options
#
#     def initialize_options(self):
#         super().initialize_options()
#         self.cpp_opts = ""
#         self.ld_opts = ""
#
#     def finalize_options(self):
#         super().finalize_options()
#         self.cpp_opts = split_quoted(self.cpp_opts)
#         self.ld_opts = split_quoted(self.ld_opts)


# class CustomBuildExt(build_ext):
#     """Extend build_ext to automatically generate the parser module"""
#
#     user_options = build_ext.user_options + extra_user_options
#
#     SCHEMA_FILE = os.path.join("xml_parser_generator", "schema.json")
#     MODULE_TEMPLATE = os.path.join("xml_parser_generator", "module_template.c.in")
#     PY_MODULE_TEMPLATE = os.path.join("xml_parser_generator", "module_template.py.in")
#     STUBS_TEMPLATE = os.path.join("xml_parser_generator", "stubs_template.pyi.in")
#     MAKER_SOURCE = os.path.join("xml_parser_generator", "make_parser.py")
#
#     M_DEPENDENCIES = [SCHEMA_FILE, MODULE_TEMPLATE, MAKER_SOURCE]
#     PY_M_DEPENDENCIES = [SCHEMA_FILE, PY_MODULE_TEMPLATE, MAKER_SOURCE]
#     S_DEPENDENCIES = [SCHEMA_FILE, STUBS_TEMPLATE, MAKER_SOURCE]
#
#     def initialize_options(self):
#         super().initialize_options()
#         self.cpp_opts = None
#         self.ld_opts = None
#
#     def finalize_options(self):
#         if self.cpp_opts is not None:
#             self.cpp_opts = split_quoted(self.cpp_opts)
#         if self.ld_opts is not None:
#             self.ld_opts = split_quoted(self.ld_opts)
#
#         self.set_undefined_options("build", ("cpp_opts", "cpp_opts"), ("ld_opts", "ld_opts"))
#         super().finalize_options()
#
#     def build_extensions(self):
#         assert len(self.extensions) == 1
#
#         if not self.debug:
#             # The parser doesn't do any complicated calculation; its speed will
#             # mostly depend on file read and memory allocation speed. Thus it's
#             # better to optimize for size.
#             c = self.compiler.compiler_type
#             if c == "msvc":
#                 self.extensions[0].extra_compile_args = ["/O1"]
#             elif c in {"unix", "cygwin", "mingw32"}:
#                 self.extensions[0].extra_compile_args = ["-Os"]
#                 self.extensions[0].extra_link_args = ["-s"]
#
#         source = os.path.join(self.build_temp, self.extensions[0].name + ".c")
#
#         # put the stub and Python file in the same place that the extension
#         # module will be
#         ext_dest = self.get_ext_fullpath(self.extensions[0].name)
#         libdir = os.path.dirname(ext_dest)
#         stub = os.path.join(libdir, self.extensions[0].name + ".pyi")
#         py_source = os.path.join(libdir, self.extensions[0].name + "_py.py")
#
#         mkpath(self.build_temp, dry_run=self.dry_run)
#         mkpath(libdir, dry_run=self.dry_run)
#
#         regen = []
#         for dep, out, tmpl in (
#             (self.M_DEPENDENCIES, source, self.MODULE_TEMPLATE),
#             (self.PY_M_DEPENDENCIES, py_source, self.PY_MODULE_TEMPLATE),
#             (self.S_DEPENDENCIES, stub, self.STUBS_TEMPLATE),
#         ):
#             if self.force or newer_group(dep, out):
#                 regen.append((tmpl, out))
#
#         if regen:
#             log.info("generating module source from templates")
#             if not self.dry_run:
#                 make_parser.generate_from_json(self.SCHEMA_FILE, regen)
#         else:
#             log.debug(f'"{source}", "{py_source}" and "{stub}" are up-to-date')
#
#         self.extensions[0].sources.append(source)
#
#         super().build_extensions()


class CustomBuildPy(build_py):
    SCHEMA_FILE = os.path.join("xml_parser_generator", "schema.json")
    PY_MODULE_TEMPLATE = os.path.join("xml_parser_generator", "module_template.py.in")
    MAKER_SOURCE = os.path.join("xml_parser_generator", "make_parser.py")
    PARSER_DEST = os.path.join("breathe", "_parser.py")

    PY_M_DEPENDENCIES = [SCHEMA_FILE, PY_MODULE_TEMPLATE, MAKER_SOURCE]

    def make_parser(self):
        dest = self.PARSER_DEST
        if not self.editable_mode:
            dest = os.path.join(self.build_lib, dest)
            mkpath(os.path.dirname(dest), dry_run=self.dry_run)

        if self.force or newer_group(self.PY_M_DEPENDENCIES, dest):
            log.info(f'generating "{dest}" source from template')
            if not self.dry_run:
                make_parser.generate_from_json(self.SCHEMA_FILE, [(self.PY_MODULE_TEMPLATE, dest)])
        else:
            log.debug(f'"{dest}" is up-to-date')

    def run(self):
        super().run()
        self.make_parser()


if __name__ == "__main__":
    make_parser.generate_from_json(
        CustomBuildPy.SCHEMA_FILE, [(CustomBuildPy.PY_MODULE_TEMPLATE, CustomBuildPy.PARSER_DEST)]
    )
