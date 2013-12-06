from breathe.renderer.rst.doxygen.base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        compound_renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.compounddef)
        nodelist = compound_renderer.render()

        return [self.node_factory.block_quote("", *nodelist)]



class CompoundDefTypeSubRenderer(Renderer):

    # We store both the identified and appropriate title text here as we want to define the order
    # here and the titles for the SectionDefTypeSubRenderer but we don't want the repetition of
    # having two lists in case they fall out of sync
    sections = [
                ("user-defined", "User Defined"),
                ("public-type", "Public Type"),
                ("public-func", "Public Functions"),
                ("public-attrib", "Public Members"),
                ("public-slot", "Public Slot"),
                ("signal", "Signal"),
                ("dcop-func",  "DCOP Function"),
                ("property",  "Property"),
                ("event",  "Event"),
                ("public-static-func", "Public Static Functions"),
                ("public-static-attrib", "Public Static Attributes"),
                ("protected-type",  "Protected Types"),
                ("protected-func",  "Protected Functions"),
                ("protected-attrib",  "Protected Attributes"),
                ("protected-slot",  "Protected Slots"),
                ("protected-static-func",  "Protected Static Functions"),
                ("protected-static-attrib",  "Protected Static Attributes"),
                ("package-type",  "Package Types"),
                ("package-func", "Package Functions"),
                ("package-attrib", "Package Attributes"),
                ("package-static-func", "Package Static Functions"),
                ("package-static-attrib", "Package Static Attributes"),
                ("private-type", "Private Types"),
                ("private-func", "Private Functions"),
                ("private-attrib", "Private Members"),
                ("private-slot",  "Private Slots"),
                ("private-static-func", "Private Static Functions"),
                ("private-static-attrib",  "Private Static Attributes"),
                ("friend",  "Friends"),
                ("related",  "Related"),
                ("define",  "Defines"),
                ("prototype",  "Prototypes"),
                ("typedef",  "Typedefs"),
                ("enum",  "Enums"),
                ("func",  "Functions"),
                ("var",  "Variables"),
                ]

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
            try:
                # As "user-defined" can repeat
                section_nodelists[kind] += subnodes
            except KeyError:
                section_nodelists[kind] = subnodes

        # Order the results in an appropriate manner
        for kind, _ in self.sections:
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

        return nodelist


class SectionDefTypeSubRenderer(Renderer):

    section_titles = dict(CompoundDefTypeSubRenderer.sections)

    def render(self):

        node_list = []

        if self.data_object.description:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.description)
            node_list.append(self.node_factory.paragraph( "", "", *renderer.render()))

        # Get all the memberdef info
        for memberdef in self.data_object.memberdef:
            renderer = self.renderer_factory.create_renderer(self.data_object, memberdef)
            node_list.extend(renderer.render())

        if node_list:

            text = self.section_titles[self.data_object.kind]

            # Override default name for user-defined sections. Use "Unnamed
            # Group" if the user didn't name the section
            # This is different to Doxygen which will track the groups and name
            # them Group1, Group2, Group3, etc.
            if self.data_object.kind == "user-defined":
                if self.data_object.header:
                    text = self.data_object.header
                else:
                    text = "Unnamed Group"
            title = self.node_factory.emphasis(text=text)
            return [title, self.node_factory.block_quote("", *node_list)]

        return []


class MemberDefTypeSubRenderer(Renderer):

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.id)
        return self.target_handler.create_target(refid)

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []

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

        # Build targets for linking
        term_nodes = self.create_domain_target()
        term_nodes.extend(self.create_doxygen_target())

        # Build title nodes
        term_nodes.extend(self.title())
        term = self.node_factory.paragraph("", "", *term_nodes )

        # Build description nodes
        definition = self.node_factory.paragraph("", "", *self.description())

        return [term, self.node_factory.block_quote("", definition)]


class FuncMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_function_target(self.data_object)

    def title(self):

        lines = []

        # Handle any template information
        if self.data_object.templateparamlist:
            renderer = self.renderer_factory.create_renderer(
                    self.data_object,
                    self.data_object.templateparamlist
                    )
            template = [
                    self.node_factory.Text("template < ")
                ]
            template.extend(renderer.render())
            template.append(self.node_factory.Text(" >"))

            # Add blank string at the start otherwise for some reason it renders
            # the emphasis tags around the kind in plain text (same below)
            lines.append(
                    self.node_factory.line(
                        "",
                        self.node_factory.Text(""),
                        *template
                        )
                    )

        # Get the function type and name
        args = MemberDefTypeSubRenderer.title(self)

        # Get the function arguments
        args.append(self.node_factory.Text("("))
        for i, parameter in enumerate(self.data_object.param):
            if i: args.append(self.node_factory.Text(", "))
            renderer = self.renderer_factory.create_renderer(self.data_object, parameter)
            args.extend(renderer.render())
        args.append(self.node_factory.Text(")"))

        lines.append(
                self.node_factory.line(
                    "",
                    self.node_factory.Text(""),
                    *args
                    )
                )

        # Setup the line block with gathered information
        block = self.node_factory.line_block(
                "",
                *lines
                )

        return [block]


class DefineMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        title = []

        title.append(self.node_factory.strong(text=self.data_object.name))

        if self.data_object.param:
            title.append(self.node_factory.Text("("))
            for i, parameter in enumerate(self.data_object.param):
                if i: title.append(self.node_factory.Text(", "))
                renderer = self.renderer_factory.create_renderer(self.data_object, parameter)
                title.extend(renderer.render())
            title.append(self.node_factory.Text(")"))

        return title

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
        for i, entry in enumerate(self.data_object.content_):
            if i:
                nodelist.append(self.node_factory.Text(" "))
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        return nodelist


class ParamTypeSubRenderer(Renderer):

    def __init__(
            self,
            output_defname,
            *args
            ):

        Renderer.__init__( self, *args )

        self.output_defname = output_defname

    def render(self):

        nodelist = []

        # Parameter type
        if self.data_object.type_:
            renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.type_)
            nodelist.extend(renderer.render())

        # Parameter name
        if self.data_object.declname:
            if nodelist: nodelist.append(self.node_factory.Text(" "))
            nodelist.append(self.node_factory.Text(self.data_object.declname))

        if self.output_defname and self.data_object.defname:
            if nodelist: nodelist.append(self.node_factory.Text(" "))
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
    """
    <para> tags in the Doxygen output tend to contain either text or a single other tag of interest.
    So whilst it looks like we're combined descriptions and program listings and other things, in
    the end we generally only deal with one per para tag. Multiple neighbouring instances of these
    things tend to each be in a separate neighbouring para tag.
    """

    def render(self):

        nodelist = []
        for item in self.data_object.content:              # Description
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        for item in self.data_object.programlisting:       # Program listings
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        for item in self.data_object.images:               # Images
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        definition_nodes = []
        for item in self.data_object.simplesects:          # Returns, user par's, etc
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            definition_nodes.extend(renderer.render())

        for entry in self.data_object.parameterlist:       # Parameters/Exceptions
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            definition_nodes.extend(renderer.render())

        if definition_nodes:
            definition_list = self.node_factory.definition_list("", *definition_nodes)
            nodelist.append(definition_list)

        return [self.node_factory.paragraph("", "", *nodelist)]


class DocImageTypeSubRenderer(Renderer):
    "Output docutils image node using name attribute from xml as the uri"

    def render(self):

        path_to_image = self.project_info.sphinx_abs_path_to_file(
                self.data_object.name
                )

        options = { "uri" : path_to_image }

        return [self.node_factory.image("", **options)]

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

        return [self.creator("", "", *nodelist)]


class DocParamListTypeSubRenderer(Renderer):
    "Parameter/Exception documentation"

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

        term_text = self.lookup[self.data_object.kind]
        term = self.node_factory.term("", "", self.node_factory.strong( "", term_text ) )
        definition = self.node_factory.definition('', nodelist_list)

        return [self.node_factory.definition_list_item('', term, definition)]



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
    "Other Type documentation such as Warning, Note, Returns, etc"

    def title(self):

        text = self.node_factory.Text(self.data_object.kind.capitalize())

        return [self.node_factory.strong( "", text )]

    def render(self):

        nodelist = []
        for item in self.data_object.para:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        term = self.node_factory.term("", "", *self.title())
        definition = self.node_factory.definition("", *nodelist)

        return [self.node_factory.definition_list_item("", term, definition)]


class ParDocSimpleSectTypeSubRenderer(DocSimpleSectTypeSubRenderer):

    def title(self):

        renderer = self.renderer_factory.create_renderer(self.data_object, self.data_object.title)

        return [self.node_factory.strong( "", *renderer.render() )]


class DocTitleTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, item)
            nodelist.extend(renderer.render())

        return nodelist


class DocForumlaTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:

            latex = item.getValue()

            # Somewhat hacky if statements to strip out the doxygen markup that slips through

            node = None

            # Either inline
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1]

                # If we're inline create a math node like the :math: role
                node = self.node_factory.math()
            else:
                # Else we're multiline
                node = self.node_factory.displaymath()

            # Or multiline
            if latex.startswith("\[") and latex.endswith("\]"):
                latex = latex[2:-2:]

            # Here we steal the core of the mathbase "math" directive handling code from:
            #    sphinx.ext.mathbase
            node["latex"] = latex

            # Required parameters which we don't have values for
            node["label"] = None
            node["nowrap"] = False
            node["docname"] = self.state.document.settings.env.docname

            nodelist.append(node)

        return nodelist


class ListingTypeSubRenderer(Renderer):

    def render(self):

        lines = []
        nodelist = []
        for i, entry in enumerate(self.data_object.codeline):
            # Put new lines between the lines. There must be a more pythonic way of doing this
            if i:
                nodelist.append(self.node_factory.Text("\n"))
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        # Add blank string at the start otherwise for some reason it renders
        # the pending_xref tags around the kind in plain text
        block = self.node_factory.literal_block(
                "",
                "",
                *nodelist
                )

        return [block]

class CodeLineTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for entry in self.data_object.highlight:
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        return nodelist

class HighlightTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for entry in self.data_object.content_:
            renderer = self.renderer_factory.create_renderer(self.data_object, entry)
            nodelist.extend(renderer.render())

        return nodelist

class TemplateParamListRenderer(Renderer):

    def render(self):

        nodelist = []

        for i, param in enumerate(self.data_object.param):
            if i:
                nodelist.append(self.node_factory.Text(", "))
            renderer = self.renderer_factory.create_renderer(self.data_object, param)
            nodelist.extend(renderer.render())

        return nodelist

class IncTypeSubRenderer(Renderer):

    def render(self):

        if self.data_object.local == u"yes":
            text = '#include "%s"' % self.data_object.content_[0].getValue()
        else:
            text = '#include <%s>' % self.data_object.content_[0].getValue()

        return [self.node_factory.emphasis(text=text)]

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

        # do we need to strip leading asterisks?
        # NOTE: We could choose to guess this based on every line starting with '*'.
        #   However This would have a side-effect for any users who have an rst-block
        #   consisting of a simple bullet list.
        #   For now we just look for an extended embed tag
        if self.data_object.text.strip().startswith("embed:rst:leading-asterisk"):

            lines = self.data_object.text.splitlines()
            # Replace the first * on each line with a blank space
            lines = map( lambda text: text.replace( "*", " ", 1 ), lines )
            self.data_object.text = "\n".join( lines )

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


