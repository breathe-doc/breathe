
class Renderer(object):

    def __init__(
            self,
            project_info,
            context,
            renderer_factory,
            node_factory,
            state,
            document,
            target_handler,
            domain_directive_factory,
    ):

        self.project_info = project_info
        self.context = context
        self.data_object = context.node_stack[0]
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.target_handler = target_handler
        self.domain_directive_factory = domain_directive_factory

        if self.context.domain == '':
            self.context.domain = self.get_domain()

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
        if type(node) == unicode or node.node_type == "enumvalue":
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
        context = self.context.create_child_context(decl.templateparamlist)
        renderer = self.renderer_factory.create_renderer(context)
        template = 'template '
        nodes = [self.node_factory.desc_annotation(template, template), self.node_factory.Text('<')]
        nodes.extend(renderer.render())
        nodes.append(self.node_factory.Text(">"))
        signode = self.node_factory.desc_signature()
        signode.extend(nodes)
        return signode

    def run_domain_directive(self, kind, names):
        domain_directive = self.renderer_factory.domain_directive_factory.create(
            self.context.domain, [kind, names] + self.context.directive_args[2:])

        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            domain_directive.options['noindex'] = True
        nodes = domain_directive.run()

        # Filter out outer class names if we are rendering a member as a part of a class content.
        signode = nodes[1].children[0]
        if len(names) > 0 and self.context.child:
            signode.children = [n for n in signode.children if not n.tagname == 'desc_addname']
        return nodes


class RenderContext(object):

    def __init__(self, node_stack, mask_factory, directive_args, domain='', child=False):
        self.node_stack = node_stack
        self.mask_factory = mask_factory
        self.directive_args = directive_args
        self.domain = domain
        self.child = child

    def create_child_context(self, data_object):

        node_stack = self.node_stack[:]
        node_stack.insert(0, self.mask_factory.mask(data_object))
        return RenderContext(node_stack, self.mask_factory, self.directive_args, self.domain, True)
