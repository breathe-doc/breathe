
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
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser
        self.render_empty_node = render_empty_node

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        return self.target_handler.create_target(refid)

    def render(self, node=None):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        parent_context = self.context.create_child_context(file_data)

        name, kind = self.get_node_info(file_data)

        data_renderer = self.renderer_factory.create_renderer(parent_context)
        rendered_data = data_renderer.render()

        if not rendered_data and not self.render_empty_node:
            return []

        doxygen_target = self.create_doxygen_target()
        file_data = parent_context.node_stack[0]
        new_context = parent_context.create_child_context(file_data.compounddef)

        if node:
            node.children[0].insert(0, doxygen_target)
            contentnode = node.children[1]
        else:
            # Build targets for linking
            targets = []
            targets.extend(self.create_domain_target())
            targets.extend(doxygen_target)

            title_signode = self.node_factory.desc_signature()

            # Check if there is template information and format it as desired
            template_signode = None
            if file_data.compounddef.templateparamlist:
                context = new_context.create_child_context(file_data.compounddef.templateparamlist)
                renderer = self.renderer_factory.create_renderer(context)
                template_nodes = [self.node_factory.Text("template <")]
                template_nodes.extend(renderer.render())
                template_nodes.append(self.node_factory.Text(">"))
                template_signode = self.node_factory.desc_signature()
                # Add targets to the template line if it is there
                template_signode.extend(targets)
                template_signode.extend(template_nodes)
            else:
                # Add targets to title line if there is no template line
                title_signode.extend(targets)

            # Set up the title
            title_signode.append(self.node_factory.emphasis(text=kind))
            title_signode.append(self.node_factory.Text(" "))
            title_signode.append(self.node_factory.desc_name(text=name))

            contentnode = self.node_factory.desc_content()

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                context = new_context.create_child_context(include)
                renderer = self.renderer_factory.create_renderer(context)
                contentnode.extend(renderer.render())

        contentnode.extend(rendered_data)

        if not node:
            node = self.node_factory.desc()
            node.document = self.state.document
            node['objtype'] = kind
            if template_signode:
                node.append(template_signode)
            node.append(title_signode)
            node.append(contentnode)
            return [node]


class CompoundTypeSubRenderer(CompoundRenderer):

    def __init__(self, compound_parser, *args):
        CompoundRenderer.__init__(self, compound_parser, True, *args)

    def get_node_info(self, file_data):
        return self.data_object.name, self.data_object.kind

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []
