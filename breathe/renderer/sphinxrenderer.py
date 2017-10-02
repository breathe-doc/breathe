
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.domains import cpp, c, python

import re
import six
import textwrap


class DomainDirectiveFactory(object):
    # A mapping from node kinds to cpp domain classes and directive names.
    cpp_classes = {
        'class': (cpp.CPPClassObject, 'class'),
        'struct': (cpp.CPPClassObject, 'class'),
        'interface': (cpp.CPPClassObject, 'interface'),
        'function': (cpp.CPPFunctionObject, 'function'),
        'friend': (cpp.CPPFunctionObject, 'function'),
        'slot': (cpp.CPPFunctionObject, 'function'),
        'enum': (cpp.CPPTypeObject, 'type'),
        'typedef': (cpp.CPPTypeObject, 'type'),
        'using': (cpp.CPPTypeObject, 'type'),
        'union': (cpp.CPPTypeObject, 'type'),
        'namespace': (cpp.CPPTypeObject, 'type'),
        'enumvalue': (cpp.CPPEnumeratorObject, 'enumerator'),
        'define': (c.CObject, 'macro')
    }

    python_classes = {
        'function': (python.PyModulelevel, 'function'),
        'variable': (python.PyClassmember, 'attribute')
    }

    @staticmethod
    def fix_python_signature(sig):
        def_ = 'def '
        if sig.startswith(def_):
            sig = sig[len(def_):]
        # Doxygen uses an invalid separator ('::') in Python signatures. Replace them with '.'.
        return sig.replace('::', '.')

    @staticmethod
    def create(domain, args):
        if domain == 'c':
            return c.CObject(*args)
        if domain == 'py':
            cls, name = DomainDirectiveFactory.python_classes.get(
                args[0], (python.PyClasslike, 'class'))
            args[1] = [DomainDirectiveFactory.fix_python_signature(n) for n in args[1]]
        else:
            cls, name = DomainDirectiveFactory.cpp_classes.get(
                args[0], (cpp.CPPMemberObject, 'member'))
        # Replace the directive name because domain directives don't know how to handle
        # Breathe's "doxygen" directives.
        args = [name] + args[1:]
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
        param_decl, number_of_subs = re.subn(r'(\([*&]+)(\))', r'\1' + param_name + r'\2',
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
            state,
            document,
            target_handler,
            compound_parser,
            filter_
    ):

        self.project_info = project_info
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
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

    def get_fully_qualified_name(self):

        names = []
        node_stack = self.context.node_stack
        node = node_stack[0]
        if node.node_type == 'enumvalue':
            names.append(node.name)
            # Skip the name of the containing enum because it is not a part of the
            # fully qualified name.
            node_stack = node_stack[2:]

        # If the node is a namespace, use its name because namespaces are skipped in the main loop.
        if node.node_type == 'compound' and node.kind == 'namespace':
            names.append(node.name)

        for node in node_stack:
            if node.node_type == 'ref' and len(names) == 0:
                return node.valueOf_
            if (node.node_type == 'compound' and node.kind not in ['file', 'namespace']) or \
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

    def create_template_node(self, decl):
        """Creates a node for the ``template <...>`` part of the declaration."""
        if not decl.templateparamlist:
            return None
        template = 'template '
        nodes = [self.node_factory.desc_annotation(template, template), self.node_factory.Text('<')]
        nodes.extend(self.render(decl.templateparamlist))
        nodes.append(self.node_factory.Text(">"))
        signode = self.node_factory.desc_signature()
        signode.extend(nodes)
        return signode

    def run_domain_directive(self, kind, names):
        domain_directive = DomainDirectiveFactory.create(
            self.context.domain, [kind, names] + self.context.directive_args[2:])

        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            domain_directive.options['noindex'] = True
        nodes = domain_directive.run()

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
            if "<linebreak>" not in node:
                return [self.node_factory.Text(node)]
            # Render lines as paragraphs because RST doesn't have line breaks.
            return [self.node_factory.paragraph('', '', self.node_factory.Text(line))
                    for line in node.split("<linebreak>")]
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

    def visit_compound(self, node, render_empty_node=True, **kwargs):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)

        rendered_data = self.render(file_data)

        if not rendered_data and not render_empty_node:
            return []

        def get_node_info(file_data):
            return node.name, node.kind
        name, kind = kwargs.get('get_node_info', get_node_info)(file_data)

        def render_signature(file_data, doxygen_target, name, kind):
            # Defer to domains specific directive.
            self.context.directive_args[1] = [self.get_fully_qualified_name()]
            nodes = self.run_domain_directive(kind, self.context.directive_args[1])
            rst_node = nodes[1]

            finder = NodeFinder(rst_node.document)
            rst_node.walk(finder)

            # The cpp domain in Sphinx doesn't support structs at the moment, so change the text
            # from "class " to the correct kind which can be "class " or "struct ".
            finder.declarator[0] = self.node_factory.desc_annotation(kind + ' ', kind + ' ')

            # Check if there is template information and format it as desired
            template_signode = self.create_template_node(file_data.compounddef)
            if template_signode:
                rst_node.insert(0, template_signode)
            rst_node.children[0].insert(0, doxygen_target)
            return nodes, finder.content

        refid = self.get_refid(node.refid)
        render_sig = kwargs.get('render_signature', render_signature)
        nodes, contentnode = render_sig(file_data, self.target_handler.create_target(refid),
                                        name, kind)

        parent_context = self.context.create_child_context(file_data)
        new_context = parent_context.create_child_context(file_data.compounddef)
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
    sections = [
        ("user-defined", "User Defined"),
        ("public-type", "Public Types"),
        ("public-func", "Public Functions"),
        ("public-attrib", "Public Members"),
        ("public-slot", "Public Slots"),
        ("signal", "Signal"),
        ("dcop-func",  "DCOP Function"),
        ("property",  "Property"),
        ("event",  "Event"),
        ("public-static-func", "Public Static Functions"),
        ("public-static-attrib", "Public Static Attributes"),
        ("protected-type",  "Protected Types"),
        ("protected-func",  "Protected Functions"),
        ("protected-attrib",  "Protected Attributes"),
        ("protected-slot",  "Protected Slots"),
        ("protected-static-func",  "Protected Static Functions"),
        ("protected-static-attrib",  "Protected Static Attributes"),
        ("package-type",  "Package Types"),
        ("package-func", "Package Functions"),
        ("package-attrib", "Package Attributes"),
        ("package-static-func", "Package Static Functions"),
        ("package-static-attrib", "Package Static Attributes"),
        ("private-type", "Private Types"),
        ("private-func", "Private Functions"),
        ("private-attrib", "Private Members"),
        ("private-slot",  "Private Slots"),
        ("private-static-func", "Private Static Functions"),
        ("private-static-attrib",  "Private Static Attributes"),
        ("friend",  "Friends"),
        ("related",  "Related"),
        ("define",  "Defines"),
        ("prototype",  "Prototypes"),
        ("typedef",  "Typedefs"),
        ("enum",  "Enums"),
        ("func",  "Functions"),
        ("var",  "Variables"),
    ]

    def visit_compounddef(self, node):

        nodelist = []

        nodelist.extend(self.render_optional(node.briefdescription))
        nodelist.extend(self.render_optional(node.detaileddescription))

        def render_list(node, prefix):
            if node is None:
                return
            output = self.render_iterable(node)
            if not output:
                return
            nodelist.append(
                self.node_factory.paragraph(
                    '',
                    '',
                    self.node_factory.Text(prefix),
                    *intersperse(output, self.node_factory.Text(', '))
                )
            )
        render_list(node.basecompoundref, 'Inherits from ')
        render_list(node.derivedcompoundref, 'Subclassed by ')

        section_nodelists = {}

        # Get all sub sections
        for sectiondef in node.sectiondef:
            child_nodes = self.render(sectiondef)
            if not child_nodes:
                # Skip empty section
                continue
            kind = sectiondef.kind
            rst_node = self.node_factory.container(classes=['breathe-sectiondef'])
            rst_node.document = self.state.document
            rst_node['objtype'] = kind
            rst_node.extend(child_nodes)
            # We store the nodes as a list against the kind in a dictionary as the kind can be
            # 'user-edited' and that can repeat so this allows us to collect all the 'user-edited'
            # entries together
            nodes = section_nodelists.setdefault(kind, [])
            nodes += [rst_node]

        # Order the results in an appropriate manner
        for kind, _ in self.sections:
            nodelist.extend(section_nodelists.get(kind, []))

        # Take care of innerclasses
        nodelist.extend(self.render_iterable(node.innerclass))
        nodelist.extend(self.render_iterable(node.innernamespace))

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

            # Somewhat hacky if statements to strip out the doxygen markup that slips through

            rst_node = None

            # Either inline
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1]

                # If we're inline create a math node like the :math: role
                rst_node = self.node_factory.math()
            else:
                # Else we're multiline
                rst_node = self.node_factory.displaymath()

            # Or multiline
            if latex.startswith("\[") and latex.endswith("\]"):
                latex = latex[2:-2:]

            # Here we steal the core of the mathbase "math" directive handling code from:
            #    sphinx.ext.mathbase
            rst_node["latex"] = latex

            # Required parameters which we don't have values for
            rst_node["label"] = None
            rst_node["nowrap"] = False
            rst_node["docname"] = self.state.document.settings.env.docname
            rst_node["number"] = None

            nodelist.append(rst_node)

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
        self.state.nested_parse(rst, 0, rst_node)

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
        if node.node_subtype is "itemized":
            val = self.render_iterable(node.listitem)
            return self.render_unordered(children=val)
        elif node.node_subtype is "ordered":
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
        # Get full function signature for the domain directive.
        param_list = []
        for param in node.param:
            param = self.context.mask_factory.mask(param)
            param_decl = get_param_decl(param)
            param_list.append(param_decl)
        signature = '{0}({1})'.format(get_definition_without_template_args(node),
                                      ', '.join(param_list))

        # Add CV-qualifiers.
        if node.const == 'yes':
            signature += ' const'
        # The doxygen xml output doesn't register 'volatile' as the xml attribute for functions
        # until version 1.8.8 so we also check argsstring:
        #     https://bugzilla.gnome.org/show_bug.cgi?id=733451
        if node.volatile == 'yes' or node.argsstring.endswith('volatile'):
            signature += ' volatile'

        self.context.directive_args[1] = [signature]

        nodes = self.run_domain_directive(node.kind, self.context.directive_args[1])
        rst_node = nodes[1]
        finder = NodeFinder(rst_node.document)
        rst_node.walk(finder)

        # Templates have multiple signature nodes in recent versions of Sphinx.
        # Insert Doxygen target into the first signature node.
        rst_node.children[0].insert(0, self.create_doxygen_target(node))

        # Add `= 0` for pure virtual members.
        if node.virt == 'pure-virtual':
            finder.declarator.append(self.node_factory.Text(' = 0'))

        finder.content.extend(self.description(node))

        template_node = self.create_template_node(node)
        if template_node:
            rst_node.insert(0, template_node)
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

        def update_define_signature(signature, obj_type):
            if node.initializer and self.project_info.show_define_initializer():
                signature.extend([self.node_factory.Text(" ")] + self.render(node.initializer))

        return self.render_declaration(node, declaration, update_signature=update_define_signature)

    def visit_enum(self, node):
        # Sphinx requires a name to be a valid identifier, so replace anonymous enum name of the
        # form @id generated by Doxygen with "anonymous".
        name = self.get_fully_qualified_name()
        declaration = name.replace("@", "__anonymous") if node.name.startswith("@") else name

        description_nodes = self.description(node)
        name = self.node_factory.emphasis("", self.node_factory.Text("Values:"))
        title = self.node_factory.paragraph("", "", name)
        description_nodes.append(title)
        enums = self.render_iterable(node.enumvalue)
        description_nodes.extend(enums)

        def update_signature(signature, obj_type):
            first_node = signature.children[0]
            if isinstance(first_node, self.node_factory.desc_annotation):
                # Replace "type" with "enum" in the signature. This is needed because older
                # versions of Sphinx cpp domain didn't have an enum directive and we use a type
                # directive instead.
                first_node[0] = self.node_factory.Text("enum ")
            else:
                # If there is no "type" annotation, insert "enum".
                first_node.insert(0, self.node_factory.desc_annotation("enum ", "enum "))
            if node.name.startswith("@"):
                signature.children[1][0] = self.node_factory.strong(text="[anonymous]")

        return self.render_declaration(node, declaration, description_nodes,
                                       update_signature=update_signature)

    def visit_typedef(self, node):
        declaration = get_definition_without_template_args(node)
        typedef = "typedef "
        using = "using "
        obj_type = node.kind
        if declaration.startswith(typedef):
            declaration = declaration[len(typedef):]
        elif declaration.startswith(using):
            declaration = declaration[len(using):]
            obj_type = "using"

        def update_signature(signature, obj_type):
            """Update the signature node if necessary, e.g. add qualifiers."""
            prefix = obj_type + ' '
            annotation = self.node_factory.desc_annotation(prefix, prefix)
            if signature[0].tagname != 'desc_annotation':
                signature.insert(0, annotation)
            else:
                signature[0] = annotation

        return self.render_declaration(node, declaration, objtype=obj_type,
                                       update_signature=update_signature)

    def update_signature_with_initializer(self, signature, node):
        initializer = node.initializer
        if initializer:
            nodes = self.render(initializer)
            separator = ' '
            if not nodes[0].startswith('='):
                separator += '= '
            signature.append(self.node_factory.Text(separator))
            signature.extend(nodes)

    def visit_variable(self, node):
        declaration = get_definition_without_template_args(node)
        enum = 'enum '
        if declaration.startswith(enum):
            declaration = declaration[len(enum):]

        def update_signature(signature, obj_type):
            self.update_signature_with_initializer(signature, node)
        return self.render_declaration(node, declaration, update_signature=update_signature)

    def visit_enumvalue(self, node):
        def update_signature(signature, obj_type):
            # Remove "class" from the signature. This is needed because Sphinx cpp domain doesn't
            # have an enum value directive and we use a class directive instead.
            signature.children.pop(0)
            self.update_signature_with_initializer(signature, node)
        return self.render_declaration(node, objtype='enumvalue', update_signature=update_signature)

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
        if node.kind in ("function", "slot") or \
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
        saved_context = self.context
        self.set_context(context if context else self.context.create_child_context(node))
        result = []
        if not self.filter_.allow(self.context.node_stack):
            pass
        elif isinstance(node, six.string_types):
            result = self.visit_unicode(node)
        else:
            method = SphinxRenderer.methods.get(node.node_type, SphinxRenderer.visit_unknown)
            result = method(self, node)
        self.context = saved_context
        return result

    def render_optional(self, node):
        """Render a node that can be None."""
        return self.render(node) if node else []

    def render_iterable(self, iterable):
        output = []
        for entry in iterable:
            output.extend(self.render(entry))
        return output
