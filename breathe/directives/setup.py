from breathe.directives.class_like import (
    DoxygenStructDirective,
    DoxygenClassDirective,
    DoxygenInterfaceDirective,
)
from breathe.directives.content_block import (
    DoxygenNamespaceDirective,
    DoxygenGroupDirective,
    DoxygenPageDirective,
)
from breathe.directives.file import DoxygenFileDirective, AutoDoxygenFileDirective
from breathe.directives.function import DoxygenFunctionDirective
from breathe.directives.index import DoxygenIndexDirective, AutoDoxygenIndexDirective
from breathe.directives.item import (
    DoxygenVariableDirective,
    DoxygenDefineDirective,
    DoxygenUnionDirective,
    DoxygenConceptDirective,
    DoxygenEnumDirective,
    DoxygenEnumValueDirective,
    DoxygenTypedefDirective,
)
from breathe.parser import DoxygenParserFactory
from breathe.project import ProjectInfoFactory
from breathe.process import AutoDoxygenProcessHandle

from sphinx.application import Sphinx

import os
import subprocess


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

    app.add_config_value("breathe_projects", {}, True)  # Dict[str, str]
    app.add_config_value("breathe_default_project", "", True)  # str
    # Provide reasonable defaults for domain_by_extension mapping. Can be overridden by users.
    app.add_config_value(
        "breathe_domain_by_extension", {"py": "py", "cs": "cs"}, True
    )  # Dict[str, str]
    app.add_config_value("breathe_domain_by_file_pattern", {}, True)  # Dict[str, str]
    app.add_config_value("breathe_projects_source", {}, True)
    app.add_config_value("breathe_build_directory", "", True)
    app.add_config_value("breathe_default_members", (), True)
    app.add_config_value("breathe_show_define_initializer", False, "env")
    app.add_config_value("breathe_show_enumvalue_initializer", False, "env")
    app.add_config_value("breathe_show_include", True, "env")
    app.add_config_value("breathe_implementation_filename_extensions", [".c", ".cc", ".cpp"], True)
    app.add_config_value("breathe_doxygen_config_options", {}, True)
    app.add_config_value("breathe_doxygen_aliases", {}, True)
    app.add_config_value("breathe_use_project_refids", False, "env")
    app.add_config_value("breathe_order_parameters_first", False, "env")
    app.add_config_value("breathe_separate_member_pages", False, "env")

    breathe_css = "breathe.css"
    if os.path.exists(os.path.join(app.confdir, "_static", breathe_css)):
        app.add_css_file(breathe_css)

    def write_file(directory, filename, content):
        # Check the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file with the provided contents
        with open(os.path.join(directory, filename), "w") as f:
            f.write(content)

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
