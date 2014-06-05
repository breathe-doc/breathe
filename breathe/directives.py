
from breathe.finder.core import FinderFactory, NoMatchesError
from breathe.parser import DoxygenParserFactory, CacheFactory
from breathe.renderer.rst.doxygen import DoxygenToRstRendererFactoryCreatorConstructor, \
    RstContentCreator
from breathe.renderer.rst.doxygen.domain import DomainHandlerFactoryCreator, NullDomainHandler
from breathe.renderer.rst.doxygen.domain import CppDomainHelper, CDomainHelper
from breathe.renderer.rst.doxygen.filter import FilterFactory, GlobFactory
from breathe.renderer.rst.doxygen.target import TargetHandlerFactory
from breathe.finder.doxygen.core import DoxygenItemFinderFactoryCreator
from breathe.finder.doxygen.matcher import ItemMatcherFactory
from breathe.directive.base import BaseDirective, DoxygenBaseDirective
from breathe.directive.index import DoxygenIndexDirective, AutoDoxygenIndexDirective
from breathe.directive.file import DoxygenFileDirective, AutoDoxygenFileDirective
from breathe.process import AutoDoxygenProcessHandle
from breathe.exception import BreatheError
from breathe.project import ProjectInfoFactory, ProjectError

from docutils.parsers.rst.directives import unchanged_required, unchanged, flag
from docutils.statemachine import ViewList
from sphinx.domains.cpp import DefinitionParser

import docutils.nodes
import sphinx.addnodes
import sphinx.ext.mathbase

import os
import fnmatch
import re
import textwrap
import collections
import subprocess

# Somewhat outrageously, reach in and fix a Sphinx regex
import sphinx.domains.cpp
sphinx.domains.cpp._identifier_re = re.compile(r'(~?\b[a-zA-Z_][a-zA-Z0-9_]*)\b')


class NoMatchingFunctionError(BreatheError):
    pass


class UnableToResolveFunctionError(BreatheError):
    pass


class NodeNotFoundError(BreatheError):
    pass


# Directives
# ----------

class WarningHandler(object):

    def __init__(self, state, context):
        self.state = state
        self.context = context

    def warn(self, text):
        result = text.format(**self.context)
        return [
            docutils.nodes.warning("", docutils.nodes.paragraph("", "", docutils.nodes.Text(result))),
            self.state.document.reporter.warning(result, line=self.context['lineno'])
            ]


def create_warning(project_info, state, lineno, **kwargs):

    tail = ''
    if project_info:
        tail = 'in doxygen xml output for project "{project}" from directory: {path}'.format(
            project=project_info.name(),
            path=project_info.project_path()
            )

    context = dict(
        lineno=lineno,
        tail=tail,
        **kwargs
        )

    return WarningHandler(state, context)


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
        match = re.match(r"([^(]*)(.*)", self.arguments[0])
        namespaced_function, args = match.group(1), match.group(2)

        # Split the namespace and the function name
        try:
            (namespace, function_name) = namespaced_function.rsplit("::", 1)
        except ValueError:
            (namespace, function_name) = "", namespaced_function

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenfunction: %s' % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimerError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenfunction: %s' % e)

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

        # Create it ahead of time as it is cheap and it is ugly to declare it for both exception
        # clauses below
        warning = create_warning(
            project_info,
            self.state,
            self.lineno,
            namespace='%s::' % namespace if namespace else '',
            function=function_name,
            args=', '.join(args)
            )

        try:
            data_object = self.resolve_function(results, args)
        except NoMatchingFunctionError:
            return warning.warn('doxygenfunction: Cannot find function "{namespace}{function}" '
                                '{tail}')
        except UnableToResolveFunctionError:
            return warning.warn('doxygenfunction: Unable to resolve multiple matches for function '
                                '"{namespace}{function}" with arguments ({args}) {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
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
            num_open_brackets = -1
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
                    if not isinstance(param_type, unicode):
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
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenclass: %s' % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimerError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenclass: %s' % e)

        matcher_stack = self.matcher_factory.create_matcher_stack(
            {
                "compound": self.matcher_factory.create_name_type_matcher(name, self.kind)
                },
            "compound"
            )

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError as e:
            warning = create_warning(project_info, self.state, self.lineno, name=name)
            return warning.warn('doxygenclass: Cannot find class "{name}" {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_class_filter(self.options)

        return self.render(data_object, project_info, filter_, target_handler)


class DoxygenGroupDirective(BaseDirective):

    kind = "group"

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "content-only": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):

        name = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygengroup: %s' % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimerError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygengroup: %s' % e)

        finder_filter = self.filter_factory.create_group_finder_filter(name)

        matches = []
        finder.filter_(finder_filter, matches)

        # It shouldn't be possible to have too many matches as groups in their nature are merged
        # together if there are multiple declarations, so we only check for no matches
        if not matches:
            warning = create_warning(project_info, self.state, self.lineno, name=name)
            return warning.warn('doxygengroup: Cannot find group "{name}" {tail}')

        if 'content-only' in self.options:

            # Unpack the single entry in the matches list
            (data_object,) = matches

            filter_ = self.filter_factory.create_group_content_filter()

            # Having found the compound node for the group in the index we want to grab the contents
            # of
            contents_finder = self.finder_factory.create_finder_from_root(data_object, project_info)
            contents = []
            contents_finder.filter_(filter_, contents)

            # Replaces matches with our new starting points
            matches = contents

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_open_filter()

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
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno, kind=self.kind)
            return warning.warn('doxygen{kind}: %s' % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimerError as e:
            warning = create_warning(None, self.state, self.lineno, kind=self.kind)
            return warning.warn('doxygen{kind}: %s' % e)


        matcher_stack = self.create_matcher_stack(namespace, name)

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError as e:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = create_warning(project_info, self.state, self.lineno, kind=self.kind,
                                     name=display_name)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{display_name}" {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
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


class DoxygenUnionDirective(DoxygenBaseItemDirective):

    kind = "union"

    def create_matcher_stack(self, namespace, name):

        # Unions are stored in the xml file with their fully namespaced name
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


# Setup Administration
# --------------------

class DirectiveContainer(object):

    def __init__(self, directive, *args):

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


class DoxygenDirectiveFactory(object):

    directives = {
        "doxygenindex": DoxygenIndexDirective,
        "autodoxygenindex": AutoDoxygenIndexDirective,
        "doxygenfunction": DoxygenFunctionDirective,
        "doxygenstruct": DoxygenStructDirective,
        "doxygenclass": DoxygenClassDirective,
        "doxygenvariable": DoxygenVariableDirective,
        "doxygendefine": DoxygenDefineDirective,
        "doxygenenum": DoxygenEnumDirective,
        "doxygentypedef": DoxygenTypedefDirective,
        "doxygenunion": DoxygenUnionDirective,
        "doxygengroup": DoxygenGroupDirective,
        "doxygenfile": DoxygenFileDirective,
        "autodoxygenfile": AutoDoxygenFileDirective,
        }

    def __init__(self, root_data_object, renderer_factory_creator_constructor, finder_factory,
                 matcher_factory, project_info_factory, filter_factory, target_handler_factory):

        self.root_data_object = root_data_object
        self.renderer_factory_creator_constructor = renderer_factory_creator_constructor
        self.finder_factory = finder_factory
        self.matcher_factory = matcher_factory
        self.project_info_factory = project_info_factory
        self.filter_factory = filter_factory
        self.target_handler_factory = target_handler_factory

    # TODO: This methods should be scrapped as they are only called in one place. We should just
    # inline the code at the call site
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

    def create_union_directive_container(self):
        return self.create_directive_container("doxygenunion")

    def create_class_directive_container(self):
        return self.create_directive_container("doxygenclass")

    def create_file_directive_container(self):
        return self.create_directive_container("doxygenfile")

    def create_group_directive_container(self):
        return self.create_directive_container("doxygengroup")

    def create_variable_directive_container(self):
        return self.create_directive_container("doxygenvariable")

    def create_define_directive_container(self):
        return self.create_directive_container("doxygendefine")

    def create_auto_index_directive_container(self):
        return self.create_directive_container("autodoxygenindex")

    def create_auto_file_directive_container(self):
        return self.create_directive_container("autodoxygenfile")

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

    def __init__(self, config_directory, sep, basename, join):

        self.config_directory = config_directory

        self.sep = sep
        self.basename = basename
        self.join = join

    def includes_directory(self, file_path):

        return bool(file_path.count(self.sep))

    def resolve_path(self, directory, filename):
        """Returns a full path to the filename in the given directory assuming that if the directory
        path is relative, then it is relative to the conf.py directory.
        """

        # os.path.join does the appropriate handling if _project_path is an absolute path
        return self.join(self.config_directory, directory, filename)


def write_file(directory, filename, content):

    # Check the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the file with the provided contents
    with open(os.path.join(directory, filename), "w") as f:
        f.write(content)


class MTimerError(Exception):
    pass


class MTimer(object):

    def __init__(self, getmtime):
        self.getmtime = getmtime

    def get_mtime(self, filename):

        try:
            return self.getmtime(filename)
        except OSError:
            raise MTimerError('Cannot find file: %s' % os.path.realpath(filename))


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

        if not hasattr(self.app.env, "breathe_file_state"):
            self.app.env.breathe_file_state = {}

        new_mtime = self.mtimer.get_mtime(source_file)

        mtime, docnames = self.app.env.breathe_file_state.setdefault(
            source_file, (new_mtime, set())
            )

        docnames.add(self.app.env.docname)

        self.app.env.breathe_file_state[source_file] = (new_mtime, docnames)

    def get_outdated(self, app, env, added, changed, removed):

        if not hasattr(self.app.env, "breathe_file_state"):
            return []

        stale = []

        for filename, info in self.app.env.breathe_file_state.iteritems():
            old_mtime, docnames = info
            if self.mtimer.get_mtime(filename) > old_mtime:
                stale.extend(docnames)

        return list(set(stale).difference(removed))

    def purge_doc(self, app, env, docname):

        if not hasattr(self.app.env, "breathe_file_state"):
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
    path_handler = PathHandler(app.confdir, os.sep, os.path.basename, os.path.join)
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
    project_info_factory = ProjectInfoFactory(app.srcdir, build_dir, app.confdir, fnmatch.fnmatch)
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
        "doxygenunion",
        directive_factory.create_union_directive_container(),
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
        "doxygengroup",
        directive_factory.create_group_directive_container(),
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

    app.add_directive(
        "autodoxygenfile",
        directive_factory.create_auto_file_directive_container(),
        )

    app.add_config_value("breathe_projects", {}, True)
    app.add_config_value("breathe_default_project", "", True)
    app.add_config_value("breathe_domain_by_extension", {}, True)
    app.add_config_value("breathe_domain_by_file_pattern", {}, True)
    app.add_config_value("breathe_projects_source", {}, True)
    app.add_config_value("breathe_build_directory", '', True)

    app.add_stylesheet("breathe.css")

    doxygen_handle = AutoDoxygenProcessHandle(
        path_handler,
        subprocess.check_call,
        write_file,
        project_info_factory
        )

    app.connect("builder-inited", doxygen_handle.generate_xml)

    app.connect("builder-inited", directive_factory.get_config_values)

    app.connect("env-get-outdated", file_state_cache.get_outdated)

    app.connect("env-purge-doc", file_state_cache.purge_doc)

