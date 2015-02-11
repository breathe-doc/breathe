
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
        # An enumvalue node doesn't have location, so use its parent node for detecting the domain instead.
        if node.node_type == "enumvalue":
            node = node_stack[1]
        filename = get_filename(node)
        if not filename and node.node_type == "compound":
            file_data = self.compound_parser.parse(node.refid)
            filename = get_filename(file_data.compounddef)
        return self.project_info.domain_for_file(filename)

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

        # Check if there is template information and format it as desired
        template_signode = self.create_template_node(file_data.compounddef)

        # Defer to domains specific directive.
        domain = self.get_domain()
        # TODO: replace domain_directive_factories dictionary with an object
        domain_directive = self.renderer_factory.domain_directive_factories[domain].create(self.context.directive_args)
        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            domain_directive.options['noindex'] = True
        nodes = domain_directive.run()
        node = nodes[1]

        signode, contentnode = node.children
        # The cpp domain in Sphinx doesn't support structs at the moment, so change the text from "class "
        # to the correct kind which can be "class " or "struct ".
        signode[0].children[0] = self.node_factory.Text(kind + " ")
        if template_signode:
            node.insert(0, template_signode)
        node.children[0].insert(0, doxygen_target)

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

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []
