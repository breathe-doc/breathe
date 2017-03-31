
from .finder.core import FinderFactory
from .parser import DoxygenParserFactory
from .renderer import DoxygenToRstRendererFactory
from .renderer.base import RenderContext
from .renderer.filter import FilterFactory
from .renderer.target import TargetHandlerFactory
from .renderer.mask import MaskFactory, NullMaskFactory, NoParameterNamesMask

from .finder.core import DoxygenItemFinderFactoryCreator
from .directive.base import BaseDirective, create_warning
from .directive.index import DoxygenIndexDirective, AutoDoxygenIndexDirective
from .directive.file import DoxygenFileDirective, AutoDoxygenFileDirective
from .process import AutoDoxygenProcessHandle
from .exception import BreatheError
from .project import ProjectInfoFactory, ProjectError
from .node_factory import create_node_factory

from docutils.parsers.rst.directives import unchanged_required, unchanged, flag
from sphinx.writers.text import TextWriter
from sphinx.builders.text import TextBuilder

import os
import fnmatch
import re
import subprocess


class NoMatchingFunctionError(BreatheError):
    pass


class UnableToResolveFunctionError(BreatheError):

    def __init__(self, signatures):
        self.signatures = signatures


class FakeDestination(object):

    def write(self, output):
        return output


class TextRenderer(object):

    def __init__(self, app):
        self.app = app

    def render(self, nodes, document):

        new_document = document.copy()

        new_document.children = nodes

        writer = TextWriter(TextBuilder(self.app))
        output = writer.write(new_document, FakeDestination())

        return output.strip()


# Directives
# ----------

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

    def __init__(self, node_factory, text_renderer, *args, **kwargs):
        BaseDirective.__init__(self, *args, **kwargs)

        self.node_factory = node_factory
        self.text_renderer = text_renderer

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

        finder_filter = self.filter_factory.create_function_finder_filter(namespace, function_name)

        matches = []
        finder.filter_(finder_filter, matches)

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
            node_stack = self.resolve_function(matches, args, project_info)
        except NoMatchingFunctionError:
            return warning.warn('doxygenfunction: Cannot find function "{namespace}{function}" '
                                '{tail}')
        except UnableToResolveFunctionError as error:
            message = 'doxygenfunction: Unable to resolve multiple matches for function ' \
                '"{namespace}{function}" with arguments ({args}) {tail}.\n' \
                'Potential matches:\n'

            # We want to create a raw_text string for the console output and a set of docutils nodes
            # for rendering into the final output. We handle the final output as a literal string
            # with a txt based list of the options.
            raw_text = message
            literal_text = ''

            # TODO: We're cheating here with the set() as signatures has repeating entries for some
            # reason (failures in the matcher_stack code) so we consolidate them by shoving them in
            # a set to remove duplicates. Should be fixed!
            for i, entry in enumerate(sorted(set(error.signatures))):
                if i:
                    literal_text += '\n'
                # Replace new lines with a new line & enough spacing to reach the appropriate
                # alignment for our simple plain text list
                literal_text += '- %s' % entry.replace('\n', '\n  ')
                raw_text += '    - %s\n' % entry.replace('\n', '\n      ')
            block = self.node_factory.literal_block('', '', self.node_factory.Text(literal_text))
            formatted_message = warning.format(message)
            warning_nodes = [
                self.node_factory.paragraph(
                    "", "",
                    self.node_factory.Text(formatted_message)
                    ),
                block
                ]
            result = warning.warn(raw_text, warning_nodes)
            return result

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_outline_filter(self.options)

        return self.render(node_stack, project_info, filter_, target_handler, NullMaskFactory(),
                           self.directive_args)

    def parse_args(self, function_description):
        # Strip off trailing qualifiers
        pattern = re.compile(r'''(?<= \)) \s*
                             (?: = \s* 0)? \s* $ ''',
                             re.VERBOSE)

        function_description = re.sub(pattern,
                                      '',
                                      function_description)

        paren_index = function_description.find('(')
        if paren_index == -1:
            return []
        # If it is empty parenthesis, then return empty list as we want empty parenthesis coming
        # from the xml file to match the user's function when the user doesn't provide parenthesis
        # ie. when there are no args anyway
        elif function_description == '()':
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

    def resolve_function(self, matches, args, project_info):

        if not matches:
            raise NoMatchingFunctionError()

        if len(matches) == 1:
            return matches[0]

        node_stack = None

        signatures = []

        # Iterate over the potential matches
        for entry in matches:

            text_options = {'no-link': u'', 'outline': u''}

            # Render the matches to docutils nodes
            target_handler = self.target_handler_factory.create_target_handler(
                {'no-link': u''}, project_info, self.state.document
                )
            filter_ = self.filter_factory.create_outline_filter(text_options)
            mask_factory = MaskFactory({'param': NoParameterNamesMask})

            # Override the directive args for this render
            directive_args = self.directive_args[:]
            directive_args[2] = text_options

            nodes = self.render(entry, project_info, filter_, target_handler, mask_factory,
                                directive_args)

            # Render the nodes to text
            signature = self.text_renderer.render(nodes, self.state.document)
            signatures.append(signature)

            match = re.match(r"([^(]*)(.*)", signature)
            match_args = match.group(2)

            # Parse the text to find the arguments
            match_args = self.parse_args(match_args)

            # Match them against the arg spec
            if args == match_args:
                node_stack = entry
                break

        if not node_stack:
            raise UnableToResolveFunctionError(signatures)

        return node_stack


class DoxygenClassLikeDirective(BaseDirective):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "members": unchanged,
        "protected-members": flag,
        "private-members": flag,
        "undoc-members": flag,
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
            warning = create_warning(None, self.state, self.lineno, kind=self.kind)
            return warning.warn('doxygen{kind}: %s' % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimerError as e:
            warning = create_warning(None, self.state, self.lineno, kind=self.kind)
            return warning.warn('doxygen{kind}: %s' % e)

        finder_filter = self.filter_factory.create_compound_finder_filter(name, self.kind)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) == 0:
            warning = create_warning(project_info, self.state, self.lineno, name=name,
                                     kind=self.kind)
            return warning.warn('doxygen{kind}: Cannot find class "{name}" {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_class_filter(name, self.options)

        mask_factory = NullMaskFactory()
        return self.render(matches[0], project_info, filter_, target_handler, mask_factory,
                           self.directive_args)


class DoxygenClassDirective(DoxygenClassLikeDirective):

    kind = "class"


class DoxygenStructDirective(DoxygenClassLikeDirective):

    kind = "struct"


class DoxygenInterfaceDirective(DoxygenClassLikeDirective):

    kind = "interface"


class DoxygenContentBlockDirective(BaseDirective):
    """Base class for namespace and group directives which have very similar behaviours"""

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "content-only": flag,
        "outline": flag,
        "members": flag,
        "protected-members": flag,
        "private-members": flag,
        "undoc-members": flag,
        "no-link": flag
        }
    has_content = False

    def run(self):

        name = self.arguments[0]

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

        finder_filter = self.filter_factory.create_finder_filter(self.kind, name)

        matches = []
        finder.filter_(finder_filter, matches)

        # It shouldn't be possible to have too many matches as namespaces & groups in their nature
        # are merged together if there are multiple declarations, so we only check for no matches
        if not matches:
            warning = create_warning(project_info, self.state, self.lineno, name=name,
                                     kind=self.kind)
            return warning.warn('doxygen{kind}: Cannot find namespace "{name}" {tail}')

        if 'content-only' in self.options:

            # Unpack the single entry in the matches list
            (node_stack,) = matches

            filter_ = self.filter_factory.create_content_filter(self.kind, self.options)

            # Having found the compound node for the namespace or group in the index we want to grab
            # the contents of it which match the filter
            contents_finder = self.finder_factory.create_finder_from_root(node_stack[0],
                                                                          project_info)
            contents = []
            contents_finder.filter_(filter_, contents)

            # Replaces matches with our new starting points
            matches = contents

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_render_filter(self.kind, self.options)

        renderer_factory = DoxygenToRstRendererFactory(
            self.parser_factory,
            project_info
            )
        node_list = []

        for node_stack in matches:
            object_renderer = renderer_factory.create_renderer(
                node_stack,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )

            mask_factory = NullMaskFactory()
            context = RenderContext(node_stack, mask_factory, self.directive_args)
            node_list.extend(object_renderer.render(context.node_stack[0], context))

        return node_list


class DoxygenNamespaceDirective(DoxygenContentBlockDirective):

    kind = "namespace"


class DoxygenGroupDirective(DoxygenContentBlockDirective):

    kind = "group"


# This class was the same as the DoxygenBaseDirective above, except that it
# wraps the output in a definition_list before passing it back. This should be
# abstracted in a far nicer way to avoid repeating so much code
#
# Now we've removed the definition_list wrap so we really need to refactor this!
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

    def create_finder_filter(self, namespace, name):
        """Creates a filter to find the node corresponding to this item."""

        return self.filter_factory.create_member_finder_filter(
            namespace, name, self.kind)

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

        finder_filter = self.create_finder_filter(namespace, name)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) == 0:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = create_warning(project_info, self.state, self.lineno, kind=self.kind,
                                     display_name=display_name)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{display_name}" {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document
            )
        filter_ = self.filter_factory.create_outline_filter(self.options)

        node_stack = matches[0]
        mask_factory = NullMaskFactory()
        return self.render(node_stack, project_info, filter_, target_handler, mask_factory,
                           self.directive_args)


class DoxygenVariableDirective(DoxygenBaseItemDirective):

    kind = "variable"

    def render(self, node_stack, project_info, options, filter_, target_handler, mask_factory):
        # Remove 'extern' keyword as Sphinx doesn't support it.
        definition = node_stack[0].definition
        extern = 'extern '
        if definition.startswith(extern):
            definition = definition[len(extern):]
        self.directive_args[1] = [definition]
        return DoxygenBaseItemDirective.render(self, node_stack, project_info, options, filter_,
                                               target_handler, mask_factory)


class DoxygenDefineDirective(DoxygenBaseItemDirective):

    kind = "define"


class DoxygenEnumDirective(DoxygenBaseItemDirective):

    kind = "enum"


class DoxygenEnumValueDirective(DoxygenBaseItemDirective):

    kind = "enumvalue"

    def create_finder_filter(self, namespace, name):

        return self.filter_factory.create_enumvalue_finder_filter(name)


class DoxygenTypedefDirective(DoxygenBaseItemDirective):

    kind = "typedef"


class DoxygenUnionDirective(DoxygenBaseItemDirective):

    kind = "union"

    def create_finder_filter(self, namespace, name):

        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        return self.filter_factory.create_compound_finder_filter(xml_name, 'union')


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
        }

    def __init__(self, node_factory, text_renderer, finder_factory,
                 project_info_factory, filter_factory, target_handler_factory, parser_factory):

        self.node_factory = node_factory
        self.text_renderer = text_renderer
        self.finder_factory = finder_factory
        self.project_info_factory = project_info_factory
        self.filter_factory = filter_factory
        self.target_handler_factory = target_handler_factory
        self.parser_factory = parser_factory

    def create_function_directive_container(self):

        # Pass text_renderer to the function directive
        return DirectiveContainer(
            self.directives["doxygenfunction"],
            self.node_factory,
            self.text_renderer,
            self.finder_factory,
            self.project_info_factory,
            self.filter_factory,
            self.target_handler_factory,
            self.parser_factory
            )

    def create_directive_container(self, type_):

        return DirectiveContainer(
            self.directives[type_],
            self.finder_factory,
            self.project_info_factory,
            self.filter_factory,
            self.target_handler_factory,
            self.parser_factory
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
            app.config.breathe_build_directory,
            app.config.breathe_show_define_initializer,
            app.config.breathe_use_project_refids,
            )


class PathHandler(object):

    def __init__(self, config_directory, sep, basename, join):

        self.config_directory = config_directory

        self.sep = sep
        self.basename = basename
        self.join = join

    def includes_directory(self, file_path):

        # Check for backslash or forward slash as we don't know what platform we're on and sometimes
        # the doxygen paths will have forward slash even on Windows.
        return bool(file_path.count('\\')) or bool(file_path.count('/'))

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

        for filename, info in self.app.env.breathe_file_state.items():
            old_mtime, docnames = info
            if self.mtimer.get_mtime(filename) > old_mtime:
                stale.extend(docnames)

        return list(set(stale).difference(removed))

    def purge_doc(self, app, env, docname):

        if not hasattr(self.app.env, "breathe_file_state"):
            return

        toremove = []

        for filename, info in self.app.env.breathe_file_state.items():

            _, docnames = info
            docnames.discard(docname)
            if not docnames:
                toremove.append(filename)

        for filename in toremove:
            del self.app.env.breathe_file_state[filename]


# Setup
# -----

def setup(app):

    path_handler = PathHandler(app.confdir, os.sep, os.path.basename, os.path.join)
    mtimer = MTimer(os.path.getmtime)
    file_state_cache = FileStateCache(mtimer, app)
    parser_factory = DoxygenParserFactory(path_handler, file_state_cache)
    filter_factory = FilterFactory(path_handler)
    item_finder_factory_creator = DoxygenItemFinderFactoryCreator(parser_factory, filter_factory)
    index_parser = parser_factory.create_index_parser()
    finder_factory = FinderFactory(index_parser, item_finder_factory_creator)

    # Assume general build directory is the doctree directory without the last component. We strip
    # off any trailing slashes so that dirname correctly drops the last part. This can be overriden
    # with the breathe_build_directory config variable
    build_dir = os.path.dirname(app.doctreedir.rstrip(os.sep))
    project_info_factory = ProjectInfoFactory(app.srcdir, build_dir, app.confdir, fnmatch.fnmatch)
    node_factory = create_node_factory()
    target_handler_factory = TargetHandlerFactory(node_factory)

    text_renderer = TextRenderer(app)

    directive_factory = DoxygenDirectiveFactory(
        node_factory,
        text_renderer,
        finder_factory,
        project_info_factory,
        filter_factory,
        target_handler_factory,
        parser_factory
        )

    def add_directive(name):
        app.add_directive(name, directive_factory.create_directive_container(name))

    add_directive('doxygenindex')
    add_directive('doxygenstruct')
    add_directive('doxygenenum')
    add_directive('doxygenenumvalue')
    add_directive('doxygentypedef')
    add_directive('doxygenunion')
    add_directive('doxygenclass')
    add_directive('doxygeninterface')
    add_directive('doxygenfile')
    add_directive('doxygennamespace')
    add_directive('doxygengroup')
    add_directive('doxygenvariable')
    add_directive('doxygendefine')
    add_directive('autodoxygenindex')
    add_directive('autodoxygenfile')

    app.add_directive(
        "doxygenfunction",
        directive_factory.create_function_directive_container(),
        )

    app.add_config_value("breathe_projects", {}, True)
    app.add_config_value("breathe_default_project", "", True)
    # Provide reasonable defaults for domain_by_extension mapping. Can be overridden by users.
    app.add_config_value("breathe_domain_by_extension", {'py': 'py'}, True)
    app.add_config_value("breathe_domain_by_file_pattern", {}, True)
    app.add_config_value("breathe_projects_source", {}, True)
    app.add_config_value("breathe_build_directory", '', True)
    app.add_config_value("breathe_default_members", (), True)
    app.add_config_value("breathe_show_define_initializer", False, 'env')
    app.add_config_value("breathe_implementation_filename_extensions", ['.c', '.cc', '.cpp'], True)
    app.add_config_value("breathe_doxygen_config_options", {}, True)
    app.add_config_value("breathe_use_project_refids", False, "env")

    breathe_css = "breathe.css"
    if (os.path.exists(os.path.join(app.confdir, "_static", breathe_css))):
        app.add_stylesheet(breathe_css)

    doxygen_handle = AutoDoxygenProcessHandle(
        path_handler,
        subprocess.check_call,
        write_file,
        project_info_factory
        )

    def doxygen_hook(app):
        doxygen_handle.generate_xml(
            app.config.breathe_projects_source,
            app.config.breathe_doxygen_config_options
        )

    app.connect("builder-inited", directive_factory.get_config_values)

    app.connect("builder-inited", filter_factory.get_config_values)

    app.connect("builder-inited", doxygen_hook)

    app.connect("env-get-outdated", file_state_cache.get_outdated)

    app.connect("env-purge-doc", file_state_cache.purge_doc)
