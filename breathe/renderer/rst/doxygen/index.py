
from breathe.renderer.rst.doxygen.base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Process all the compound children
        for compound in self.data_object.get_compound():
            compound_renderer = self.renderer_factory.create_renderer(self.data_object, compound)
            nodelist.extend(compound_renderer.render())

        return nodelist


class CompoundTypeSubRenderer(Renderer):

    def __init__(self, compound_parser, *args):
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        return self.target_handler.create_target(refid)

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []


    def render(self):

        # Build targets for linking
        signode = self.node_factory.desc_signature()
        signode.extend(self.create_domain_target())
        signode.extend(self.create_doxygen_target())

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        # Check if there is template information and format it as desired
        if file_data.compounddef.templateparamlist:
            renderer = self.renderer_factory.create_renderer(
                    file_data.compounddef,
                    file_data.compounddef.templateparamlist
                    )
            template_nodes = []
            template_nodes.append(self.node_factory.Text("template <"))
            template_nodes.extend(renderer.render())
            template_nodes.append(self.node_factory.Text(">"))
            signode.append(self.node_factory.line("", *template_nodes))

        # Set up the title and a reference for it (refid)
        signode.append(self.node_factory.emphasis(text=self.data_object.kind))
        signode.append(self.node_factory.Text(" "))
        signode.append(self.node_factory.desc_name(text=self.data_object.name))

        contentnode = self.node_factory.desc_content()

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                renderer = self.renderer_factory.create_renderer(
                        file_data.compounddef,
                        include
                        )
                contentnode.extend(renderer.render())

        data_renderer = self.renderer_factory.create_renderer(self.data_object, file_data)
        contentnode.extend(data_renderer.render())

        node = self.node_factory.desc()
        node.document = self.state.document
        node['objtype'] = self.data_object.kind
        node.append(signode)
        node.append(contentnode)

        return [node]


class ClassCompoundTypeSubRenderer(CompoundTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_class_target(self.data_object)

