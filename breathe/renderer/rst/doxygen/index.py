
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
        nodelist = self.create_domain_target()
        nodelist.extend(self.create_doxygen_target())

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        lines = []

        # Check if there is template information and format it as desired
        if file_data.compounddef.templateparamlist:
            renderer = self.renderer_factory.create_renderer(
                    file_data.compounddef,
                    file_data.compounddef.templateparamlist
                    )
            template = [
                    self.node_factory.Text("template < ")
                ]
            template.extend(renderer.render())
            template.append(self.node_factory.Text(" >"))
            lines.append(self.node_factory.line("", *template))

        # Set up the title and a reference for it (refid)
        kind = self.node_factory.emphasis(text=self.data_object.kind)
        name = self.node_factory.strong(text=self.data_object.name)

        # Add blank string at the start otherwise for some reason it renders
        # the emphasis tags around the kind in plain text
        lines.append(
                self.node_factory.line(
                    "", 
                    self.node_factory.Text(""),
                    kind,
                    self.node_factory.Text(" "),
                    name
                    )
                )


        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                renderer = self.renderer_factory.create_renderer(
                        file_data.compounddef,
                        include
                        )
                result = renderer.render()
                if result:
                    lines.append(
                            self.node_factory.line(
                                "",
                                self.node_factory.Text(""),
                                *result
                                )
                            )

        nodelist.append(
                self.node_factory.line_block(
                    "",
                    *lines
                    )
                )

        data_renderer = self.renderer_factory.create_renderer(self.data_object, file_data)
        nodelist.extend(data_renderer.render())

        return nodelist


class ClassCompoundTypeSubRenderer(CompoundTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_class_target(self.data_object)

