"""Run Doxygen on all test samples and save the results."""

import os
import pathlib
import shutil
import subprocess

from breathe.process import AUTOCFG_TEMPLATE


PROJECT_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "tests" / "data"
EXAMPLES_DIR = DATA_DIR / "examples"
CACHE_DIR = EXAMPLES_DIR / "_cache"


def make_cache():
    template = (EXAMPLES_DIR / "doxyfile_template").read_text()

    exc = shutil.which("doxygen")
    if exc is None:
        raise ValueError("cannot find doxygen executable")
    
    CACHE_DIR.mkdir(exist_ok=True)
    prev_dir = os.getcwd()

    r = subprocess.run(
        [exc, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    (CACHE_DIR / "version.txt").write_text(r.stdout)

    try:
        for p in EXAMPLES_DIR.glob("test_*"):
            print(f"generating output for {p.name}")
            os.chdir(p)
            out_dir = CACHE_DIR / p.name
            out_dir.mkdir(exist_ok=True)
            doxyfile = out_dir / "Doxyfile"
            doxycontent = template.format(output=out_dir)
            extra_opts = pathlib.Path("extra_dox_opts.txt")
            if extra_opts.exists():
                doxycontent += extra_opts.read_text()
            doxyfile.write_text(doxycontent)

            subprocess.run([exc, doxyfile], check=True)
        
        print(f"generating output for auto")
        os.chdir(DATA_DIR / "auto")
        out_dir = CACHE_DIR / "auto"
        out_dir.mkdir(exist_ok=True)

        doxyfile = out_dir / "Doxyfile"
        doxyfile.write_text(AUTOCFG_TEMPLATE.format(
            project_name="example",
            output_dir=str(out_dir),
            input='"auto_class.h" "auto_function.h"',
            extra=""
        ))

        subprocess.run([exc, doxyfile], check=True)
    finally:
        os.chdir(prev_dir)


if __name__ == "__main__":
    make_cache()