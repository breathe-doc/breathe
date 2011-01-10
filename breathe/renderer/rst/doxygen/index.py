
from breathe.renderer.rst.doxygen.base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        if self.continue_rendering():
            nodelist = []

            # Process all the compound children
            for compound in self.data_object.get_compound():
                compound_renderer = self.renderer_factory.create_renderer(compound)
                nodelist.extend(compound_renderer.render())

            return nodelist
        return []


class CompoundTypeSubRenderer(Renderer):

    def __init__(self, compound_parser, *args):
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser

    def render(self):
         
        if self.continue_rendering():
            refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
            nodelist = self.target_handler.create_target(refid)

            # Set up the title and a reference for it (refid)
            kind = self.node_factory.emphasis(text=self.data_object.kind)
            name = self.node_factory.strong(text=self.data_object.name)
            nodelist.append(
                    self.node_factory.paragraph(
                        "",
                        "",
                        kind,
                        self.node_factory.Text(" "),
                        name,
                        ids=[refid]
                        )
                )

            # Read in the corresponding xml file and process
            file_data = self.compound_parser.parse(self.data_object.refid)
            data_renderer = self.renderer_factory.create_renderer(file_data)

            nodelist.extend(data_renderer.render())

            return nodelist
        return []


