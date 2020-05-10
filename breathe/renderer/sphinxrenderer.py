
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.domains import cpp, c, python
from sphinx.util.nodes import nested_parse_with_titles

try:
    from sphinxcontrib import phpdomain as php
except ImportError:
    php = None

import re
import six
import textwrap


debug_trace_directives = False
debug_trace_doxygen_ids = False
debug_trace_qualification = False
debug_trace_directives_indent = 0


class WithContext(object):
    def __init__(self, parent, context):
        self.context = context
        self.parent = parent
        self.previous = None

    def __enter__(self):
        assert self.previous is None
        self.previous = self.parent.context
        self.parent.set_context(self.context)
        return self

    def __exit__(self, et, ev, bt):
        self.parent.context = self.previous
        self.previous = None


class BaseObject:
    # Use this class as the first base class to make sure the overrides are used.
    # Set the content_callback attribute to a function taking a docutils node.

    def transform_content(self, contentnode):
        super().transform_content(contentnode)
        callback = getattr(self, "breathe_content_callback", None)
        if callback is None:
            return
        callback(contentnode)


# ----------------------------------------------------------------------------

class CPPClassObject(BaseObject, cpp.CPPClassObject):
    pass


class CPPUnionObject(BaseObject, cpp.CPPUnionObject):
    pass


class CPPFunctionObject(BaseObject, cpp.CPPFunctionObject):
    pass


class CPPMemberObject(BaseObject, cpp.CPPMemberObject):
    pass


class CPPTypeObject(BaseObject, cpp.CPPTypeObject):
    pass


class CPPEnumObject(BaseObject, cpp.CPPEnumObject):
    pass


class CPPEnumeratorObject(BaseObject, cpp.CPPEnumeratorObject):
    pass


# ----------------------------------------------------------------------------

class CStructObject(BaseObject, c.CStructObject):
    pass


class CUnionObject(BaseObject, c.CUnionObject):
    pass


class CFunctionObject(BaseObject, c.CFunctionObject):
    pass


class CMemberObject(BaseObject, c.CMemberObject):
    pass


class CTypeObject(BaseObject, c.CTypeObject):
    pass


class CEnumObject(BaseObject, c.CEnumObject):
    pass


class CEnumeratorObject(BaseObject, c.CEnumeratorObject):
    pass


class CMacroObject(BaseObject, c.CMacroObject):
    pass


# ----------------------------------------------------------------------------

class PyFunction(BaseObject, python.PyFunction):
    pass


class PyAttribute(BaseObject, python.PyAttribute):
    pass


class PyClasslike(BaseObject, python.PyClasslike):
    pass


# ----------------------------------------------------------------------------

class DomainDirectiveFactory(object):
    # A mapping from node kinds to domain directives and their names.
    cpp_classes = {
        'variable': (CPPMemberObject, 'var'),
        'class': (CPPClassObject, 'class'),
        'struct': (CPPClassObject, 'struct'),
        'interface': (CPPClassObject, 'class'),
        'function': (CPPFunctionObject, 'function'),
        'friend': (CPPFunctionObject, 'function'),
        'signal': (CPPFunctionObject, 'function'),
        'slot': (CPPFunctionObject, 'function'),
        'enum': (CPPEnumObject, 'enum'),
        'typedef': (CPPTypeObject, 'type'),
        'using': (CPPTypeObject, 'type'),
        'union': (CPPUnionObject, 'union'),
        'namespace': (CPPTypeObject, 'type'),
        'enumvalue': (CPPEnumeratorObject, 'enumerator'),
        'define': (CMacroObject, 'macro'),
    }
    c_classes = {
        'variable': (CMemberObject, 'var'),
        'function': (CFunctionObject, 'function'),
        'define': (CMacroObject, 'macro'),
        'struct': (CStructObject, 'struct'),
        'union': (CUnionObject, 'union'),
        'enum': (CEnumObject, 'enum'),
        'enumvalue': (CEnumeratorObject, 'enumerator'),
        'typedef': (CTypeObject, 'type'),
    }
    python_classes = {
        # TODO: PyFunction is meant for module-level functions
        #       and PyAttribute is meant for class attributes, not module-level variables.
        #       Somehow there should be made a distinction at some point to get the correct
        #       index-text and whatever other things are different.
        'function': (PyFunction, 'function'),
        'variable': (PyAttribute, 'attribute'),
        'class': (PyClasslike, 'class'),
        'namespace': (PyClasslike, 'class'),
    }

    if php is not None:
        php_classes = {
            'function': (php.PhpNamespacelevel, 'function'),
            'class': (php.PhpClasslike, 'class'),
            'attr': (php.PhpClassmember, 'attr'),
            'method': (php.PhpClassmember, 'method'),
            'global': (php.PhpGloballevel, 'global'),
        }

    @staticmethod
    def create(domain, args):
        if domain == 'c':
            cls, name = DomainDirectiveFactory.c_classes[args[0]]
        elif domain == 'py':
            cls, name = DomainDirectiveFactory.python_classes[args[0]]
        elif php is not None and domain == 'php':
            separators = php.separators
            arg_0 = args[0]
            if any([separators['method'] in n for n in args[1]]):
                if any([separators['attr'] in n for n in args[1]]):
                    arg_0 = 'attr'
                else:
                    arg_0 = 'method'
            else:
                if arg_0 in ['variable']:
                    arg_0 = 'global'
            cls, name = DomainDirectiveFactory.php_classes.get(
                arg_0, (php.PhpClasslike, 'class'))
        else:
            domain = 'cpp'
            cls, name = DomainDirectiveFactory.cpp_classes[args[0]]
        # Replace the directive name because domain directives don't know how to handle
        # Breathe's "doxygen" directives.
        assert ':' not in name
        args = [domain + ':' + name] + args[1:]
        return cls(*args)


class NodeFinder(nodes.SparseNodeVisitor):
    """Find the Docutils desc_signature declarator and desc_content nodes."""

    def __init__(self, document):
        nodes.SparseNodeVisitor.__init__(self, document)
        self.declarator = None
        self.content = None

    def visit_desc_signature(self, node):
        # Find the last signature node because it contains the actual declarator
        # rather than "template <...>". In Sphinx 1.4.1 we'll be able to use sphinx_cpp_tagname:
        # https://github.com/michaeljones/breathe/issues/242
        self.declarator = node

    def visit_desc_signature_line(self, node):
        # In sphinx 1.5, there is now a desc_signature_line node within the desc_signature
        # This should be used instead
        self.declarator = node

    def visit_desc_content(self, node):
        self.content = node


def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x


def get_param_decl(param):

    def to_string(node):
        """Convert Doxygen node content to a string."""
        result = []
        if node is not None:
            for p in node.content_:
                value = p.value
                if not isinstance(value, six.text_type):
                    value = value.valueOf_
                result.append(value)
        return ' '.join(result)

    param_type = to_string(param.type_)
    param_name = param.declname if param.declname else param.defname
    if not param_name:
        param_decl = param_type
    else:
        param_decl, number_of_subs = re.subn(r'(\((?:\w+::)*[*&]+)(\))',
                                             r'\g<1>' + param_name + r'\g<2>',
                                             param_type)
        if number_of_subs == 0:
            param_decl = param_type + ' ' + param_name
    if param.array:
        param_decl += param.array
    if param.defval:
        param_decl += ' = ' + to_string(param.defval)

    return param_decl


def get_definition_without_template_args(data_object):
    """
    Return data_object.definition removing any template arguments from the class name in the member
    function.  Otherwise links to classes defined in the same template are not generated correctly.

    For example in 'Result<T> A< B<C> >::f' we want to remove the '< B<C> >' part.
    """
    definition = data_object.definition
    if (len(data_object.bitfield) > 0):
        definition += " : " + data_object.bitfield
    qual_name = '::' + data_object.name
    if definition.endswith(qual_name):
        qual_name_start = len(definition) - len(qual_name)
        pos = qual_name_start - 1
        if definition[pos] == '>':
            bracket_count = 0
            # Iterate back through the characters of the definition counting matching braces and
            # then remove all braces and everything between
            while pos > 0:
                if definition[pos] == '>':
                    bracket_count += 1
                elif definition[pos] == '<':
                    bracket_count -= 1
                    if bracket_count == 0:
                        definition = definition[:pos] + definition[qual_name_start:]
                        break
                pos -= 1
    return definition


class SphinxRenderer(object):
    """
    Doxygen node visitor that converts input into Sphinx/RST representation.
    Each visit method takes a Doxygen node as an argument and returns a list of RST nodes.
    """

    def __init__(
            self,
            project_info,
            renderer_factory,
            node_factory,
            node_stack,
            state,
            document,
            target_handler,
            compound_parser,
            filter_
    ):

        self.project_info = project_info
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.qualification_stack = node_stack
        self.nesting_level = 0
        self.state = state
        self.document = document
        self.target_handler = target_handler
        self.compound_parser = compound_parser
        self.filter_ = filter_
        self.project_refids = project_info.project_refids()
        self.context = None
        self.output_defname = True
        # Nesting level for lists.
        self.nesting_level = 0

    def set_context(self, context):
        self.context = context
        if self.context.domain == '':
            self.context.domain = self.get_domain()

    def get_refid(self, refid):
        if self.project_refids:
            return "%s%s" % (self.project_info.name(), refid)
        else:
            return refid

    def get_domain(self):
        """Returns the domain for the current node."""

        def get_filename(node):
            """Returns the name of a file where the declaration represented by node is located."""
            try:
                return node.location.file
            except AttributeError:
                return None

        node_stack = self.context.node_stack
        node = node_stack[0]
        # An enumvalue node doesn't have location, so use its parent node for detecting
        # the domain instead.
        if isinstance(node, six.string_types) or node.node_type == "enumvalue":
            node = node_stack[1]
        filename = get_filename(node)
        if not filename and node.node_type == "compound":
            file_data = self.compound_parser.parse(node.refid)
            filename = get_filename(file_data.compounddef)
        return self.project_info.domain_for_file(filename) if filename else ''

    def join_nested_name(self, names):
        dom = self.get_domain()
        sep = '::' if not dom or dom == 'cpp' else '.'
        return sep.join(names)

    def run_directive(self, obj_type, names, contentCallback, options={}):
        args = [obj_type, names] + self.context.directive_args[2:]
        directive = DomainDirectiveFactory.create(self.context.domain, args)
        assert issubclass(type(directive), BaseObject)
        directive.breathe_content_callback = contentCallback

        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            directive.options['noindex'] = True
        for k, v in options.items():
            directive.options[k] = v

        if debug_trace_directives:
            global debug_trace_directives_indent
            print("{}Running directive: .. {}:: {}".format(
                '  ' * debug_trace_directives_indent,
                directive.name, ''.join(names)))
            debug_trace_directives_indent += 1

        self.nesting_level += 1
        nodes = directive.run()
        self.nesting_level -= 1

        # TODO: the directive_args seems to be reused between different run_directives
        #       so for now, reset the options.
        #       Remove this once the args are given in a different manner.
        for k, v in options.items():
            del directive.options[k]

        if debug_trace_directives:
            debug_trace_directives_indent -= 1

        # Filter out outer class names if we are rendering a member as a part of a class content.
        rst_node = nodes[1]
        finder = NodeFinder(rst_node.document)
        rst_node.walk(finder)

        signode = finder.declarator

        if len(names) > 0 and self.context.child:
            signode.children = [n for n in signode.children if not n.tagname == 'desc_addname']
        return nodes

    def handle_declaration(self, node, declaration, *, obj_type=None, content_callback=None,
                           display_obj_type=None, declarator_callback=None, options={}):
        if obj_type is None:
            obj_type = node.kind
        if content_callback is None:
            def content(contentnode):
                contentnode.extend(self.description(node))
            content_callback = content
        declaration = declaration.replace('\n', ' ')
        nodes = self.run_directive(obj_type, [declaration], content_callback, options)
        if debug_trace_doxygen_ids:
            ts = self.create_doxygen_target(node)
            if len(ts) == 0:
                print("{}Doxygen target: (none)".format(
                    '  ' * debug_trace_directives_indent))
            else:
                print("{}Doxygen target: {}".format(
                    '  ' * debug_trace_directives_indent, ts[0]['ids']))

        # <desc><desc_signature> and then one or more <desc_signature_line>
        # each <desc_signature_line> has a sphinx_line_type which hints what is present in that line
        assert len(nodes) >= 1
        desc = nodes[1]
        assert desc.__class__.__name__ == "desc"
        assert len(desc) >= 1
        sig = desc[0]
        assert sig.__class__.__name__ == "desc_signature"
        # if may or may not be a multiline signature
        isMultiline = sig.get('is_multiline', False)
        if isMultiline:
            declarator = None
            for line in sig:
                assert line.__class__.__name__ == "desc_signature_line"
                if line.sphinx_line_type == 'declarator':
                    declarator = line
        else:
            declarator = sig
        assert declarator is not None
        if display_obj_type is not None:
            n = declarator[0]
            assert n.__class__.__name__ == "desc_annotation"
            assert n.astext()[-1] == " "
            txt = display_obj_type + ' '
            declarator[0] = self.node_factory.desc_annotation(txt, txt)
        target = self.create_doxygen_target(node)
        declarator.insert(0, target)
        if declarator_callback:
            declarator_callback(declarator)
        return nodes

    def get_qualification(self):
        if self.nesting_level > 0:
            return []

        if debug_trace_qualification:
            def debug_print_node(n):
                return "node_type={}".format(n.node_type)

            global debug_trace_directives_indent
            print("{}{}".format(debug_trace_directives_indent * '  ',
                                debug_print_node(self.qualification_stack[0])))
            debug_trace_directives_indent += 1

        names = []
        for node in self.qualification_stack[1:]:
            if debug_trace_qualification:
                print("{}{}".format(debug_trace_directives_indent * '  ', debug_print_node(node)))
            if node.node_type == 'ref' and len(names) == 0:
                if debug_trace_qualification:
                    print("{}{}".format(debug_trace_directives_indent * '  ', 'res='))
                return []
            if (node.node_type == 'compound' and
                    node.kind not in ['file', 'namespace', 'group']) or \
                    node.node_type == 'memberdef':
                # We skip the 'file' entries because the file name doesn't form part of the
                # qualified name for the identifier. We skip the 'namespace' entries because if we
                # find an object through the namespace 'compound' entry in the index.xml then we'll
                # also have the 'compounddef' entry in our node stack and we'll get it from that. We
                # need the 'compounddef' entry because if we find the object through the 'file'
                # entry in the index.xml file then we need to get the namespace name from somewhere
                names.append(node.name)
            if (node.node_type == 'compounddef' and node.kind == 'namespace'):
                # Nested namespaces include their parent namespace(s) in compoundname. ie,
                # compoundname is 'foo::bar' instead of just 'bar' for namespace 'bar' nested in
                # namespace 'foo'. We need full compoundname because node_stack doesn't necessarily
                # include parent namespaces and we stop here in case it does.
                names.extend(node.compoundname.split('::'))
                break

        names.reverse()

        if debug_trace_qualification:
            print("{}res={}".format(debug_trace_directives_indent * '  ', names))
            debug_trace_directives_indent -= 1
        return names

    # ===================================================================================

    def get_fully_qualified_name(self):

        names = []
        node_stack = self.context.node_stack
        node = node_stack[0]

        # If the node is a namespace, use its name because namespaces are skipped in the main loop.
        if node.node_type == 'compound' and node.kind == 'namespace':
            names.append(node.name)

        for node in node_stack:
            if node.node_type == 'ref' and len(names) == 0:
                return node.valueOf_
            if (node.node_type == 'compound' and
                    node.kind not in ['file', 'namespace', 'group']) or \
                    node.node_type == 'memberdef':
                # We skip the 'file' entries because the file name doesn't form part of the
                # qualified name for the identifier. We skip the 'namespace' entries because if we
                # find an object through the namespace 'compound' entry in the index.xml then we'll
                # also have the 'compounddef' entry in our node stack and we'll get it from that. We
                # need the 'compounddef' entry because if we find the object through the 'file'
                # entry in the index.xml file then we need to get the namespace name from somewhere
                names.insert(0, node.name)
            if (node.node_type == 'compounddef' and node.kind == 'namespace'):
                # Nested namespaces include their parent namespace(s) in compoundname. ie,
                # compoundname is 'foo::bar' instead of just 'bar' for namespace 'bar' nested in
                # namespace 'foo'. We need full compoundname because node_stack doesn't necessarily
                # include parent namespaces and we stop here in case it does.
                names.insert(0, node.compoundname)
                break

        return '::'.join(names)

    def create_template_prefix(self, decl):
        if not decl.templateparamlist:
            return ""
        nodes = self.render(decl.templateparamlist)
        return 'template<' + ''.join(n.astext() for n in nodes) + '>'

    def run_domain_directive(self, kind, names):
        domain_directive = DomainDirectiveFactory.create(
            self.context.domain, [kind, names] + self.context.directive_args[2:])

        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            domain_directive.options['noindex'] = True

        if debug_trace_directives:
            global debug_trace_directives_indent
            print("{}Running directive (old): .. {}:: {}".format(
                '  ' * debug_trace_directives_indent,
                domain_directive.name, ''.join(names)))
            debug_trace_directives_indent += 1

        nodes = domain_directive.run()

        if debug_trace_directives:
            debug_trace_directives_indent -= 1

        # Filter out outer class names if we are rendering a member as a part of a class content.
        rst_node = nodes[1]
        finder = NodeFinder(rst_node.document)
        rst_node.walk(finder)

        signode = finder.declarator

        if len(names) > 0 and self.context.child:
            signode.children = [n for n in signode.children if not n.tagname == 'desc_addname']
        return nodes

    def create_doxygen_target(self, node):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = self.get_refid(node.id)
        return self.target_handler.create_target(refid)

    def title(self, node):

        nodes = []

        # Variable type or function return type
        nodes.extend(self.render_optional(node.type_))
        if nodes:
            nodes.append(self.node_factory.Text(" "))

        nodes.append(self.node_factory.desc_name(text=node.name))

        return nodes

    def description(self, node):
        return self.render_optional(node.briefdescription) + \
               self.render_optional(node.detaileddescription)

    def update_signature(self, signature, obj_type):
        """Update the signature node if necessary, e.g. add qualifiers."""
        prefix = obj_type + ' '
        annotation = self.node_factory.desc_annotation(prefix, prefix)
        if signature[0].tagname != 'desc_name':
            signature[0] = annotation
        else:
            signature.insert(0, annotation)

    def render_declaration(self, node, declaration=None, description=None, **kwargs):
        if declaration is None:
            declaration = self.get_fully_qualified_name()
        obj_type = kwargs.get('objtype', None)
        if obj_type is None:
            obj_type = node.kind
        nodes = self.run_domain_directive(obj_type, [declaration.replace('\n', ' ')])
        if debug_trace_doxygen_ids:
            ts = self.create_doxygen_target(node)
            if len(ts) == 0:
                print("{}Doxygen target (old): (none)".format(
                    '  ' * debug_trace_directives_indent))
            else:
                print("{}Doxygen target (old): {}".format(
                    '  ' * debug_trace_directives_indent, ts[0]['ids']))

        rst_node = nodes[1]
        finder = NodeFinder(rst_node.document)
        rst_node.walk(finder)

        signode = finder.declarator
        contentnode = finder.content

        update_signature = kwargs.get('update_signature', None)
        if update_signature is not None:
            update_signature(signode, obj_type)
        if description is None:
            description = self.description(node)
        signode.insert(0, self.create_doxygen_target(node))
        contentnode.extend(description)
        return nodes

    def visit_unicode(self, node):

        # Skip any nodes that are pure whitespace
        # Probably need a better way to do this as currently we're only doing
        # it skip whitespace between higher-level nodes, but this will also
        # skip any pure whitespace entries in actual content nodes
        #
        # We counter that second issue slightly by allowing through single white spaces
        #
        if node.strip():
            delimiter = None
            if "<linebreak>" in node:
                delimiter = "<linebreak>"
            elif "\n" in node:
                delimiter = "\n"
            if delimiter:
                # Render lines as paragraphs because RST doesn't have line breaks.
                return [self.node_factory.paragraph('', '', self.node_factory.Text(line))
                        for line in node.split(delimiter) if line.strip()]
            return [self.node_factory.Text(node)]
        if node == six.u(" "):
            return [self.node_factory.Text(node)]
        return []

    def visit_doxygen(self, node):

        nodelist = []

        # Process all the compound children
        for compound in node.get_compound():
            nodelist.extend(self.render(compound))

        return nodelist

    def visit_doxygendef(self, node):
        return self.render(node.compounddef)

    def visit_union(self, node):
        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)
        nodeDef = file_data.compounddef

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(nodeDef)

        with WithContext(self, new_context):
            names = self.get_qualification()
            if self.nesting_level == 0:
                names.extend(nodeDef.compoundname.split('::'))
            else:
                names.append(nodeDef.compoundname.split('::')[-1])
            declaration = self.join_nested_name(names)

            def content(contentnode):
                if nodeDef.includes:
                    for include in nodeDef.includes:
                        contentnode.extend(self.render(include,
                                                       new_context.create_child_context(include)))
                rendered_data = self.render(file_data, parent_context)
                contentnode.extend(rendered_data)
            nodes = self.handle_declaration(nodeDef, declaration, content_callback=content)
        return nodes

    def visit_class(self, node):
        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)
        nodeDef = file_data.compounddef

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(nodeDef)

        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            kind = nodeDef.kind
            # Defer to domains specific directive.

            names = self.get_qualification()
            # TODO: this breaks if it's a template specialization
            #       and one of the arguments contain '::'
            if self.nesting_level == 0:
                names.extend(nodeDef.compoundname.split('::'))
            else:
                names.append(nodeDef.compoundname.split('::')[-1])
            decls = [
                self.create_template_prefix(nodeDef),
                self.join_nested_name(names),
            ]
            # add base classes
            if len(nodeDef.basecompoundref) != 0:
                decls.append(':')
            first = True
            for base in nodeDef.basecompoundref:
                if not first:
                    decls.append(',')
                else:
                    first = False
                if base.prot is not None:
                    decls.append(base.prot)
                if base.virt == 'virtual':
                    decls.append('virtual')
                decls.append(base.content_[0].value)
            declaration = ' '.join(decls)

            def content(contentnode):
                if nodeDef.includes:
                    for include in nodeDef.includes:
                        contentnode.extend(self.render(include,
                                                       new_context.create_child_context(include)))
                rendered_data = self.render(file_data, parent_context)
                contentnode.extend(rendered_data)

            assert kind in ('class', 'struct', 'interface')
            display_obj_type = 'interface' if kind == 'interface' else None
            nodes = self.handle_declaration(nodeDef, declaration, content_callback=content,
                                            display_obj_type=display_obj_type)
        return nodes

    def visit_namespace(self, node):
        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)
        nodeDef = file_data.compounddef

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(file_data.compounddef)

        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            names = self.get_qualification()
            if self.nesting_level == 0:
                names.extend(nodeDef.compoundname.split('::'))
            else:
                names.append(nodeDef.compoundname.split('::')[-1])
            declaration = self.join_nested_name(names)

            def content(contentnode):
                if nodeDef.includes:
                    for include in nodeDef.includes:
                        contentnode.extend(self.render(include,
                                                       new_context.create_child_context(include)))
                rendered_data = self.render(file_data, parent_context)
                contentnode.extend(rendered_data)
            display_obj_type = 'namespace' if self.get_domain() != 'py' else 'module'
            nodes = self.handle_declaration(nodeDef, declaration, content_callback=content,
                                            display_obj_type=display_obj_type)
        return nodes

    def visit_compound(self, node, render_empty_node=True, **kwargs):
        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)

        def get_node_info(file_data):
            return node.name, node.kind
        name, kind = kwargs.get('get_node_info', get_node_info)(file_data)
        if kind == 'union':
            dom = self.get_domain()
            assert not dom or dom in ('c', 'cpp')
            return self.visit_union(node)
        elif kind in ('struct', 'class', 'interface'):
            dom = self.get_domain()
            if not dom or dom in ('c', 'cpp', 'py'):
                return self.visit_class(node)
        elif kind == 'namespace':
            dom = self.get_domain()
            if not dom or dom in ('c', 'cpp', 'py'):
                return self.visit_namespace(node)

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(file_data.compounddef)
        rendered_data = self.render(file_data, parent_context)

        if not rendered_data and not render_empty_node:
            return []

        def render_signature(file_data, doxygen_target, name, kind):
            # Defer to domains specific directive.

            templatePrefix = self.create_template_prefix(file_data.compounddef)
            arg = "%s %s" % (templatePrefix, self.get_fully_qualified_name())

            # add base classes
            if kind in ('class', 'struct'):
                bs = []
                for base in file_data.compounddef.basecompoundref:
                    b = []
                    if base.prot is not None:
                        b.append(base.prot)
                    if base.virt == 'virtual':
                        b.append("virtual")
                    b.append(base.content_[0].value)
                    bs.append(" ".join(b))
                if len(bs) != 0:
                    arg += " : "
                    arg += ", ".join(bs)

            self.context.directive_args[1] = [arg]

            nodes = self.run_domain_directive(kind, self.context.directive_args[1])
            rst_node = nodes[1]

            finder = NodeFinder(rst_node.document)
            rst_node.walk(finder)

            if kind in ('interface', 'namespace'):
                # This is not a real C++ declaration type that Sphinx supports,
                # so we hax the replacement of it.
                finder.declarator[0] = self.node_factory.desc_annotation(kind + ' ', kind + ' ')

            rst_node.children[0].insert(0, doxygen_target)
            return nodes, finder.content

        refid = self.get_refid(node.refid)
        render_sig = kwargs.get('render_signature', render_signature)
        with WithContext(self, new_context):
            # Pretend that the signature is being rendered in context of the
            # definition, for proper domain detection
            nodes, contentnode = render_sig(
                    file_data, self.target_handler.create_target(refid),
                    name, kind)

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                contentnode.extend(self.render(include, new_context.create_child_context(include)))

        contentnode.extend(rendered_data)
        return nodes

    def visit_file(self, node):
        def render_signature(file_data, doxygen_target, name, kind):
            # Build targets for linking
            targets = []
            targets.extend(doxygen_target)

            title_signode = self.node_factory.desc_signature()
            title_signode.extend(targets)

            # Set up the title
            title_signode.append(self.node_factory.emphasis(text=kind))
            title_signode.append(self.node_factory.Text(" "))
            title_signode.append(self.node_factory.desc_name(text=name))

            contentnode = self.node_factory.desc_content()

            rst_node = self.node_factory.desc()
            rst_node.document = self.state.document
            rst_node['objtype'] = kind
            rst_node.append(title_signode)
            rst_node.append(contentnode)
            return [rst_node], contentnode
        return self.visit_compound(node, render_signature=render_signature)

    # We store both the identified and appropriate title text here as we want to define the order
    # here and the titles for the SectionDefTypeSubRenderer but we don't want the repetition of
    # having two lists in case they fall out of sync
    #
    # If this list is edited, also change the sections option documentation for
    # the doxygen(auto)file directive in documentation/source/autofile.rst.
    sections = [
        ("user-defined", "User Defined"),
        ("public-type", "Public Types"),
        ("public-func", "Public Functions"),
        ("public-attrib", "Public Members"),
        ("public-slot", "Public Slots"),
        ("signal", "Signals"),
        ("dcop-func", "DCOP Function"),
        ("property", "Property"),
        ("event", "Event"),
        ("public-static-func", "Public Static Functions"),
        ("public-static-attrib", "Public Static Attributes"),
        ("protected-type", "Protected Types"),
        ("protected-func", "Protected Functions"),
        ("protected-attrib", "Protected Attributes"),
        ("protected-slot", "Protected Slots"),
        ("protected-static-func", "Protected Static Functions"),
        ("protected-static-attrib", "Protected Static Attributes"),
        ("package-type", "Package Types"),
        ("package-func", "Package Functions"),
        ("package-attrib", "Package Attributes"),
        ("package-static-func", "Package Static Functions"),
        ("package-static-attrib", "Package Static Attributes"),
        ("private-type", "Private Types"),
        ("private-func", "Private Functions"),
        ("private-attrib", "Private Members"),
        ("private-slot", "Private Slots"),
        ("private-static-func", "Private Static Functions"),
        ("private-static-attrib", "Private Static Attributes"),
        ("friend", "Friends"),
        ("related", "Related"),
        ("define", "Defines"),
        ("prototype", "Prototypes"),
        ("typedef", "Typedefs"),
        ("enum", "Enums"),
        ("func", "Functions"),
        ("var", "Variables"),
    ]

    def visit_compounddef(self, node):

        options = self.context.directive_args[2]
        section_order = None
        if 'sections' in options:
            section_order = {sec: i for i, sec in enumerate(options['sections'].split(' '))}
        nodemap = {}

        def addnode(kind, lam):
            if section_order is None:
                nodemap[len(nodemap)] = lam()
            elif kind in section_order:
                nodemap.setdefault(section_order[kind], []).extend(lam())

        addnode('briefdescription', lambda: self.render_optional(node.briefdescription))
        addnode('detaileddescription', lambda: self.render_optional(node.detaileddescription))

        def render_derivedcompoundref(node):
            if node is None:
                return []
            output = self.render_iterable(node)
            if not output:
                return []
            return [self.node_factory.paragraph(
                '',
                '',
                self.node_factory.Text('Subclassed by '),
                *intersperse(output, self.node_factory.Text(', '))
            )]

        addnode('derivedcompoundref', lambda: render_derivedcompoundref(node.derivedcompoundref))

        section_nodelists = {}

        # Get all sub sections
        for sectiondef in node.sectiondef:
            child_nodes = self.render(sectiondef)
            if not child_nodes:
                # Skip empty section
                continue
            kind = sectiondef.kind
            if section_order is not None and kind not in section_order:
                continue
            rst_node = self.node_factory.container(classes=['breathe-sectiondef'])
            rst_node.document = self.state.document
            rst_node['objtype'] = kind
            rst_node.extend(child_nodes)
            # We store the nodes as a list against the kind in a dictionary as the kind can be
            # 'user-edited' and that can repeat so this allows us to collect all the 'user-edited'
            # entries together
            section_nodelists.setdefault(kind, []).append(rst_node)

        # Order the results in an appropriate manner
        for kind, _ in self.sections:
            addnode(kind, lambda: section_nodelists.get(kind, []))

        # Take care of innerclasses
        addnode('innerclass', lambda: self.render_iterable(node.innerclass))
        addnode('innernamespace', lambda: self.render_iterable(node.innernamespace))

        nodelist = []
        for i, nodes_ in sorted(nodemap.items()):
            nodelist += nodes_

        return nodelist

    section_titles = dict(sections)

    def visit_sectiondef(self, node):

        node_list = []

        node_list.extend(self.render_optional(node.description))

        # Get all the memberdef info
        node_list.extend(self.render_iterable(node.memberdef))

        if node_list:

            text = self.section_titles[node.kind]

            # Override default name for user-defined sections. Use "Unnamed
            # Group" if the user didn't name the section
            # This is different to Doxygen which will track the groups and name
            # them Group1, Group2, Group3, etc.
            if node.kind == "user-defined":
                if node.header:
                    text = node.header
                else:
                    text = "Unnamed Group"

            # Use rubric for the title because, unlike the docutils element "section",
            # it doesn't interfere with the document structure.
            rubric = self.node_factory.rubric(text=text, classes=['breathe-sectiondef-title'])

            return [rubric] + node_list

        return []

    def visit_docreftext(self, node):

        nodelist = self.render_iterable(node.content_)
        nodelist.extend(self.render_iterable(node.para))

        refid = self.get_refid(node.refid)

        nodelist = [
            self.node_factory.pending_xref(
                "",
                reftype="ref",
                refdomain="std",
                refexplicit=True,
                refid=refid,
                reftarget=refid,
                *nodelist
            )
        ]

        return nodelist

    def visit_docheading(self, node):
        """Heading renderer.

        Renders embedded headlines as emphasized text. Different heading levels
        are not supported.
        """
        nodelist = self.render_iterable(node.content_)
        return [self.node_factory.emphasis("", "", *nodelist)]

    def visit_docpara(self, node):
        """
        <para> tags in the Doxygen output tend to contain either text or a single other tag of
        interest. So whilst it looks like we're combined descriptions and program listings and
        other things, in the end we generally only deal with one per para tag. Multiple
        neighbouring instances of these things tend to each be in a separate neighbouring para tag.
        """

        nodelist = self.render_iterable(node.content)
        nodelist.extend(self.render_iterable(node.images))

        if self.project_info.order_parameters_first():
            # Order parameters before simplesects, which mainly are return/warnings/remarks
            definition_nodes = self.render_iterable(node.parameterlist)
            definition_nodes.extend(self.render_iterable(node.simplesects))
        else:
            # Returns, user par's, etc
            definition_nodes = self.render_iterable(node.simplesects)
            # Parameters/Exceptions
            definition_nodes.extend(self.render_iterable(node.parameterlist))

        if definition_nodes:
            definition_list = self.node_factory.definition_list("", *definition_nodes)
            nodelist.append(definition_list)

        return [self.node_factory.paragraph("", "", *nodelist)]

    def visit_docimage(self, node):
        """Output docutils image node using name attribute from xml as the uri"""

        path_to_image = self.project_info.sphinx_abs_path_to_file(
            node.name
        )

        options = {"uri": path_to_image}

        return [self.node_factory.image("", **options)]

    def visit_docurllink(self, node):
        """Url Link Renderer"""
        nodelist = self.render_iterable(node.content_)
        return [self.node_factory.reference("", "", refuri=node.url, *nodelist)]

    def visit_docmarkup(self, node):

        nodelist = self.render_iterable(node.content_)
        creator = self.node_factory.inline
        if node.type_ == "emphasis":
            creator = self.node_factory.emphasis
        elif node.type_ == "computeroutput":
            creator = self.node_factory.literal
        elif node.type_ == "bold":
            creator = self.node_factory.strong
        elif node.type_ == "superscript":
            creator = self.node_factory.superscript
        elif node.type_ == "subscript":
            creator = self.node_factory.subscript
        elif node.type_ == "center":
            print("Warning: does not currently handle 'center' text display")
        elif node.type_ == "small":
            print("Warning: does not currently handle 'small' text display")
        return [creator("", "", *nodelist)]

    def visit_docsect1(self, node):
        return []

    def visit_docsimplesect(self, node):
        """Other Type documentation such as Warning, Note, Returns, etc"""

        nodelist = self.render_iterable(node.para)

        if node.kind == "par":
            text = self.render(node.title)
        else:
            text = [self.node_factory.Text(node.kind.capitalize())]
        title = self.node_factory.strong("", *text)

        term = self.node_factory.term("", "", title)
        definition = self.node_factory.definition("", *nodelist)

        return [self.node_factory.definition_list_item("", term, definition)]

    def visit_doctitle(self, node):
        return self.render_iterable(node.content_)

    def visit_docformula(self, node):

        nodelist = []

        for item in node.content_:

            latex = item.getValue()

            docname = self.state.document.settings.env.docname
            # Strip out the doxygen markup that slips through
            # Either inline
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1]
                nodelist.append(self.node_factory.math(text=latex,
                                                       label=None,
                                                       nowrap=False,
                                                       docname=docname,
                                                       number=None))
            # Else we're multiline
            else:
                if latex.startswith("\\[") and latex.endswith("\\]"):
                    latex = latex[2:-2:]

                nodelist.append(self.node_factory.math_block(text=latex,
                                                             label=None,
                                                             nowrap=False,
                                                             docname=docname,
                                                             number=None))

        return nodelist

    def visit_listing(self, node):

        nodelist = []
        for i, item in enumerate(node.codeline):
            # Put new lines between the lines. There must be a more pythonic way of doing this
            if i:
                nodelist.append(self.node_factory.Text("\n"))
            nodelist.extend(self.render(item))

        # Add blank string at the start otherwise for some reason it renders
        # the pending_xref tags around the kind in plain text
        block = self.node_factory.literal_block(
            "",
            "",
            *nodelist
        )

        return [block]

    def visit_codeline(self, node):
        return self.render_iterable(node.highlight)

    def visit_highlight(self, node):
        return self.render_iterable(node.content_)

    def visit_verbatim(self, node):

        if not node.text.strip().startswith("embed:rst"):

            # Remove trailing new lines. Purely subjective call from viewing results
            text = node.text.rstrip()

            # Handle has a preformatted text
            return [self.node_factory.literal_block(text, text)]

        # do we need to strip leading asterisks?
        # NOTE: We could choose to guess this based on every line starting with '*'.
        #   However This would have a side-effect for any users who have an rst-block
        #   consisting of a simple bullet list.
        #   For now we just look for an extended embed tag
        if node.text.strip().startswith("embed:rst:leading-asterisk"):

            lines = node.text.splitlines()
            # Replace the first * on each line with a blank space
            lines = map(lambda text: text.replace("*", " ", 1), lines)
            node.text = "\n".join(lines)

        # do we need to strip leading ///?
        elif node.text.strip().startswith("embed:rst:leading-slashes"):

            lines = node.text.splitlines()
            # Replace the /// on each line with three blank spaces
            lines = map(lambda text: text.replace("///", "   ", 1), lines)
            node.text = "\n".join(lines)

        # Remove the first line which is "embed:rst[:leading-asterisk]"
        text = "\n".join(node.text.split(u"\n")[1:])

        # Remove starting whitespace
        text = textwrap.dedent(text)

        # Inspired by autodoc.py in Sphinx
        rst = ViewList()
        for line in text.split("\n"):
            rst.append(line, "<breathe>")

        # Parent node for the generated node subtree
        rst_node = self.node_factory.paragraph()
        rst_node.document = self.state.document

        # Generate node subtree
        nested_parse_with_titles(self.state, rst, rst_node)

        return rst_node

    def visit_inc(self, node):

        if node.local == u"yes":
            text = '#include "%s"' % node.content_[0].getValue()
        else:
            text = '#include <%s>' % node.content_[0].getValue()

        return [self.node_factory.emphasis(text=text)]

    def visit_ref(self, node):
        def get_node_info(file_data):
            name = node.content_[0].getValue()
            name = name.rsplit("::", 1)[-1]
            return name, file_data.compounddef.kind
        return self.visit_compound(node, False, get_node_info=get_node_info)

    def visit_doclistitem(self, node):
        """List item renderer. Render all the children depth-first.
        Upon return expand the children node list into a docutils list-item.
        """
        nodelist = self.render_iterable(node.para)
        return [self.node_factory.list_item("", *nodelist)]

    numeral_kind = ['arabic', 'loweralpha', 'lowerroman', 'upperalpha', 'upperroman']

    def render_unordered(self, children):
        nodelist_list = self.node_factory.bullet_list("", *children)

        return [nodelist_list]

    def render_enumerated(self, children, nesting_level):
        nodelist_list = self.node_factory.enumerated_list("", *children)
        idx = nesting_level % len(SphinxRenderer.numeral_kind)
        nodelist_list['enumtype'] = SphinxRenderer.numeral_kind[idx]
        nodelist_list['prefix'] = ''
        nodelist_list['suffix'] = '.'

        return [nodelist_list]

    def visit_doclist(self, node):
        """List renderer

        The specifics of the actual list rendering are handled by the
        decorator around the generic render function.
        Render all the children depth-first. """
        """ Call the wrapped render function. Update the nesting level for the enumerated lists. """
        if node.node_subtype == "itemized":
            val = self.render_iterable(node.listitem)
            return self.render_unordered(children=val)
        elif node.node_subtype == "ordered":
            self.nesting_level += 1
            val = self.render_iterable(node.listitem)
            self.nesting_level -= 1
            return self.render_enumerated(children=val, nesting_level=self.nesting_level)
        return []

    def visit_compoundref(self, node):

        nodelist = self.render_iterable(node.content_)

        refid = self.get_refid(node.refid)

        if refid is not None:
            nodelist = [
                self.node_factory.pending_xref(
                    "",
                    reftype="ref",
                    refdomain="std",
                    refexplicit=True,
                    refid=refid,
                    reftarget=refid,
                    *nodelist
                )
            ]

        return nodelist

    def visit_mixedcontainer(self, node):
        return self.render_optional(node.getValue())

    def visit_description(self, node):
        return self.render_iterable(node.content_)

    def visit_linkedtext(self, node):
        return self.render_iterable(node.content_)

    def visit_function(self, node):
        dom = self.get_domain()
        if not dom or dom in ('c', 'cpp', 'py'):
            names = self.get_qualification()
            names.append(node.get_name())
            name = self.join_nested_name(names)
            if dom == 'py':
                declaration = name + node.get_argsstring()
            else:
                declaration = ' '.join([
                    self.create_template_prefix(node),
                    ''.join(n.astext() for n in self.render(node.get_type())),
                    name,
                    node.get_argsstring()
                ])
            nodes = self.handle_declaration(node, declaration)
            return nodes
        else:
            # Get full function signature for the domain directive.
            param_list = []
            for param in node.param:
                param = self.context.mask_factory.mask(param)
                param_decl = get_param_decl(param)
                param_list.append(param_decl)
            templatePrefix = self.create_template_prefix(node)
            signature = '{0}{1}({2})'.format(
                templatePrefix,
                get_definition_without_template_args(node),
                ', '.join(param_list))

            # Add CV-qualifiers.
            if node.const == 'yes':
                signature += ' const'
            # The doxygen xml output doesn't register 'volatile' as the xml attribute for functions
            # until version 1.8.8 so we also check argsstring:
            #     https://bugzilla.gnome.org/show_bug.cgi?id=733451
            if node.volatile == 'yes' or node.argsstring.endswith('volatile'):
                signature += ' volatile'

            if node.refqual == 'lvalue':
                signature += '&'
            elif node.refqual == 'rvalue':
                signature += '&&'

            # Add `= 0` for pure virtual members.
            if node.virt == 'pure-virtual':
                signature += '= 0'

            self.context.directive_args[1] = [signature]

            nodes = self.run_domain_directive(node.kind, self.context.directive_args[1])
            if debug_trace_doxygen_ids:
                ts = self.create_doxygen_target(node)
                if len(ts) == 0:
                    print("{}Doxygen target (old): (none)".format(
                        '  ' * debug_trace_directives_indent))
                else:
                    print("{}Doxygen target (old): {}".format(
                        '  ' * debug_trace_directives_indent, ts[0]['ids']))

            rst_node = nodes[1]
            finder = NodeFinder(rst_node.document)
            rst_node.walk(finder)

            # Templates have multiple signature nodes in recent versions of Sphinx.
            # Insert Doxygen target into the first signature node.
            rst_node.children[0].insert(0, self.create_doxygen_target(node))

            finder.content.extend(self.description(node))
            return nodes

    def visit_define(self, node):
        declaration = node.name
        if node.param:
            declaration += "("
            for i, parameter in enumerate(node.param):
                if i:
                    declaration += ", "
                declaration += parameter.defname
            declaration += ")"

        # TODO: remove this once Sphinx supports definitions for macros
        def add_definition(declarator):
            if node.initializer and self.project_info.show_define_initializer():
                declarator.extend([self.node_factory.Text(" ")] + self.render(node.initializer))

        return self.handle_declaration(node, declaration, declarator_callback=add_definition)

    def visit_enum(self, node):
        def content(contentnode):
            contentnode.extend(self.description(node))
            values = self.node_factory.emphasis("", self.node_factory.Text("Values:"))
            title = self.node_factory.paragraph("", "", values)
            contentnode += title
            enums = self.render_iterable(node.enumvalue)
            contentnode.extend(enums)
        # TODO: scopedness, Doxygen doesn't seem to generate the xml for that
        # TODO: underlying type, Doxygen doesn't seem to generate the xml for that
        names = self.get_qualification()
        names.append(node.name)
        declaration = self.join_nested_name(names)
        return self.handle_declaration(node, declaration, content_callback=content)

    def visit_enumvalue(self, node):
        declaration = node.name + self.make_initializer(node)
        return self.handle_declaration(node, declaration, obj_type='enumvalue')

    def visit_typedef(self, node):
        type_ = ''.join(n.astext() for n in self.render(node.get_type()))
        names = self.get_qualification()
        names.append(node.get_name())
        name = self.join_nested_name(names)
        if node.definition.startswith('typedef '):
            declaration = ' '.join([type_, name, node.get_argsstring()])
        elif node.definition.startswith('using '):
            # TODO: looks like Doxygen does not generate the proper XML
            #       for the template paramter list
            declaration = self.create_template_prefix(node)
            declaration += ' ' + name + " = " + type_
        return self.handle_declaration(node, declaration)

    def make_initializer(self, node):
        initializer = node.initializer
        signature = []
        if initializer:
            render_nodes = self.render(initializer)
            # Do not append separators for paragraphs.
            if not isinstance(render_nodes[0], nodes.paragraph):
                separator = ' '
                if not render_nodes[0].startswith('='):
                    separator += '= '
                signature.append(self.node_factory.Text(separator))
            signature.extend(render_nodes)
        return ''.join(n.astext() for n in signature)

    def visit_variable(self, node):
        names = self.get_qualification()
        names.append(node.name)
        name = self.join_nested_name(names)
        dom = self.get_domain()
        options = {}
        if dom == 'py':
            declaration = name
            initializer = self.make_initializer(node).strip().lstrip('=').strip()
            if len(initializer) != 0:
                options['value'] = initializer
        else:
            declaration = ' '.join([
                self.create_template_prefix(node),
                ''.join(n.astext() for n in self.render(node.get_type())),
                name,
                node.get_argsstring(),
                self.make_initializer(node)
            ])
        if not dom or dom in ('c', 'cpp', 'py'):
            return self.handle_declaration(node, declaration, options=options)
        else:
            return self.render_declaration(node, declaration)

    def visit_friendclass(self, node):
        dom = self.get_domain()
        assert not dom or dom == 'cpp'

        desc = self.node_factory.desc()
        desc['objtype'] = 'friendclass'
        signode = self.node_factory.desc_signature()
        desc += signode

        typ = ''.join(n.astext() for n in self.render(node.get_type()))
        assert typ in ("friend class", "friend struct")
        signode += self.node_factory.desc_annotation(typ, typ)
        signode += self.node_factory.Text(' ')
        # expr = cpp.CPPExprRole(asCode=False)
        # expr.text = node.name
        # TODO: set most of the things that SphinxRole.__call__ sets
        # signode.extend(expr.run())
        signode += self.node_factory.Text(node.name)
        return [desc]

    def visit_param(self, node):

        nodelist = []

        # Parameter type
        if node.type_:
            type_nodes = self.render(node.type_)
            # Render keywords as annotations for consistency with the cpp domain.
            if len(type_nodes) > 0 and isinstance(type_nodes[0], six.text_type):
                first_node = type_nodes[0]
                for keyword in ['typename', 'class']:
                    if first_node.startswith(keyword + ' '):
                        type_nodes[0] = self.node_factory.Text(first_node.replace(keyword, '', 1))
                        type_nodes.insert(0, self.node_factory.desc_annotation(keyword, keyword))
                        break
            nodelist.extend(type_nodes)

        # Parameter name
        if node.declname:
            if nodelist:
                nodelist.append(self.node_factory.Text(" "))
            nodelist.append(self.node_factory.emphasis(text=node.declname))

        elif self.output_defname and node.defname:
            # We only want to output the definition name (from the cpp file) if the declaration name
            # (from header file) isn't present
            if nodelist:
                nodelist.append(self.node_factory.Text(" "))
            nodelist.append(self.node_factory.emphasis(text=node.defname))

        # array information
        if node.array:
            nodelist.append(self.node_factory.Text(node.array))

        # Default value
        if node.defval:
            nodelist.append(self.node_factory.Text(" = "))
            nodelist.extend(self.render(node.defval))

        return nodelist

    lookup = {
        "param": "Parameters",
        "exception": "Exceptions",
        "templateparam": "Template Parameters",
        "retval": "Return Value",
    }

    def visit_docparamlist(self, node):
        """Parameter/Exception documentation"""

        nodelist = self.render_iterable(node.parameteritem)

        # Fild list entry
        nodelist_list = self.node_factory.bullet_list("", classes=["breatheparameterlist"],
                                                      *nodelist)

        term_text = self.lookup[node.kind]
        term = self.node_factory.term("", "", self.node_factory.strong("", term_text))
        definition = self.node_factory.definition('', nodelist_list)

        return [self.node_factory.definition_list_item('', term, definition)]

    def visit_docparamlistitem(self, node):
        """ Parameter Description Renderer  """

        nodelist = self.render_iterable(node.parameternamelist)

        term = self.node_factory.literal("", "", *nodelist)

        separator = self.node_factory.Text(": ")

        nodelist = self.render_optional(node.parameterdescription)

        # If we have some contents from the parameterdescription then we assume that first entry
        # will be a paragraph object and we reach in and insert the term & separate to the start of
        # that first paragraph so that the description appears inline with the term & separator
        # instead of having it's own paragraph which feels disconnected
        #
        # If there is no description then render then term by itself
        if nodelist:
            nodelist[0].insert(0, term)
            nodelist[0].insert(1, separator)
        else:
            nodelist = [term]

        return [self.node_factory.list_item("", *nodelist)]

    def visit_docparamnamelist(self, node):
        """ Parameter Name Renderer"""
        return self.render_iterable(node.parametername)

    def visit_docparamname(self, node):
        return self.render_iterable(node.content_)

    def visit_templateparamlist(self, node):

        nodelist = []
        self.output_defname = False
        for i, item in enumerate(node.param):
            if i:
                nodelist.append(self.node_factory.Text(", "))
            nodelist.extend(self.render(item))
        self.output_defname = True
        return nodelist

    def visit_unknown(self, node):
        """Visit a node of unknown type."""
        return []

    def dispatch_compound(self, node):
        """Dispatch handling of a compound node to a suitable visit method."""
        if node.kind in ["file", "dir", "page", "example", "group"]:
            return self.visit_file(node)
        return self.visit_compound(node)

    def dispatch_memberdef(self, node):
        """Dispatch handling of a memberdef node to a suitable visit method."""
        if node.kind in ("function", "signal", "slot") or \
                (node.kind == 'friend' and node.argsstring):
            return self.visit_function(node)
        if node.kind == "enum":
            return self.visit_enum(node)
        if node.kind == "typedef":
            return self.visit_typedef(node)
        if node.kind == "variable":
            return self.visit_variable(node)
        if node.kind == "define":
            return self.visit_define(node)
        if node.kind == "friend":
            # note, friend functions should be dispatched further up
            return self.visit_friendclass(node)
        return self.render_declaration(node, update_signature=self.update_signature)

    # A mapping from node types to corresponding dispatch and visit methods.
    # Dispatch methods, as the name suggest, dispatch nodes to appropriate visit
    # methods based on node attributes such as kind.
    methods = {
        "doxygen": visit_doxygen,
        "doxygendef": visit_doxygendef,
        "compound": dispatch_compound,
        "compounddef": visit_compounddef,
        "sectiondef": visit_sectiondef,
        "memberdef": dispatch_memberdef,
        "docreftext": visit_docreftext,
        "docheading": visit_docheading,
        "docpara": visit_docpara,
        "docimage": visit_docimage,
        "docurllink": visit_docurllink,
        "docmarkup": visit_docmarkup,
        "docsect1": visit_docsect1,
        "docsimplesect": visit_docsimplesect,
        "doctitle": visit_doctitle,
        "docformula": visit_docformula,
        "listing": visit_listing,
        "codeline": visit_codeline,
        "highlight": visit_highlight,
        "verbatim": visit_verbatim,
        "inc": visit_inc,
        "ref": visit_ref,
        "doclist": visit_doclist,
        "doclistitem": visit_doclistitem,
        "enumvalue": visit_enumvalue,
        "linkedtext": visit_linkedtext,
        "compoundref": visit_compoundref,
        "mixedcontainer": visit_mixedcontainer,
        "description": visit_description,
        "param": visit_param,
        "docparamlist": visit_docparamlist,
        "docparamlistitem": visit_docparamlistitem,
        "docparamnamelist": visit_docparamnamelist,
        "docparamname": visit_docparamname,
        "templateparamlist": visit_templateparamlist
    }

    def render(self, node, context=None):
        if context is None:
            context = self.context.create_child_context(node)
        with WithContext(self, context):
            result = []
            if not self.filter_.allow(self.context.node_stack):
                pass
            elif isinstance(node, six.string_types):
                result = self.visit_unicode(node)
            else:
                method = SphinxRenderer.methods.get(node.node_type, SphinxRenderer.visit_unknown)
                result = method(self, node)
        return result

    def render_optional(self, node):
        """Render a node that can be None."""
        return self.render(node) if node else []

    def render_iterable(self, iterable):
        output = []
        for entry in iterable:
            output.extend(self.render(entry))
        return output
