
from docutils import nodes
from .base import Renderer


class DoxygenTypeSubRenderer(Renderer):

    def render(self, node):

        nodelist = []

        # Process all the compound children
        for compound in node.get_compound():
            context = self.context.create_child_context(compound)
            compound_renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(compound_renderer.render(context.node_stack[0]))

        return nodelist


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

    def visit_desc_content(self, node):
        self.content = node


class CompoundRenderer(Renderer):
    """Base class for CompoundTypeSubRenderer and RefTypeSubRenderer."""

    def __init__(self, compound_parser, render_empty_node, *args):
        self.compound_parser = compound_parser
        self.render_empty_node = render_empty_node
        Renderer.__init__(self, *args)

    def create_doxygen_target(self, node):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), node.refid)
        return self.target_handler.create_target(refid)

    def render_signature(self, node, file_data, doxygen_target):
        # Defer to domains specific directive.
        name, kind = self.get_node_info(node, file_data)
        self.context.directive_args[1] = [self.get_fully_qualified_name()]
        nodes = self.run_domain_directive(kind, self.context.directive_args[1])
        rst_node = nodes[1]

        finder = NodeFinder(rst_node.document)
        rst_node.walk(finder)

        # The cpp domain in Sphinx doesn't support structs at the moment, so change the text from "class "
        # to the correct kind which can be "class " or "struct ".
        finder.declarator[0] = self.node_factory.desc_annotation(kind + ' ', kind + ' ')

        # Check if there is template information and format it as desired
        template_signode = self.create_template_node(file_data.compounddef)
        if template_signode:
            rst_node.insert(0, template_signode)
        rst_node.children[0].insert(0, doxygen_target)
        return nodes, finder.content

    def render(self, node):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(node.refid)

        parent_context = self.context.create_child_context(file_data)
        data_renderer = self.renderer_factory.create_renderer(parent_context)
        rendered_data = data_renderer.render(parent_context.node_stack[0])

        if not rendered_data and not self.render_empty_node:
            return []

        file_data = parent_context.node_stack[0]
        new_context = parent_context.create_child_context(file_data.compounddef)

        nodes, contentnode = self.render_signature(node, file_data, self.create_doxygen_target(node))

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                context = new_context.create_child_context(include)
                renderer = self.renderer_factory.create_renderer(context)
                contentnode.extend(renderer.render(context.node_stack[0]))

        contentnode.extend(rendered_data)
        return nodes


class CompoundTypeSubRenderer(CompoundRenderer):

    def __init__(self, compound_parser, *args):
        CompoundRenderer.__init__(self, compound_parser, True, *args)

    def get_node_info(self, node, file_data):
        return node.name, node.kind


class FileRenderer(CompoundTypeSubRenderer):

    def render_signature(self, node, file_data, doxygen_target):
        # Build targets for linking
        targets = []
        targets.extend(doxygen_target)

        title_signode = self.node_factory.desc_signature()
        title_signode.extend(targets)

        # Set up the title
        name, kind = self.get_node_info(node, file_data)
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
