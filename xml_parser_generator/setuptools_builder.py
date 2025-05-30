from __future__ import annotations

import os.path

from setuptools.command.build_py import build_py

try:
    from setuptools.modified import newer_group
except ImportError:
    from distutils.dep_util import newer_group

from distutils import log
from distutils.dir_util import mkpath

import make_parser


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
