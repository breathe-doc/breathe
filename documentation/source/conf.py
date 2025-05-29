from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import sphinx

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# General configuration
# ---------------------

extensions = [
    "breathe",
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
    "sphinxcontrib.spelling",
]

master_doc = "index"
project = "Breathe"
copyright = "2009-2025, Michael Jones"

if os.getenv("BREATHE_COMPARE") == "True":
    # If we're doing a comparison then set the version & release to 'compare'
    # so that they are always the same otherwise they can come up as changes
    # when we really don't care if they are different.
    version = release = "compare"
else:
    # Get a description of the current position.
    git_tag = subprocess.run(["git", "describe", "--tags"], capture_output=True, encoding="utf-8")
    if re.match(r"^v\d+\.\d+\.\d+$", git_tag.stdout):
        # Check if it matches a pure tag number vX.Y.Z,
        # rather than vX.Y.Z-91-g8676988, which is how non-tagged commits
        # are described (relative to the last tag).
        version = release = git_tag.stdout
    else:
        version = release = "latest"


# Options for breathe extension
# -----------------------------

breathe_projects = {
    "class": "../../examples/doxygen/class/xml/",
    "classtest": "../../examples/specific/class/xml/",
    "struct": "../../examples/specific/struct/xml/",
    "interface": "../../examples/specific/interface/xml/",
    "decl_impl": "../../examples/specific/decl_impl/xml/",
    "structcmd": "../../examples/doxygen/structcmd/xml/",
    "tinyxml": "../../examples/tinyxml/tinyxml/xml/",
    "restypedef": "../../examples/doxygen/restypedef/xml/",
    "nutshell": "../../examples/specific/nutshell/xml/",
    "rst": "../../examples/specific/rst/xml/",
    "c_file": "../../examples/specific/c_file/xml/",
    "namespace": "../../examples/specific/namespacefile/xml/",
    "userdefined": "../../examples/specific/userdefined/xml/",
    "template_function": "../../examples/specific/template_function/xml/",
    "template_class": "../../examples/specific/template_class/xml/",
    "template_class_non_type": "../../examples/specific/template_class_non_type/xml/",
    "template_specialisation": "../../examples/specific/template_specialisation/xml/",
    "latexmath": "../../examples/specific/latexmath/xml/",
    "functionOverload": "../../examples/specific/functionOverload/xml/",
    "programlisting": "../../examples/specific/programlisting/xml/",
    "image": "../../examples/specific/image/xml/",
    "lists": "../../examples/specific/lists/xml/",
    "tables": "../../examples/specific/tables/xml/",
    "group": "../../examples/specific/group/xml/",
    "union": "../../examples/specific/union/xml/",
    "qtsignalsandslots": "../../examples/specific/qtsignalsandslots/xml/",
    "array": "../../examples/specific/array/xml/",
    "c_struct": "../../examples/specific/c_struct/xml/",
    "c_enum": "../../examples/specific/c_enum/xml/",
    "c_typedef": "../../examples/specific/c_typedef/xml/",
    "c_macro": "../../examples/specific/c_macro/xml/",
    "c_union": "../../examples/specific/c_union/xml/",
    "define": "../../examples/specific/define/xml/",
    "multifile": "../../examples/specific/multifilexml/xml/",
    "cpp_anon": "../../examples/specific/cpp_anon/xml/",
    "cpp_concept": "../../examples/specific/cpp_concept/xml/",
    "cpp_enum": "../../examples/specific/cpp_enum/xml/",
    "cpp_union": "../../examples/specific/cpp_union/xml/",
    "cpp_function": "../../examples/specific/cpp_function/xml/",
    "cpp_function_lookup": "../../examples/specific/cpp_function_lookup/xml/",
    "cpp_friendclass": "../../examples/specific/cpp_friendclass/xml/",
    "cpp_inherited_members": "../../examples/specific/cpp_inherited_members/xml/",
    "cpp_ns_template_specialization": "../../examples/specific/cpp_ns_template_specialization/xml/",
    "cpp_trailing_return_type": "../../examples/specific/cpp_trailing_return_type/xml/",
    "cpp_constexpr_hax": "../../examples/specific/cpp_constexpr_hax/xml/",
    "xrefsect": "../../examples/specific/xrefsect/xml/",
    "membergroups": "../../examples/specific/membergroups/xml/",
    "simplesect": "../../examples/specific/simplesect/xml/",
    "dot_graphs": "../../examples/specific/dot_graphs/xml/",
}

breathe_projects_source = {
    "auto": ("../../examples/specific", ["auto_function.h", "auto_class.h"]),
}

breathe_default_project = "tinyxml"

breathe_domain_by_extension = {
    "h": "cpp",
    "py": "py",
}

breathe_domain_by_file_pattern = {
    "class.h": "cpp",
    "alias.h": "c",
    "array.h": "c",
    "c_*.h": "c",
}

breathe_use_project_refids = True


# Options for HTML output
# -----------------------

html_theme = "furo"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"
html_static_path = ["_static"]
html_css_files = ["breathe.css"]


# Options for the spelling extension
# ----------------------------------
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_lang = "en_US"


# Extension interface
# -------------------

try:
    doxygen_test = subprocess.check_output(["doxygen", "--version"], encoding="utf-8")
except subprocess.CalledProcessError as err:
    msg = f"doxygen --version reported an error: {err.stderr}"
    raise RuntimeError(msg) from err
else:
    print(f"Using Doxygen v{doxygen_test}")
    del doxygen_test


if os.getenv("READTHEDOCS") == "True":
    if version == "latest":
        tags.add("documentation_build_readthedocs_latest")  # NoQA: F821
    else:
        tags.add("documentation_build_readthedocs")  # NoQA: F821
else:
    tags.add("documentation_build_development")  # NoQA: F821


def run_doxygen(folder: Path) -> None:
    """Run the doxygen make command in the designated folder"""
    try:
        subprocess.run(["make", "DOXYGEN=doxygen"], check=True, cwd=folder)
    except subprocess.CalledProcessError as e:
        print(f"doxygen terminated by signal {-e.returncode}", file=sys.stderr)
    except OSError as e:
        print(f"doxygen execution failed: {e}", file=sys.stderr)


def generate_doxygen_xml(app: Sphinx) -> None:
    """Run the doxygen make commands if we're on the ReadTheDocs server"""
    if os.getenv("READTHEDOCS") == "True":
        # Attempt to build the doxygen files on the RTD server.
        # Explicitly override the path/name used for executing doxygen
        # to simply be 'doxygen' to stop the makefiles looking for the executable.
        # This is because the `which doxygen` effort seemed to fail
        # when tested on the RTD server.
        run_doxygen(PROJECT_ROOT / "examples" / "doxygen")
        run_doxygen(PROJECT_ROOT / "examples" / "specific")
        run_doxygen(PROJECT_ROOT / "examples" / "tinyxml")


def setup(app) -> ExtensionMetadata:
    if sphinx.version_info[:2] < (7, 4):
        # Approach borrowed from the Sphinx docs
        app.add_object_type(
            "confval",
            "confval",
            objname="configuration value",
            indextemplate="pair: %s; configuration value",
        )

    # Add hook for building doxygen xml when needed
    app.connect("builder-inited", generate_doxygen_xml)

    return {
        "version": version,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
