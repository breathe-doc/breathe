
from docutils import nodes
from docutils.parsers.rst.directives import unchanged_required, unchanged, flag

import os
import sys
import copy
import fnmatch
import re
import textwrap
import collections
import subprocess

from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.domains.cpp import DefinitionParser

from breathe.finder import FinderFactory, NoMatchesError, MultipleMatchesError
from breathe.parser import DoxygenParserFactory, CacheFactory, ParserError
from breathe.renderer.rst.doxygen import DoxygenToRstRendererFactoryCreatorConstructor, RstContentCreator
from breathe.renderer.rst.doxygen import format_parser_error
from breathe.renderer.rst.doxygen.domain import DomainHandlerFactoryCreator, NullDomainHandler
from breathe.renderer.rst.doxygen.domain import CppDomainHelper, CDomainHelper
from breathe.renderer.rst.doxygen.filter import FilterFactory, GlobFactory
from breathe.renderer.rst.doxygen.target import TargetHandlerFactory
from breathe.finder.doxygen import DoxygenItemFinderFactoryCreator, ItemMatcherFactory
from breathe.transforms import DoxygenTransform, DoxygenAutoTransform, TransformWrapper, IndexHandler
from breathe.nodes import DoxygenNode, DoxygenAutoNode
from breathe.process import DoxygenProcessHandle

import docutils.nodes
import sphinx.addnodes
import sphinx.ext.mathbase

# Somewhat outrageously, reach in and fix a Sphinx regex
import sphinx.domains.cpp
sphinx.domains.cpp._identifier_re = re.compile(r'(~?\b[a-zA-Z_][a-zA-Z0-9_]*)\b')

class BreatheError(Exception):
    pass

class NoMatchingFunctionError(BreatheError):
    pass

class UnableToResolveFunctionError(BreatheError):
    pass

class ProjectError(BreatheError):
    pass

class NoDefaultProjectError(ProjectError):
    pass


class BaseDirective(rst.Directive):

    def __init__(
            self,
            root_data_object,
            renderer_factory_creator_constructor,
            finder_factory,
            matcher_factory,
            project_info_factory,
            filter_factory,
            target_handler_factory,
            *args
            ):
        rst.Directive.__init__(self, *args)

        self.root_data_object = root_data_object
        self.renderer_factory_creator_constructor = renderer_factory_creator_constructor
        self.finder_factory = finder_factory
        self.matcher_factory = matcher_factory
        self.project_info_factory = project_info_factory
        self.filter_factory = filter_factory
        self.target_handler_factory = target_handler_factory

    def render(self, data_object, project_info, filter_, target_handler):
        "Standard render process used by subclasses"

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
                project_info,
                self.state.document,
                self.options,
                target_handler
                )

        try:
            renderer_factory = renderer_factory_creator.create_factory(
                    data_object,
                    self.state,
                    self.state.document,
                    filter_,
                    target_handler,
                    )
        except ParserError, e:
            return format_parser_error("doxygenclass", e.error, e.filename, self.state, self.lineno, True)
        except FileIOError, e:
            return format_parser_error("doxygenclass", e.error, e.filename, self.state, self.lineno)

        object_renderer = renderer_factory.create_renderer(self.root_data_object, data_object)
        node_list = object_renderer.render()

        return node_list

# Directives
# ----------

class DoxygenIndexDirective(BaseDirective):

    required_arguments = 0
    optional_arguments = 2
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenindex: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        handler = IndexHandler(
                "doxygenindex",
                project_info,
                self.options,
                self.state,
                self.lineno,
                self
                )

        return [DoxygenNode(handler)]

class AutoDoxygenIndexDirective(BaseDirective):

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
            "source-path": unchanged_required,
            "source": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        files = self.arguments[0].split()

        try:
            project_info = self.project_info_factory.create_auto_project_info(self.options)
        except ProjectError, e:
            warning = 'autodoxygenindex: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        return [DoxygenAutoNode(project_info, files, self.options, self, self.state, self.lineno)]


class DoxygenFunctionDirective(BaseDirective):

    required_arguments = 1
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False
    final_argument_whitespace = True

    def run(self):

        # Separate possible arguments (delimited by a "(") from the namespace::name
        match = re.match( r"([^(]*)(.*)", self.arguments[0] )
        namespaced_function, args = match.group(1), match.group(2)

        # Split the namespace and the function name
        try:
            (namespace, function_name) = namespaced_function.rsplit( "::", 1 )
        except ValueError:
            (namespace, function_name) = "", namespaced_function

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenfunction: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        finder = self.finder_factory.create_finder(project_info)

        # Extract arguments from the function name.
        args = self.parse_args(args)

        matcher_stack = self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_matcher(namespace),
                    "member": self.matcher_factory.create_name_type_matcher(function_name, "function")
                },
                "member"
            )

        results = finder.find(matcher_stack)

        try:
            data_object = self.resolve_function(results, args)
        except NoMatchingFunctionError:
            warning = ('doxygenfunction: Cannot find function "%s%s" in doxygen xml output '
                    'for project "%s" from directory: %s'
                    % (namespace, function_name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]
        except UnableToResolveFunctionError:
            warning = ('doxygenfunction: Unable to resolve multiple matches for function "%s%s" with arguments (%s) in doxygen xml output '
                    'for project "%s" from directory: %s.'
                    % (namespace, function_name, ", ".join(args), project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(self.options)

        return self.render(data_object, project_info, filter_, target_handler)


    def parse_args(self, function_description):

        paren_index = function_description.find('(')
        if paren_index == -1:
            return []
        else:
            # Parse the function name string, eg. f(int, float) to
            # extract the types so we can use them for matching
            args = []
            num_open_brackets = -1;
            start = paren_index + 1
            for i in range(paren_index, len(function_description)):
                c = function_description[i]
                if c == '(' or c == '<':
                    num_open_brackets += 1
                elif c == ')' or c == '>':
                    num_open_brackets -= 1
                elif c == ',' and num_open_brackets == 0:
                    args.append(function_description[start:i].strip())
                    start = i + 1
            args.append(function_description[start:-1].strip())

            return args


    def resolve_function(self, matches, args):

        if not matches:
            raise NoMatchingFunctionError()

        if len(matches) == 1:
            return matches[0]

        data_object = None

        # Tries to match the args array agains the arguments listed in the
        # doxygen data
        # TODO: We don't have any doxygen xml dom accessing code at this level
        # this might benefit from being abstracted away at some point
        for entry in matches:
            if len(args) == len(entry.param):
                equal = True
                for i in range(len(args)):
                    param_type = entry.param[i].type_.content_[0].value
                    if not isinstance(param_type, unicode) :
                        param_type = param_type.valueOf_
                    if args[i] != param_type:
                        equal = False
                        break
                if equal:
                    data_object = entry
                    break

        if not data_object:
            raise UnableToResolveFunctionError()

        return data_object


class DoxygenClassDirective(BaseDirective):

    kind = "class"

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "members": unchanged,
            "sections": unchanged,
            "show": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        name = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygen%s: %s' % (self.kind, e)
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        finder = self.finder_factory.create_finder(project_info)

        matcher_stack = self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
                "compound"
            )

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError, e:
            warning = ('doxygen%s: Cannot find %s "%s" in doxygen xml output for project "%s" from directory: %s'
                    % (self.kind, self.kind, name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_class_filter(self.options)

        return self.render(data_object, project_info, filter_, target_handler)


class DoxygenFileDirective(BaseDirective):

    kind = "file"

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        name = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygenfile: %s' % e
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        finder = self.finder_factory.create_finder(project_info)

        finder_filter = self.filter_factory.create_file_finder_filter(name)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) > 1:
            warning = ('doxygenfile: Found multiple matches for file "%s" in doxygen xml output for project "%s" '
                    'from directory: %s' % (name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        elif not matches:
            warning = ('doxygenfile: Cannot find file "%s" in doxygen xml output for project "%s" from directory: %s'
                    % (name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_file_filter(name, self.options)

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
                project_info,
                self.state.document,
                self.options,
                target_handler
                )
        node_list = []
        for data_object in matches:

            renderer_factory = renderer_factory_creator.create_factory(
                    data_object,
                    self.state,
                    self.state.document,
                    filter_,
                    target_handler,
                    )

            object_renderer = renderer_factory.create_renderer(self.root_data_object, data_object)
            node_list.extend(object_renderer.render())

        return node_list


class DoxygenBaseDirective(BaseDirective):

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        try:
            namespace, name = self.arguments[0].rsplit("::", 1)
        except ValueError:
            namespace, name = "", self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygen%s: %s' % (self.kind, e)
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        finder = self.finder_factory.create_finder(project_info)

        matcher_stack = self.create_matcher_stack(namespace, name)

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError, e:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = ('doxygen%s: Cannot find %s "%s" in doxygen xml output for project "%s" from directory: %s'
                    % (self.kind, self.kind, display_name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(self.options)

        return self.render(data_object, project_info, filter_, target_handler)


class DoxygenStructDirective(DoxygenBaseDirective):

    kind = "struct"

    def create_matcher_stack(self, namespace, name):

        # Structs are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name

        return self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_type_matcher(xml_name, self.kind)
                },
                "compound"
            )


# This class was the same as the DoxygenBaseDirective above, except that it
# wraps the output in a definition_list before passing it back. This should be
# abstracted in a far nicely way to avoid repeating so much code
#
# Now we're removed the definition_list wrap so we really need to refactor this!
class DoxygenBaseItemDirective(BaseDirective):

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
            "path": unchanged_required,
            "project": unchanged_required,
            "outline": flag,
            "no-link": flag,
            }
    has_content = False

    def run(self):

        try:
            namespace, name = self.arguments[0].rsplit("::", 1)
        except ValueError:
            namespace, name = "", self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError, e:
            warning = 'doxygen%s: %s' % (self.kind, e)
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        finder = self.finder_factory.create_finder(project_info)

        matcher_stack = self.create_matcher_stack(namespace, name)

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError, e:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = ('doxygen%s: Cannot find %s "%s" in doxygen xml output for project "%s" from directory: %s'
                    % (self.kind, self.kind, display_name, project_info.name(), project_info.project_path()))
            return [docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(warning))),
                    self.state.document.reporter.warning(warning, line=self.lineno)]

        target_handler = self.target_handler_factory.create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(self.options)

        return self.render(data_object, project_info, filter_, target_handler)


class DoxygenVariableDirective(DoxygenBaseItemDirective):

    kind = "variable"

    def create_matcher_stack(self, namespace, name):

        return self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_matcher(namespace),
                    "member": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
                "member"
            )

class DoxygenDefineDirective(DoxygenBaseItemDirective):

    kind = "define"

    def create_matcher_stack(self, namespace, name):

        return self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_matcher(namespace),
                    "member": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
                "member"
            )

class DoxygenEnumDirective(DoxygenBaseItemDirective):

    kind = "enum"

    def create_matcher_stack(self, namespace, name):

        return self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_matcher(namespace),
                    "member": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
                "member"
            )

class DoxygenTypedefDirective(DoxygenBaseItemDirective):

    kind = "typedef"

    def create_matcher_stack(self, namespace, name):

        return self.matcher_factory.create_matcher_stack(
                {
                    "compound": self.matcher_factory.create_name_matcher(namespace),
                    "member": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
                "member"
            )
# Setup Administration
# --------------------

class DirectiveContainer(object):

    def __init__(
            self,
            directive,
            *args
            ):

        self.directive = directive
        self.args = args

        # Required for sphinx to inspect
        self.required_arguments = directive.required_arguments
        self.optional_arguments = directive.optional_arguments
        self.option_spec = directive.option_spec
        self.has_content = directive.has_content
        self.final_argument_whitespace = directive.final_argument_whitespace

    def __call__(self, *args):

        call_args = []
        call_args.extend(self.args)
        call_args.extend(args)

        return self.directive(*call_args)


class AutoProjectInfo(object):

    def __init__(
            self,
            name,
            source_path,
            build_dir,
            reference,
            source_dir,
            domain_by_extension,
            domain_by_file_pattern,
            match
            ):

        self._name = name
        self._source_path = source_path
        self._build_dir = build_dir
        self._reference = reference
        self._source_dir = source_dir
        self._domain_by_extension = domain_by_extension
        self._domain_by_file_pattern = domain_by_file_pattern
        self._match = match

    def name(self):
        return self._name

    def build_dir(self):
        return self._build_dir

    def abs_path_to_source_file(self, file_):
        """
        Returns full path to the provide file assuming that the provide path is relative to the
        projects source directory as specified in the breathe_projects_source config variable.
        """

        if os.path.isabs(self._source_path):
            full_source_path = self._source_path
        else:
            full_source_path = os.path.realpath(self._source_path)

        return os.path.join(full_source_path, file_)

    def create_project_info(self, project_path):

        return ProjectInfo(
            self._name,
            project_path,
            self._source_path,
            self._reference,
            self._source_dir,
            self._domain_by_extension,
            self._domain_by_file_pattern,
            self._match
            )

class ProjectInfo(object):

    def __init__(
            self,
            name,
            path,
            source_path,
            reference,
            source_dir,
            domain_by_extension,
            domain_by_file_pattern,
            match
            ):

        self._name = name
        self._project_path = path
        self._source_path = source_path
        self._reference = reference
        self._source_dir = source_dir
        self._domain_by_extension = domain_by_extension
        self._domain_by_file_pattern = domain_by_file_pattern
        self._match = match

    def name(self):
        return self._name

    def project_path(self):
        return self._project_path

    def source_path(self):
        return self._source_path

    def relative_path_to_xml_file(self, file_):
        """
        Returns relative path from Sphinx documentation top-level source directory to the specified
        file assuming that the specified file is a path relative to the doxygen xml output directory.
        """
        if os.path.isabs(self._project_path):
            full_xml_project_path = self._project_path
        else:
            full_xml_project_path = os.path.realpath(self._project_path)

        return os.path.relpath(
                os.path.join(full_xml_project_path, file_),
                self._source_dir
                )

    def sphinx_abs_path_to_file(self, file_):
        """
        Prepends os.path.sep to the value returned by relative_path_to_file.

        This is to match Sphinx's concept of an absolute path which starts from the top-level source
        directory of the project.
        """
        return os.path.sep + self.relative_path_to_xml_file(file_)

    def reference(self):
        return self._reference

    def domain_for_file(self, file_):

        domain = ""
        extension = file_.split(".")[-1]

        try:
            domain = self._domain_by_extension[extension]
        except KeyError:
            pass

        for pattern, pattern_domain in self._domain_by_file_pattern.items():
            if self._match(file_, pattern):
                domain = pattern_domain

        return domain


class ProjectInfoFactory(object):

    def __init__(self, source_dir, build_dir, match):

        self.source_dir = source_dir
        self.build_dir = build_dir
        self.match = match

        self.projects = {}
        self.default_project = None
        self.domain_by_extension = {}
        self.domain_by_file_pattern = {}

        self.project_count = 0
        self.project_info_store = {}
        self.auto_project_info_store = {}

    def update(
            self,
            projects,
            default_project,
            domain_by_extension,
            domain_by_file_pattern,
            projects_source,
            build_dir
            ):

        self.projects = projects
        self.default_project = default_project
        self.domain_by_extension = domain_by_extension
        self.domain_by_file_pattern = domain_by_file_pattern
        self.projects_source = projects_source

        # If the breathe config values has a non-empty value for build_dir then use that otherwise
        # stick with the default
        if build_dir:
            self.build_dir = build_dir

    def default_path(self):

        if not self.default_project:
            raise NoDefaultProjectError(
                    "No breathe_default_project config setting to fall back on "
                    "for directive with no 'project' or 'path' specified."
                    )

        try:
            return self.projects[self.default_project]
        except KeyError:
            raise ProjectError(
                    ( "breathe_default_project value '%s' does not seem to be a valid key for the "
                      "breathe_projects dictionary" ) % self.default_project
                    )

    def create_project_info(self, options):

        name = ""

        if "project" in options:
            try:
                path = self.projects[options["project"]]
                name = options["project"]
            except KeyError, e:
                raise ProjectError( "Unable to find project '%s' in breathe_projects dictionary" % options["project"] )

        elif "path" in options:
            path = options["path"]

        else:
            path = self.default_path()

        try:
            return self.project_info_store[path]
        except KeyError:

            reference = name

            if not name:
                name = "project%s" % self.project_count
                reference = path
                self.project_count += 1

            project_info = ProjectInfo(
                    name,
                    path,
                    "NoSourcePath",
                    reference,
                    self.source_dir,
                    self.domain_by_extension,
                    self.domain_by_file_pattern,
                    self.match
                    )

            self.project_info_store[path] = project_info

            return project_info

    def create_auto_project_info(self, options):

        name = ""

        if "source" in options:
            try:
                source_path = self.projects_source[options["source"]]
                name = options["source"]
            except KeyError, e:
                raise ProjectError( "Unable to find project '%s' in breathe_projects_source dictionary" % options["source"] )

        elif "source-path" in options:
            source_path = options["source-path"]

        else:
            raise ProjectError( "Unable to find either :project: or :path: specified" )

        try:
            return self.auto_project_info_store[source_path]
        except KeyError:

            reference = name

            if not name:
                name = "project%s" % self.project_count
                reference = source_path
                self.project_count += 1

            auto_project_info = AutoProjectInfo(
                    name,
                    source_path,
                    self.build_dir,
                    reference,
                    self.source_dir,
                    self.domain_by_extension,
                    self.domain_by_file_pattern,
                    self.match
                    )

            self.auto_project_info_store[source_path] = auto_project_info

            return auto_project_info

class DoxygenDirectiveFactory(object):

    directives = {
            "doxygenindex": DoxygenIndexDirective,
            "doxygenfunction": DoxygenFunctionDirective,
            "doxygenstruct": DoxygenStructDirective,
            "doxygenclass": DoxygenClassDirective,
            "doxygenvariable": DoxygenVariableDirective,
            "doxygendefine": DoxygenDefineDirective,
            "doxygenenum": DoxygenEnumDirective,
            "doxygentypedef": DoxygenTypedefDirective,
            "doxygenfile": DoxygenFileDirective,
            "autodoxygenindex": AutoDoxygenIndexDirective,
            }

    def __init__(
            self,
            root_data_object,
            renderer_factory_creator_constructor,
            finder_factory,
            matcher_factory,
            project_info_factory,
            filter_factory,
            target_handler_factory
            ):
        self.root_data_object = root_data_object
        self.renderer_factory_creator_constructor = renderer_factory_creator_constructor
        self.finder_factory = finder_factory
        self.matcher_factory = matcher_factory
        self.project_info_factory = project_info_factory
        self.filter_factory = filter_factory
        self.target_handler_factory = target_handler_factory

    def create_index_directive_container(self):
        return self.create_directive_container("doxygenindex")

    def create_function_directive_container(self):
        return self.create_directive_container("doxygenfunction")

    def create_struct_directive_container(self):
        return self.create_directive_container("doxygenstruct")

    def create_enum_directive_container(self):
        return self.create_directive_container("doxygenenum")

    def create_typedef_directive_container(self):
        return self.create_directive_container("doxygentypedef")

    def create_class_directive_container(self):
        return self.create_directive_container("doxygenclass")

    def create_file_directive_container(self):
        return self.create_directive_container("doxygenfile")

    def create_variable_directive_container(self):
        return self.create_directive_container("doxygenvariable")

    def create_define_directive_container(self):
        return self.create_directive_container("doxygendefine")

    def create_auto_index_directive_container(self):
        return self.create_directive_container("autodoxygenindex")

    def create_directive_container(self, type_):

        return DirectiveContainer(
                self.directives[type_],
                self.root_data_object,
                self.renderer_factory_creator_constructor,
                self.finder_factory,
                self.matcher_factory,
                self.project_info_factory,
                self.filter_factory,
                self.target_handler_factory
                )

    def get_config_values(self, app):

        # All DirectiveContainers maintain references to this project info factory
        # so we can update this to update them
        self.project_info_factory.update(
                app.config.breathe_projects,
                app.config.breathe_default_project,
                app.config.breathe_domain_by_extension,
                app.config.breathe_domain_by_file_pattern,
                app.config.breathe_projects_source,
                app.config.breathe_build_directory
                )


class NodeFactory(object):

    def __init__(self, *args):

        self.sources = args

    def __getattr__(self, node_name):

        for source in self.sources:
            try:
                return getattr(source, node_name)
            except AttributeError:
                pass

        raise NodeNotFoundError(node_name)


class RootDataObject(object):

    node_type = "root"


class PathHandler(object):

    def __init__(self, sep, basename, join):

        self.sep = sep
        self.basename = basename
        self.join = join

    def includes_directory(self, file_path):

        return bool( file_path.count( self.sep ) )

def write_file(directory, filename, content):

    # Check the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the file with the provided contents
    with open(os.path.join(directory, filename), "w") as f:
        f.write(content)

class MTimer(object):

    def __init__(self, getmtime):
        self.getmtime = getmtime

    def get_mtime(self, filename):
        return self.getmtime(filename)

class FileStateCache(object):
    """
    Stores the modified time of the various doxygen xml files against the
    reStructuredText file that they are referenced from so that we know which
    reStructuredText files to rebuild if the doxygen xml is modified.

    We store the information in the environment object so that it is pickled
    down and stored between builds as Sphinx is designed to do.
    """

    def __init__(self, mtimer, app):

        self.app = app
        self.mtimer = mtimer

    def update(self, source_file):

        if not hasattr( self.app.env, "breathe_file_state" ):
            self.app.env.breathe_file_state = {}

        new_mtime = self.mtimer.get_mtime(source_file)

        mtime, docnames = self.app.env.breathe_file_state.setdefault(source_file, (new_mtime, set()))

        docnames.add(self.app.env.docname)

        self.app.env.breathe_file_state[source_file] = (new_mtime, docnames)

    def get_outdated(self, app, env, added, changed, removed):

        if not hasattr( self.app.env, "breathe_file_state" ):
            return []

        stale = []

        for filename, info in self.app.env.breathe_file_state.iteritems():
            old_mtime, docnames = info
            if self.mtimer.get_mtime(filename) > old_mtime:
                stale.extend(docnames)

        return list(set(stale).difference(removed))

    def purge_doc(self, app, env, docname):

        if not hasattr( self.app.env, "breathe_file_state" ):
            return

        toremove = []

        for filename, info in self.app.env.breathe_file_state.iteritems():

            _, docnames = info
            docnames.discard(docname)
            if not docnames:
                toremove.append(filename)

        for filename in toremove:
            del self.app.env.breathe_file_state[filename]

# Setup
# -----

def setup(app):

    cache_factory = CacheFactory()
    cache = cache_factory.create_cache()
    path_handler = PathHandler(os.sep, os.path.basename, os.path.join)
    mtimer = MTimer(os.path.getmtime)
    file_state_cache = FileStateCache(mtimer, app)
    parser_factory = DoxygenParserFactory(cache, path_handler, file_state_cache)
    matcher_factory = ItemMatcherFactory()
    item_finder_factory_creator = DoxygenItemFinderFactoryCreator(parser_factory, matcher_factory)
    index_parser = parser_factory.create_index_parser()
    finder_factory = FinderFactory(index_parser, item_finder_factory_creator)

    # Create a math_nodes object with a displaymath member for the displaymath
    # node so that we can treat it in the same way as the nodes & addnodes
    # modules in the NodeFactory
    math_nodes = collections.namedtuple("MathNodes", ["displaymath"])
    math_nodes.displaymath = sphinx.ext.mathbase.displaymath
    node_factory = NodeFactory(docutils.nodes, sphinx.addnodes, math_nodes)

    cpp_domain_helper = CppDomainHelper(DefinitionParser, re.sub)
    c_domain_helper = CDomainHelper()
    domain_helpers = {"c": c_domain_helper, "cpp": cpp_domain_helper}
    domain_handler_factory_creator = DomainHandlerFactoryCreator(node_factory, domain_helpers)

    rst_content_creator = RstContentCreator(ViewList, textwrap.dedent)
    default_domain_handler = NullDomainHandler()
    renderer_factory_creator_constructor = DoxygenToRstRendererFactoryCreatorConstructor(
            node_factory,
            parser_factory,
            default_domain_handler,
            domain_handler_factory_creator,
            rst_content_creator
            )

    # Assume general build directory is the doctree directory without the last component. We strip
    # off any trailing slashes so that dirname correctly drops the last part. This can be overriden
    # with the breathe_build_directory config variable
    build_dir = os.path.dirname(app.doctreedir.rstrip(os.sep))
    project_info_factory = ProjectInfoFactory(app.srcdir, build_dir, fnmatch.fnmatch)
    glob_factory = GlobFactory(fnmatch.fnmatch)
    filter_factory = FilterFactory(glob_factory, path_handler)
    target_handler_factory = TargetHandlerFactory(node_factory)

    root_data_object = RootDataObject()

    directive_factory = DoxygenDirectiveFactory(
            root_data_object,
            renderer_factory_creator_constructor,
            finder_factory,
            matcher_factory,
            project_info_factory,
            filter_factory,
            target_handler_factory
            )

    app.add_directive(
            "doxygenindex",
            directive_factory.create_index_directive_container(),
            )

    app.add_directive(
            "doxygenfunction",
            directive_factory.create_function_directive_container(),
            )

    app.add_directive(
            "doxygenstruct",
            directive_factory.create_struct_directive_container(),
            )

    app.add_directive(
            "doxygenenum",
            directive_factory.create_enum_directive_container(),
            )

    app.add_directive(
            "doxygentypedef",
            directive_factory.create_typedef_directive_container(),
            )

    app.add_directive(
            "doxygenclass",
            directive_factory.create_class_directive_container(),
            )

    app.add_directive(
            "doxygenfile",
            directive_factory.create_file_directive_container(),
            )

    app.add_directive(
            "doxygenvariable",
            directive_factory.create_variable_directive_container(),
            )

    app.add_directive(
            "doxygendefine",
            directive_factory.create_define_directive_container(),
            )

    app.add_directive(
            "autodoxygenindex",
            directive_factory.create_auto_index_directive_container(),
            )

    doxygen_handle = DoxygenProcessHandle(path_handler, subprocess.check_call, write_file)
    app.add_transform(TransformWrapper(DoxygenAutoTransform, doxygen_handle))

    app.add_transform(DoxygenTransform)

    app.add_node(DoxygenNode)

    app.add_config_value("breathe_projects", {}, True)
    app.add_config_value("breathe_default_project", "", True)
    app.add_config_value("breathe_domain_by_extension", {}, True)
    app.add_config_value("breathe_domain_by_file_pattern", {}, True)
    app.add_config_value("breathe_projects_source", {}, True)
    app.add_config_value("breathe_build_directory", '', True)

    app.add_stylesheet("breathe.css")

    app.connect("builder-inited", directive_factory.get_config_values)

    app.connect("env-get-outdated", file_state_cache.get_outdated)

    app.connect("env-purge-doc", file_state_cache.purge_doc)

