
from breathe.renderer.rst.doxygen.base import Renderer
from breathe.renderer.rst.doxygen import index as indexrenderer
from breathe.renderer.rst.doxygen import compound as compoundrenderer

from breathe.parser.doxygen import index, compound, compoundsuper

class RstContentCreator(object):

    def __init__(self, list_type, dedent):

        self.list_type = list_type
        self.dedent = dedent

    def __call__(self, text):

        # Remove the first line
        text = "\n".join(text.split(u"\n")[1:])

        # Remove starting whitespace
        text = self.dedent(text)

        # Inspired by autodoc.py in Sphinx
        result = self.list_type()
        for line in text.split("\n"):
            result.append(line, "<breathe>")

        return result

class UnicodeRenderer(Renderer):

    def render(self):

        return [self.node_factory.Text(self.data_object)]

class NullRenderer(Renderer):

    def __init__(self):
        pass

    def render(self):
        return []

class DoxygenToRstRendererFactory(object):

    def __init__(
            self,
            renderers,
            node_factory,
            project_info,
            state,
            document,
            domain_handler_factory,
            domain_handler,
            rst_content_creator,
            member_filter,
            target_handler
            ):

        self.node_factory = node_factory
        self.project_info = project_info
        self.renderers = renderers
        self.state = state
        self.document = document
        self.domain_handler_factory = domain_handler_factory
        self.domain_handler = domain_handler
        self.rst_content_creator = rst_content_creator
        self.member_filter = member_filter
        self.target_handler = target_handler

    def create_renderer(self, data_object):

        renderer_factory = self

        location = ""

        try:
            location = data_object.location.file
        except AttributeError:
            # No location attribute
            pass

        renderer_factory = self.create_domain_renderer_factory(location)

        return self.create_renderer_with_factory(
                data_object,
                renderer_factory,
                renderer_factory.domain_handler
                )

    def create_renderer_with_factory(
            self,
            data_object,
            renderer_factory,
            domain_handler
            ):

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
                    renderer_factory,
                    self.node_factory,
                    self.state,
                    self.document,
                    domain_handler,
                    self.target_handler
                    )

        if data_object.__class__ == compound.verbatimTypeSub:

            return Renderer(
                    self.rst_content_creator,
                    self.project_info,
                    data_object,
                    renderer_factory,
                    self.node_factory,
                    self.state,
                    self.document,
                    domain_handler,
                    self.target_handler
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
                renderer_factory,
                self.node_factory,
                self.state,
                self.document,
                domain_handler,
                self.target_handler
                )

    def create_domain_renderer_factory(self, location):

        if not location:
            return self

        domain_handler = self.domain_handler_factory.create_domain_handler(location)

        return DomainRendererFactory(
                    self.renderers,
                    self.node_factory,
                    self.project_info,
                    self.state,
                    self.document,
                    self.domain_handler_factory,
                    domain_handler,
                    self.rst_content_creator,
                    self.member_filter,
                    self.target_handler
                    )

    def create_member_renderer(self, data_object):

        name = data_object.name

        if self.member_filter.allow_member(name):
            return self.create_renderer(data_object)

        return NullRenderer()

    def create_section_renderer(self, data_object):

        name = data_object.kind

        if self.member_filter.allow_section(name):
            return self.create_renderer(data_object)

        return NullRenderer()


class DomainRendererFactory(DoxygenToRstRendererFactory):

    def create_renderer(self, data_object):

        return self.create_renderer_with_factory(data_object, self, self.domain_handler)


class CreateCompoundTypeSubRenderer(object):

    def __init__(self, parser_factory):

        self.parser_factory = parser_factory

    def __call__(self, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexrenderer.CompoundTypeSubRenderer(compound_parser, project_info, *args)


class DoxygenToRstRendererFactoryCreator(object):

    def __init__(
            self,
            node_factory,
            parser_factory,
            domain_handler_factory_creator,
            rst_content_creator
            ):

        self.node_factory = node_factory
        self.parser_factory = parser_factory
        self.domain_handler_factory_creator = domain_handler_factory_creator
        self.rst_content_creator = rst_content_creator

    def create_factory(self, project_info, state, document, member_filter, target_handler):

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
            compound.verbatimTypeSub : compoundrenderer.VerbatimTypeSubRenderer,
            compoundsuper.MixedContainer : compoundrenderer.MixedContainerRenderer,
            unicode : UnicodeRenderer,
            }

        domain_handler_factory = self.domain_handler_factory_creator.create(
                project_info,
                document,
                document.settings.env
                )

        domain_handler = domain_handler_factory.create_null_domain_handler()

        return DoxygenToRstRendererFactory(
                renderers,
                self.node_factory,
                project_info,
                state,
                document,
                domain_handler_factory,
                domain_handler,
                self.rst_content_creator,
                member_filter,
                target_handler
                )


