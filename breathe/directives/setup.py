from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from breathe.directives.class_like import (
    DoxygenClassDirective,
    DoxygenInterfaceDirective,
    DoxygenStructDirective,
)
from breathe.directives.content_block import (
    DoxygenGroupDirective,
    DoxygenNamespaceDirective,
    DoxygenPageDirective,
)
from breathe.directives.file import AutoDoxygenFileDirective, DoxygenFileDirective
from breathe.directives.function import DoxygenFunctionDirective
from breathe.directives.index import AutoDoxygenIndexDirective, DoxygenIndexDirective
from breathe.directives.item import (
    DoxygenConceptDirective,
    DoxygenDefineDirective,
    DoxygenEnumDirective,
    DoxygenEnumValueDirective,
    DoxygenTypedefDirective,
    DoxygenUnionDirective,
    DoxygenVariableDirective,
)
from breathe.parser import DoxygenParserFactory
from breathe.process import AutoDoxygenProcessHandle
from breathe.project import ProjectInfoFactory

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: Sphinx) -> None:
    directives = {
        "doxygenindex": DoxygenIndexDirective,
        "autodoxygenindex": AutoDoxygenIndexDirective,
        "doxygenfunction": DoxygenFunctionDirective,
        "doxygenstruct": DoxygenStructDirective,
        "doxygenclass": DoxygenClassDirective,
        "doxygeninterface": DoxygenInterfaceDirective,
        "doxygenvariable": DoxygenVariableDirective,
        "doxygendefine": DoxygenDefineDirective,
        "doxygenconcept": DoxygenConceptDirective,
        "doxygenenum": DoxygenEnumDirective,
        "doxygenenumvalue": DoxygenEnumValueDirective,
        "doxygentypedef": DoxygenTypedefDirective,
        "doxygenunion": DoxygenUnionDirective,
        "doxygennamespace": DoxygenNamespaceDirective,
        "doxygengroup": DoxygenGroupDirective,
        "doxygenfile": DoxygenFileDirective,
        "autodoxygenfile": AutoDoxygenFileDirective,
        "doxygenpage": DoxygenPageDirective,
    }

    # The directives need these global objects, so in order to smuggle
    # them in, we use env.temp_data. But it is cleared after each document
    # has been read, we use the source-read event to set them.
    # note: the parser factory contains a cache of the parsed XML
    # note: the project_info_factory also contains some caching stuff
    # TODO: is that actually safe for when reading in parallel?
    project_info_factory = ProjectInfoFactory(app)
    parser_factory = DoxygenParserFactory(app)

    def set_temp_data(
        app: Sphinx, project_info_factory=project_info_factory, parser_factory=parser_factory
    ):
        assert app.env is not None
        app.env.temp_data["breathe_project_info_factory"] = project_info_factory
        app.env.temp_data["breathe_parser_factory"] = parser_factory

    app.connect("source-read", lambda app, docname, source: set_temp_data(app))

    for name, directive in directives.items():
        app.add_directive(name, directive)

    app.add_config_value("breathe_projects", {}, "env")  # Dict[str, str]
    app.add_config_value("breathe_default_project", "", "env")  # str
    # Provide reasonable defaults for domain_by_extension mapping. Can be overridden by users.
    app.add_config_value(
        "breathe_domain_by_extension", {"py": "py", "cs": "cs"}, "env"
    )  # Dict[str, str]
    app.add_config_value("breathe_domain_by_file_pattern", {}, "env")  # Dict[str, str]
    app.add_config_value("breathe_projects_source", {}, "env")
    app.add_config_value("breathe_build_directory", "", "env")
    app.add_config_value("breathe_default_members", (), "env")
    app.add_config_value("breathe_show_define_initializer", False, "env")
    app.add_config_value("breathe_show_enumvalue_initializer", False, "env")
    app.add_config_value("breathe_show_include", True, "env")
    app.add_config_value("breathe_implementation_filename_extensions", [".c", ".cc", ".cpp"], "env")
    app.add_config_value("breathe_doxygen_config_options", {}, "env")
    app.add_config_value("breathe_doxygen_aliases", {}, "env")
    app.add_config_value("breathe_use_project_refids", False, "env")
    app.add_config_value("breathe_order_parameters_first", False, "env")
    app.add_config_value("breathe_separate_member_pages", False, "env")

    breathe_css = "breathe.css"
    if Path(app.confdir, "_static", breathe_css).exists():
        app.add_css_file(breathe_css)

    def write_file(directory, filename, content):
        # Ensure that the directory exists
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

        # Write the file with the provided contents
        (directory / filename).write_text(content)

    doxygen_handle = AutoDoxygenProcessHandle(
        subprocess.check_call, write_file, project_info_factory
    )

    def doxygen_hook(app: Sphinx):
        doxygen_handle.generate_xml(
            app.config.breathe_projects_source,
            app.config.breathe_doxygen_config_options,
            app.config.breathe_doxygen_aliases,
        )

    app.connect("builder-inited", doxygen_hook)
