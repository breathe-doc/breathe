"""For any test that is missing the "compare.xml" file, run the test, strip the
output of certain attributes and save the results as "compare_draft.xml" in the
folder where "compare.xml" belongs.

The resulting file will need to be inspected manually to make sure it is
actually correct. Then it can be saved as "compare.xml".

The output file omits a number of attributes from the docutils XML format that
are either unimportant for ensuring correctness of Breathe or has a value that
depends on an unimportant factor, such as the exact version of Sphinx, or the
directories of input files.
"""

import os
import pathlib
import subprocess
import shutil
import docutils.nodes
import docutils.writers.docutils_xml
import tempfile
from sphinx.testing.util import SphinxTestApp


TEST_DATA_DIR = pathlib.Path(__file__).parent.parent / "tests" / "data"

C_FILE_SUFFIXES = frozenset(('.h', '.c', '.hpp', '.cpp'))
IGNORED_ELEMENTS = frozenset(())
IGNORED_ATTRIBUTES = frozenset((
    'ids',
    'names',
    'no-contents-entry',
    'no-index',
    'no-index-entry',
    'no-typesetting',
    'nocontentsentry',
    'noindex',
    'noindexentry',
    'is_multiline',
    'multi_line_parameter_list',
    'add_permalink',
    'xml:space',
    'source',
    'translation_progress',
    'options',
    'original_uri',
    '_toc_name',
    '_toc_parts',
    'xmlns:c',
    'xmlns:changeset',
    'xmlns:citation',
    'xmlns:cpp',
    'xmlns:index',
    'xmlns:js',
    'xmlns:math',
    'xmlns:py',
    'xmlns:rst',
    'xmlns:std'
))

DEFAULT_CONF = {
    'project': 'test',
    'breathe_default_project': 'example',
    'breathe_show_include': False,
    'extensions': ['breathe','sphinx.ext.graphviz']}

def attlist(self):
    return sorted(item for item in self.non_default_attributes().items() if item[0] not in IGNORED_ATTRIBUTES)
docutils.nodes.Element.attlist = attlist

class Translator(docutils.writers.docutils_xml.XMLTranslator):
    doctype = ''

    def __init__(self, document):
        super().__init__(document)
        self.ignore = 0

    def default_visit(self, node):
        if self.ignore or node.tagname in IGNORED_ELEMENTS:
            self.ignore += 1
        else:
            super().default_visit(node)

    def default_departure(self, node):
        if self.ignore:
            self.ignore -= 1
        else:
            super().default_departure(node)

    def visit_Text(self, node):
        if not self.ignore:
            super().visit_Text(node)

    def depart_Text(self, node):
        if not self.ignore:
            super().depart_Text(node)

class DirChange:
    def __init__(self, path):
        self.path = path
        self._old_path = os.getcwd()
    
    def __enter__(self):
        os.chdir(self.path)
    
    def __exit__(self, etype, evalue, etb):
        os.chdir(self._old_path)

class TmpDir:
    """A wrapper for tempfile.TemporaryDirectory that returns an instance of
    pathlib.Path in its __enter__ method"""

    def __init__(self, *args, **kwds):
        self.base = tempfile.TemporaryDirectory(*args, **kwds)
    
    def __enter__(self):
        return pathlib.Path(self.base.__enter__())
    
    def __exit__(self, *args):
        self.base.__exit__(*args)

def get_individual_tests():
    return (TEST_DATA_DIR / 'examples').glob("test_*")

def filter_c_files(input_dir):
    for p in input_dir.iterdir():
        if p.suffix in C_FILE_SUFFIXES:
            full = str(p)
            if '"' in full:
                raise ValueError('quotations marks not allowed in path names')
            yield f'"{full}"'

def conf_overrides(extra):
    conf = DEFAULT_CONF.copy()
    conf.update(extra)
    return conf

class Doxygen:
    def __init__(self):
        exe = shutil.which('doxygen')
        if exe is None:
            raise ValueError('cannot find doxygen executable')
        self.exe = exe
        
        self.template = (TEST_DATA_DIR / "examples" / "doxyfile_template").read_text()

    def run_one(self, tmp_path, outname):
        doxyfile = tmp_path / "Doxyfile"
        doxycontent = self.template.format(
            output=tmp_path
        )
        extra_opts = pathlib.Path('extra_dox_opts.txt')
        if extra_opts.exists():
            doxycontent += extra_opts.read_text()
        doxyfile.write_text(doxycontent)

        subprocess.run([self.exe, doxyfile], check = True)
        if outname != 'xml':
            os.rename(tmp_path / 'xml', tmp_path / outname)

def run_sphinx_and_copy_output(tmp_path, input_path, overrides):
    dest = tmp_path / "conf.py"
    ec = pathlib.Path("extra_conf.py")
    if ec.exists():
        shutil.copyfile(ec, dest)
    else:
        dest.touch()

    app = SphinxTestApp(
        buildername='xml',
        srcdir=tmp_path,
        confoverrides=conf_overrides(overrides))
    app.set_translator('xml', Translator, True)
    app.build()
    app.cleanup()

    shutil.copyfile(tmp_path / '_build' / 'xml' / 'index.xml', input_path / 'compare_draft.xml')

def gen_example(dox, test_input):
    if (test_input / 'compare.xml').exists():
        return

    with DirChange(test_input), TmpDir() as tmp_path:
        dox.run_one(tmp_path, 'xml')
        shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")
        run_sphinx_and_copy_output(tmp_path, test_input, {
            'breathe_projects': {'example': str(tmp_path / "xml")}})

def gen_auto():
    test_input = TEST_DATA_DIR / 'auto'
    if (test_input / 'compare.xml').exists():
        return

    with DirChange(test_input), TmpDir() as tmp_path:
        shutil.copyfile(test_input / "input.rst", tmp_path / "index.rst")
        run_sphinx_and_copy_output(tmp_path, test_input, {
            'breathe_projects_source': {'example': (test_input.absolute(), ['auto_class.h', 'auto_function.h'])}})

def gen_multi_project(dox):
    test_input = TEST_DATA_DIR / 'multi_project'

    if (test_input / 'compare.xml').exists():
        return

    with TmpDir() as tmp_path:
        for c in "ABC":
            with DirChange(test_input / c):
                dox.run_one(tmp_path, f'xml{c}')

        (tmp_path / "conf.py").touch()
        (tmp_path / "index.rst").write_text((test_input / "input.rst").read_text().format(project_c_path=str(tmp_path / "xmlC")))

        run_sphinx_and_copy_output(tmp_path, test_input, {
            "breathe_projects": {"A": str(tmp_path / "xmlA"), "B": str(tmp_path / "xmlB")}})


def main():
    dox = Doxygen()
    for t in get_individual_tests():
        gen_example(dox, t)
    gen_auto()
    gen_multi_project(dox)

if __name__ == "__main__":
    main()
