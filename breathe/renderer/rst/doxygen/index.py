
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

    def create_target(self, refid):

        return self.target_handler.create_target(refid)

    def create_domain_id(self):

        return ""

    def render(self):

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        nodelist = self.create_target(refid)

        domain_id = self.create_domain_id()

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
                    ids=[domain_id, refid]
                    )
            )

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)
        data_renderer = self.renderer_factory.create_renderer(self.data_object, file_data)

        nodelist.extend(data_renderer.render())

        return nodelist


class ClassCompoundTypeSubRenderer(CompoundTypeSubRenderer):

    def create_target(self, refid):

        self.domain_handler.create_class_target(self.data_object)
        return CompoundTypeSubRenderer.create_target(self, refid)

    def create_domain_id(self):

        return self.domain_handler.create_class_id(self.data_object)

