
from .base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Process all the compound children
        for compound in self.data_object.get_compound():
            context = self.context.create_child_context(compound)
            compound_renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(compound_renderer.render())

        return nodelist


class CompoundRenderer(Renderer):
    """Base class for CompoundTypeSubRenderer and RefTypeSubRenderer."""

    def __init__(self, compound_parser, render_empty_node, *args):
        self.compound_parser = compound_parser
        self.render_empty_node = render_empty_node
        Renderer.__init__(self, *args)

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        return self.target_handler.create_target(refid)

    def render_signature(self, file_data, doxygen_target):
        # Defer to domains specific directive.
        name, kind = self.get_node_info(file_data)
        self.context.directive_args[1] = [self.get_fully_qualified_name()]
        nodes = self.run_domain_directive(kind, self.context.directive_args[1])
        node = nodes[1]
        signode, contentnode = node.children

        # The cpp domain in Sphinx doesn't support structs at the moment, so change the text from "class "
        # to the correct kind which can be "class " or "struct ".
        signode[0] = self.node_factory.desc_annotation(kind + ' ', kind + ' ')

        # Check if there is template information and format it as desired
        template_signode = self.create_template_node(file_data.compounddef)
        if template_signode:
            node.insert(0, template_signode)
        node.children[0].insert(0, doxygen_target)
        return nodes, contentnode

    def render(self):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        parent_context = self.context.create_child_context(file_data)
        data_renderer = self.renderer_factory.create_renderer(parent_context)
        rendered_data = data_renderer.render()

        if not rendered_data and not self.render_empty_node:
            return []

        file_data = parent_context.node_stack[0]
        new_context = parent_context.create_child_context(file_data.compounddef)

        nodes, contentnode = self.render_signature(file_data, self.create_doxygen_target())

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                context = new_context.create_child_context(include)
                renderer = self.renderer_factory.create_renderer(context)
                contentnode.extend(renderer.render())

        contentnode.extend(rendered_data)
        return nodes


class CompoundTypeSubRenderer(CompoundRenderer):

    def __init__(self, compound_parser, *args):
        CompoundRenderer.__init__(self, compound_parser, True, *args)

    def get_node_info(self, file_data):
        return self.data_object.name, self.data_object.kind


class FileRenderer(CompoundTypeSubRenderer):

    def render_signature(self, file_data, doxygen_target):
        # Build targets for linking
        targets = []
        targets.extend(doxygen_target)

        title_signode = self.node_factory.desc_signature()
        title_signode.extend(targets)

        # Set up the title
        name, kind = self.get_node_info(file_data)
        title_signode.append(self.node_factory.emphasis(text=kind))
        title_signode.append(self.node_factory.Text(" "))
        title_signode.append(self.node_factory.desc_name(text=name))

        contentnode = self.node_factory.desc_content()

        node = self.node_factory.desc()
        node.document = self.state.document
        node['objtype'] = kind
        node.append(title_signode)
        node.append(contentnode)
        return [node], contentnode
