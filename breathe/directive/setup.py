from breathe.directives import (
    DoxygenVariableDirective, DoxygenDefineDirective,
    DoxygenEnumDirective, DoxygenEnumValueDirective, DoxygenTypedefDirective,
    DoxygenUnionDirective, DoxygenNamespaceDirective, DoxygenGroupDirective,
    DoxygenPageDirective
)
from breathe.directive import BaseDirective
from breathe.directive.class_like import (
    DoxygenStructDirective, DoxygenClassDirective, DoxygenInterfaceDirective,
)
from breathe.directive.file import DoxygenFileDirective, AutoDoxygenFileDirective
from breathe.directive.function import DoxygenFunctionDirective
from breathe.directive.index import DoxygenIndexDirective, AutoDoxygenIndexDirective
from breathe.finder.factory import FinderFactory
from breathe.parser import DoxygenParserFactory
from breathe.project import ProjectInfoFactory
from breathe.process import AutoDoxygenProcessHandle

from sphinx.application import Sphinx

import os
import subprocess

from typing import Any, List, Optional, Type  # noqa


class DirectiveContainer:
    def __init__(self, app: Sphinx, directive: Type[BaseDirective],
                 finder_factory: FinderFactory, project_info_factory: ProjectInfoFactory,
                 parser_factory: DoxygenParserFactory):
        self.app = app
        self.directive = directive
        self.finder_factory = finder_factory
        self.project_info_factory = project_info_factory
        self.parser_factory = parser_factory

        # Required for sphinx to inspect
        self.required_arguments = directive.required_arguments
        self.optional_arguments = directive.optional_arguments
        self.option_spec = directive.option_spec
        self.has_content = directive.has_content
        self.final_argument_whitespace = directive.final_argument_whitespace

    def __call__(self, *args):
        call_args = [
            self.finder_factory,
            self.project_info_factory,
            self.parser_factory
        ]
        call_args.extend(args)
        return self.directive(*call_args)


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

    # note: the parser factory contains a cache of the parsed XML
    # note: the project_info_factory also contains some caching stuff
    # TODO: is that actually safe for when reading in parallel?
    project_info_factory = ProjectInfoFactory(app)
    parser_factory = DoxygenParserFactory(app)
    finder_factory = FinderFactory(app, parser_factory)
    for name, directive in directives.items():
        # ordinarily app.add_directive takes a class it self, but we need to inject extra arguments
        # so we give a DirectiveContainer object which has an overloaded __call__ operator.
        app.add_directive(name, DirectiveContainer(  # type: ignore
            app,
            directive,
            finder_factory,
            project_info_factory,
            parser_factory
            ))

    app.add_config_value("breathe_projects", {}, True)  # Dict[str, str]
    app.add_config_value("breathe_default_project", "", True)  # str
    # Provide reasonable defaults for domain_by_extension mapping. Can be overridden by users.
    app.add_config_value("breathe_domain_by_extension",
                         {'py': 'py', 'cs': 'cs'}, True)  # Dict[str, str]
    app.add_config_value("breathe_domain_by_file_pattern", {}, True)  # Dict[str, str]
    app.add_config_value("breathe_projects_source", {}, True)
    app.add_config_value("breathe_build_directory", '', True)
    app.add_config_value("breathe_default_members", (), True)
    app.add_config_value("breathe_show_define_initializer", False, 'env')
    app.add_config_value("breathe_show_enumvalue_initializer", False, 'env')
    app.add_config_value("breathe_implementation_filename_extensions", ['.c', '.cc', '.cpp'], True)
    app.add_config_value("breathe_doxygen_config_options", {}, True)
    app.add_config_value("breathe_use_project_refids", False, "env")
    app.add_config_value("breathe_order_parameters_first", False, 'env')
    app.add_config_value("breathe_separate_member_pages", False, 'env')

    breathe_css = "breathe.css"
    if (os.path.exists(os.path.join(app.confdir, "_static", breathe_css))):  # type: ignore
        app.add_css_file(breathe_css)

    def write_file(directory, filename, content):
        # Check the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file with the provided contents
        with open(os.path.join(directory, filename), "w") as f:
            f.write(content)

    doxygen_handle = AutoDoxygenProcessHandle(
        subprocess.check_call,
        write_file,
        project_info_factory)

    def doxygen_hook(app):
        doxygen_handle.generate_xml(
            app.config.breathe_projects_source,
            app.config.breathe_doxygen_config_options
        )
    app.connect("builder-inited", doxygen_hook)
