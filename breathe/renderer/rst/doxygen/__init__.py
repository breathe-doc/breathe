
from breathe.renderer.rst.doxygen.base import Renderer
from breathe.renderer.rst.doxygen import index as indexrenderer
from breathe.renderer.rst.doxygen import compound as compoundrenderer

from breathe.parser.doxygen import index, compound, compoundsuper


class UnicodeRenderer(Renderer):

    def render(self):

        return [self.node_factory.Text(self.data_object)]

class DoxygenToRstRendererFactory(object):

    def __init__(self, renderers, node_factory, project_info, document):

        self.node_factory = node_factory
        self.project_info = project_info
        self.renderers = renderers
        self.document = document

    def create_renderer(self, data_object):

        Renderer = self.renderers[data_object.__class__]

        if data_object.__class__ == compound.docMarkupTypeSub:

            creator = self.node_factory.inline
            if data_object.type_ == "emphasis":
                creator = self.node_factory.emphasis
            elif data_object.type_ == "computeroutput":
                creator = self.node_factory.literal
            elif data_object.type_ == "bold":
                creator = self.node_factory.strong
            elif data_object.type_ == "superscript":
                creator = self.node_factory.superscript
            elif data_object.type_ == "subscript":
                creator = self.node_factory.subscript
            elif data_object.type_ == "center":
                print "Warning: does not currently handle 'center' text display"
            elif data_object.type_ == "small":
                print "Warning: does not currently handle 'small' text display"

            return Renderer(
                    creator,
                    self.project_info,
                    data_object,
                    self,
                    self.node_factory,
                    self.document
                    )

        if data_object.__class__ == compound.memberdefTypeSub:

            if data_object.kind == "function":
                Renderer = compoundrenderer.FuncMemberDefTypeSubRenderer
            elif data_object.kind == "enum":
                Renderer = compoundrenderer.EnumMemberDefTypeSubRenderer
            elif data_object.kind == "typedef":
                Renderer = compoundrenderer.TypedefMemberDefTypeSubRenderer
            elif data_object.kind == "variable":
                Renderer = compoundrenderer.VariableMemberDefTypeSubRenderer

        if data_object.__class__ == compound.docSimpleSectTypeSub:
            if data_object.kind == "par":
                Renderer = compoundrenderer.ParDocSimpleSectTypeSubRenderer

        return Renderer(
                self.project_info,
                data_object,
                self,
                self.node_factory,
                self.document
                )


class CreateCompoundTypeSubRenderer(object):

    def __init__(self, parser_factory):

        self.parser_factory = parser_factory

    def __call__(self, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexrenderer.CompoundTypeSubRenderer(compound_parser, project_info, *args)


class DoxygenToRstRendererFactoryCreator(object):

    def __init__(self, node_factory, parser_factory):

        self.node_factory = node_factory
        self.parser_factory = parser_factory

    def create_factory(self, project_info, document):

        renderers = {
            index.DoxygenTypeSub : indexrenderer.DoxygenTypeSubRenderer,
            index.CompoundTypeSub : CreateCompoundTypeSubRenderer(self.parser_factory),
            compound.DoxygenTypeSub : compoundrenderer.DoxygenTypeSubRenderer,
            compound.compounddefTypeSub : compoundrenderer.CompoundDefTypeSubRenderer,
            compound.sectiondefTypeSub : compoundrenderer.SectionDefTypeSubRenderer,
            compound.memberdefTypeSub : compoundrenderer.MemberDefTypeSubRenderer,
            compound.enumvalueTypeSub : compoundrenderer.EnumvalueTypeSubRenderer,
            compound.linkedTextTypeSub : compoundrenderer.LinkedTextTypeSubRenderer,
            compound.descriptionTypeSub : compoundrenderer.DescriptionTypeSubRenderer,
            compound.paramTypeSub : compoundrenderer.ParamTypeSubRenderer,
            compound.docRefTextTypeSub : compoundrenderer.DocRefTextTypeSubRenderer,
            compound.docParaTypeSub : compoundrenderer.DocParaTypeSubRenderer,
            compound.docMarkupTypeSub : compoundrenderer.DocMarkupTypeSubRenderer,
            compound.docParamListTypeSub : compoundrenderer.DocParamListTypeSubRenderer,
            compound.docParamListItemSub : compoundrenderer.DocParamListItemSubRenderer,
            compound.docParamNameListSub : compoundrenderer.DocParamNameListSubRenderer,
            compound.docParamNameSub : compoundrenderer.DocParamNameSubRenderer,
            compound.docSect1TypeSub : compoundrenderer.DocSect1TypeSubRenderer,
            compound.docSimpleSectTypeSub : compoundrenderer.DocSimpleSectTypeSubRenderer,
            compound.docTitleTypeSub : compoundrenderer.DocTitleTypeSubRenderer,
            compoundsuper.MixedContainer : compoundrenderer.MixedContainerRenderer,
            unicode : UnicodeRenderer,
            }

        return DoxygenToRstRendererFactory(renderers, self.node_factory, project_info, document)


