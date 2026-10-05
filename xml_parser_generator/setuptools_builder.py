from __future__ import annotations

import os.path
from pathlib import Path

from setuptools.command.build_py import build_py  # type: ignore[import-untyped]

try:
    from setuptools.modified import newer_group  # type: ignore[import-untyped]
except ImportError:
    from distutils.dep_util import newer_group

from distutils import log
from distutils.dir_util import mkpath

try:
    from xml_parser_generator import make_parser
except ImportError:  # executed as a script: python xml_parser_generator/setuptools_builder.py
    import make_parser  # type: ignore[no-redef, import-not-found]


class CustomBuildPy(build_py):
    SCHEMA_FILE = os.path.join("xml_parser_generator", "schema.json")
    PY_MODULE_TEMPLATE = os.path.join("xml_parser_generator", "module_template.py.in")
    MAKER_SOURCE = os.path.join("xml_parser_generator", "make_parser.py")
    PARSER_DEST = os.path.join("breathe", "_parser.py")

    PY_M_DEPENDENCIES = [SCHEMA_FILE, PY_MODULE_TEMPLATE, MAKER_SOURCE]

    def make_parser(self):
        src_root = Path.cwd()
        if self.editable_mode:
            # In editable mode, setuptools expects generated files to live in
            # the project directory, not in the temporary build directory.
            src_root = Path(__file__).resolve().parent.parent
            dest = src_root / self.PARSER_DEST
            dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            dest = Path(self.build_lib) / self.PARSER_DEST
            mkpath(os.path.dirname(dest), dry_run=self.dry_run)

        dependencies = [src_root / dep for dep in self.PY_M_DEPENDENCIES]
        if self.force or newer_group([str(d) for d in dependencies], str(dest)):
            log.info(f'generating "{dest}" source from template')
            if not self.dry_run:
                make_parser.generate_from_json(
                    str(src_root / self.SCHEMA_FILE),
                    [(str(src_root / self.PY_MODULE_TEMPLATE), str(dest))],
                )
        else:
            log.debug(f'"{dest}" is up-to-date')

    def run(self):
        super().run()
        self.make_parser()


if __name__ == "__main__":
    make_parser.generate_from_json(
        CustomBuildPy.SCHEMA_FILE, [(CustomBuildPy.PY_MODULE_TEMPLATE, CustomBuildPy.PARSER_DEST)]
    )
