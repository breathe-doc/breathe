
from breathe.renderer.rst.doxygen.base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        compound_renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.compounddef)
        return compound_renderer.render()


class CompoundDefTypeSubRenderer(Renderer):

    section_titles = [
                "user-defined",
                "public-type",
                "public-func",
                "public-attrib",
                "public-slot",
                "signal",
                "dcop-func",
                "property",
                "event",
                "public-static-func",
                "public-static-attrib",
                "protected-type",
                "protected-func",
                "protected-attrib",
                "protected-slot",
                "protected-static-func",
                "protected-static-attrib",
                "package-type",
                "package-attrib",
                "package-static-func",
                "package-static-attrib",
                "private-type",
                "private-func",
                "private-attrib",
                "private-slot",
                "private-static-func",
                "private-static-attrib",
                "friend",
                "related",
                "define",
                "prototype",
                "typedef",
                "enum",
                "func",
                "var"
             ]


    def extend_nodelist(self, nodelist, section, title, section_nodelists):

        # Add title and contents if found
        if section_nodelists.has_key(section):
            nodes = section_nodelists[section]

            if nodes:

                nodelist.append(self.node_factory.emphasis(text=title))
                nodelist.append(self.node_factory.block_quote("", *nodes))

    def render(self):

        nodelist = []    

        if self.data_object.briefdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.briefdescription)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        if self.data_object.detaileddescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.detaileddescription)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        section_nodelists = {}

        # Get all sub sections
        for sectiondef in self.data_object.sectiondef:
            kind = sectiondef.kind
            renderer = self.renderer_factory.create_renderer(self.data_object, sectiondef)
            subnodes = renderer.render()
            section_nodelists[kind] = subnodes

        # Order the results in an appropriate manner
        for kind in self.section_titles:
            nodelist.extend(section_nodelists.get(kind, []))

        # Take care of innerclasses
        for innerclass in self.data_object.innerclass:
            renderer = self.renderer_factory.create_renderer(self.data_object, innerclass)
            class_nodes = renderer.render()
            if class_nodes: 
                nodelist.append(self.node_factory.paragraph("", "", *class_nodes))

        for innernamespace in self.data_object.innernamespace:
            renderer = self.renderer_factory.create_renderer(self.data_object, innernamespace)
            namespace_nodes = renderer.render() 
            if namespace_nodes:
                nodelist.append(self.node_factory.paragraph("", "", *namespace_nodes))

        return [self.node_factory.block_quote("", *nodelist)]


class SectionDefTypeSubRenderer(Renderer):

    section_titles = {
                "user-defined": "User Defined",
                "public-type": "Public Type",
                "public-func": "Public Functions",
                "public-attrib": "Public Members",
                "public-slot": "Public Slot",
                "signal": "Signal",
                "dcop-func":  "DCOP Function",
                "property":  "Property",
                "event":  "Event",
                "public-static-func": "Public Static Functons",
                "public-static-attrib": "Public Static Attributes",
                "protected-type":  "Protected Types",
                "protected-func":  "Protected Functions",
                "protected-attrib":  "Protected Attributes",
                "protected-slot":  "Protected Slots",
                "protected-static-func":  "Protected Static Functions",
                "protected-static-attrib":  "Protected Static Attributes",
                "package-type":  "Package Types",
                "package-attrib": "Package Attributes",
                "package-static-func": "Package Static Functions",
                "package-static-attrib": "Package Static Attributes",
                "private-type": "Private Types",
                "private-func": "Private Functions",
                "private-attrib": "Private Members",
                "private-slot":  "Private Slots",
                "private-static-func": "Private Static Functions",
                "private-static-attrib":  "Private Static Attributes",
                "friend":  "Friends",
                "related":  "Related",
                "define":  "Defines",
                "prototype":  "Prototypes",
                "typedef":  "Typedefs",
                "enum":  "Enums",
                "func":  "Functions",
                "var":  "Variables",
                }

    def render(self):

        defs = []

        # Get all the memberdef info
        for memberdef in self.data_object.memberdef:
            renderer = self.renderer_factory.create_renderer(self.data_object, memberdef)
            defs.extend(renderer.render())

        if defs:
            text = self.section_titles[self.data_object.kind]
            title = self.node_factory.emphasis(text=text)
            def_list = self.node_factory.definition_list("", *defs)
            return [title, self.node_factory.block_quote("", def_list)]

        return []


class MemberDefTypeSubRenderer(Renderer):

    def create_target(self, refid):

        return self.target_handler.create_target(refid)

    def create_domain_id(self):

        return ""

    def title(self):

        kind = []
        
        # Variable type or function return type
        if self.data_object.type_:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.type_)
            kind = renderer.render()

        name = self.node_factory.strong(text=self.data_object.name)

        args = []
        args.extend(kind)
        args.extend([self.node_factory.Text(" "), name])

        return args


    def description(self):

        description_nodes = []

        if self.data_object.briefdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.briefdescription)
            description_nodes.append(self.node_factory.paragraph("", "", *renderer.render()))

        if self.data_object.detaileddescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.detaileddescription)
            description_nodes.append(self.node_factory.paragraph( "", "", *renderer.render()))

        return description_nodes


    def render(self):

        refid = "%s%s" % (self.project_info.name(), self.data_object.id)

        domain_id = self.create_domain_id()

        title = self.title()
        target = self.create_target(refid)
        target.extend(title)
        term = self.node_factory.term("","", ids=[domain_id,refid], *target )
        definition = self.node_factory.definition("", *self.description())
        entry = self.node_factory.definition_list_item("",term, definition)

        return [entry]


class FuncMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def create_target(self, refid):

        self.domain_handler.create_function_target(self.data_object)

        return MemberDefTypeSubRenderer.create_target(self, refid)


    def create_domain_id(self):

        return self.domain_handler.create_function_id(self.data_object)


    def title(self):

        args = MemberDefTypeSubRenderer.title(self)

        # Get the function arguments
        args.append(self.node_factory.Text("("))
        for i, parameter in enumerate(self.data_object.param):
            if i: args.append(self.node_factory.Text(", "))
            renderer = self.renderer_factory.create_renderer(self.data_object, parameter)
            args.extend(renderer.render())
        args.append(self.node_factory.Text(")"))

        return args


class DefineMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        name = self.node_factory.strong(text=self.data_object.name)
        return [name]

    def description(self):

        return MemberDefTypeSubRenderer.description(self)


class EnumMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        if self.data_object.name.startswith("@"):
            # Assume anonymous enum
            return [self.node_factory.strong(text="Anonymous enum")]

        name = self.node_factory.strong(text="%s enum" % self.data_object.name)
        return [name]

    def description(self):

        description_nodes = MemberDefTypeSubRenderer.description(self)

        name = self.node_factory.emphasis("", self.node_factory.Text("Values:"))
        title = self.node_factory.paragraph("", "", name)
        description_nodes.append(title)

        enums = []
        for item in self.data_object.enumvalue:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            enums.extend(renderer.render())

        description_nodes.append(self.node_factory.bullet_list("", classes=["breatheenumvalues"], *enums))

        return description_nodes


class TypedefMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        args = [self.node_factory.Text("typedef ")]
        args.extend(MemberDefTypeSubRenderer.title(self))

        if self.data_object.argsstring:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.argsstring)
            args.extend(renderer.render())

        return args


class VariableMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        args = MemberDefTypeSubRenderer.title(self)

        if self.data_object.argsstring:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.argsstring)
            args.extend(renderer.render())

        return args


class EnumvalueTypeSubRenderer(Renderer):

    def render(self):

        name = self.node_factory.literal(text=self.data_object.name)
        description_nodes = [name]

        if self.data_object.initializer:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.initializer)
            nodelist = [self.node_factory.Text(" = ")]
            nodelist.extend(renderer.render())
            description_nodes.append(self.node_factory.literal("", "", *nodelist))

        separator = self.node_factory.Text(" - ")
        description_nodes.append(separator)

        if self.data_object.briefdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.briefdescription)
            description_nodes.extend(renderer.render())

        if self.data_object.detaileddescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.detaileddescription)
            description_nodes.extend(renderer.render())

        # Build the list item
        return [self.node_factory.list_item("", *description_nodes)]

class DescriptionTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        
        # Get description in rst_nodes if possible
        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        return nodelist


class LinkedTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Recursively process where possible
        for i in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, i)
            nodelist.extend(renderer.render())
            nodelist.append(self.node_factory.Text(" "))


        return nodelist


class ParamTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Parameter type
        if self.data_object.type_:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.type_)
            nodelist.extend(renderer.render())

        # Parameter name
        if self.data_object.declname:
            nodelist.append(self.node_factory.Text(self.data_object.declname))

        if self.data_object.defname:
            nodelist.append(self.node_factory.Text(self.data_object.defname))

        # Default value
        if self.data_object.defval:
            nodelist.append(self.node_factory.Text(" = "))
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.defval)
            nodelist.extend(renderer.render())

        return nodelist



class DocRefTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        for item in self.data_object.para:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        nodelist = [
                self.node_factory.pending_xref(
                    "",
                    reftype="ref",
                    refdomain="std",
                    refexplicit=True,
                    refid=refid, 
                    reftarget=refid,
                    *nodelist
                    )
                ]

        return nodelist


class DocParaTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.content:              # Description
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        field_nodes = []
        for entry in self.data_object.parameterlist:        # Parameters/Exceptions
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            field_nodes.extend(renderer.render())

        for item in self.data_object.simplesects:           # Returns
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            field_nodes.extend(renderer.render())

        if field_nodes:
            field_list = self.node_factory.field_list("", *field_nodes)
            nodelist.append(field_list)

        return [self.node_factory.paragraph("", "", *nodelist)]


class DocMarkupTypeSubRenderer(Renderer):

    def __init__(
            self,
            creator,
            *args
            ):

        Renderer.__init__( self, *args )

        self.creator = creator

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        return [self.creator("", *nodelist)]


class DocParamListTypeSubRenderer(Renderer):
    """ Parameter/Exectpion documentation """

    lookup = {
            "param" : "Parameters",
            "exception" : "Exceptions",
            "templateparam" : "Templates",
            "retval" : "Return Value",
            }

    def render(self):

        nodelist = []
        for entry in self.data_object.parameteritem:
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        # Fild list entry
        nodelist_list = self.node_factory.bullet_list("", classes=["breatheparameterlist"], *nodelist)

        field_name = self.lookup[self.data_object.kind]
        field_name = self.node_factory.field_name("", field_name)
        field_body = self.node_factory.field_body('', nodelist_list)

        return [self.node_factory.field('', field_name, field_body)]



class DocParamListItemSubRenderer(Renderer):
    """ Paramter Description Renderer  """

    def render(self):

        nodelist = []
        for entry in self.data_object.parameternamelist:
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        term = self.node_factory.literal("","", *nodelist)

        separator = self.node_factory.Text(" - ")

        nodelist = []

        if self.data_object.parameterdescription:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.parameterdescription)
            nodelist.extend(renderer.render())

        return [self.node_factory.list_item("", term, separator, *nodelist)]

class DocParamNameListSubRenderer(Renderer):
    """ Parameter Name Renderer """

    def render(self):

        nodelist = []
        for entry in self.data_object.parametername:
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        return nodelist

class DocParamNameSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        return nodelist

class DocSect1TypeSubRenderer(Renderer):

    def render(self):

        return []


class DocSimpleSectTypeSubRenderer(Renderer):
    """ Other Type documentation such as Warning, Note, Retuns..."""

    def title(self):

        text = self.node_factory.Text(self.data_object.kind.capitalize())
        emphasis = self.node_factory.emphasis("", text)

        return [emphasis]

    def render(self):

        nodelist = []
        for item in self.data_object.para:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        field_name = self.node_factory.field_name("", self.node_factory.Text(self.data_object.kind.capitalize()))
        field_body = self.node_factory.field_body('', *nodelist)

        return [self.node_factory.field('', field_name, field_body)]


class ParDocSimpleSectTypeSubRenderer(DocSimpleSectTypeSubRenderer):

    def title(self):

        renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.title)
        emphasis = self.node_factory.emphasis("", *renderer.render())

        return [emphasis]


class DocTitleTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        return nodelist


class RefTypeSubRenderer(Renderer):

    ref_types = {
            "innerclass" : "class",
            "innernamespace" : "namespace",
            }

    def __init__(self, compound_parser, *args):
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser

    def render(self):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)
        data_renderer = self.renderer_factory.create_renderer(self.data_object, file_data)

        child_nodes = data_renderer.render()

        # Only render the header with refs if we've definitely got content to
        # put underneath it. Otherwise return an empty list
        if child_nodes:

            refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
            nodelist = self.target_handler.create_target(refid)

            # Set up the title and a reference for it (refid)
            type_ = self.ref_types[self.data_object.node_name]
            kind = self.node_factory.emphasis(text=type_)

            name_text = self.data_object.content_[0].getValue()
            name_text = name_text.rsplit("::", 1)[-1]
            name = self.node_factory.strong(text=name_text)

            nodelist = []

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

            nodelist.extend(child_nodes)

            return nodelist

        return []

class VerbatimTypeSubRenderer(Renderer):

    def __init__(self, content_creator, *args):
        Renderer.__init__(self, *args)

        self.content_creator = content_creator

    def render(self):

        if not self.data_object.text.strip().startswith("embed:rst"):

            # Remove trailing new lines. Purely subjective call from viewing results
            text = self.data_object.text.rstrip()

            # Handle has a preformatted text
            return [self.node_factory.literal_block(text, text)]

        rst = self.content_creator(self.data_object.text)

        # Parent node for the generated node subtree
        node = self.node_factory.paragraph()
        node.document = self.state.document

        # Generate node subtree
        self.state.nested_parse(rst, 0, node)

        return node


class MixedContainerRenderer(Renderer):

    def render(self):

        renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.getValue())
        return renderer.render()


