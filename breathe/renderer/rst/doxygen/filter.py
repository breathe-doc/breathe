
class Selector(object):
    pass


class Ancestor(Selector):

    def __init__(self, generations):
        self.generations = generations

    def __call__(self, node_stack):
        return node_stack[self.generations]


class Parent(Selector):

    def __call__(self, node_stack):
        return node_stack[1]


class Node(Selector):

    def __call__(self, node_stack):
        return node_stack[0]


class Accessor(object):

    def __init__(self, selector):
        self.selector = selector


class NameAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).name


class NodeNameAccessor(Accessor):
    """Check the .node_name member which is declared on refTypeSub nodes

    It distinguishes between innerclass, innernamespace, etc.
    """

    def __call__(self, node_stack):
        return self.selector(node_stack).node_name


class NodeTypeAccessor(Accessor):

    def __call__(self, node_stack):

        data_object = self.selector(node_stack)
        try:
            return data_object.node_type
        except AttributeError as e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                return "unicode"
            else:
                raise e


class KindAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).kind


class LambdaAccessor(Accessor):

    def __init__(self, selector, func):
        Accessor.__init__(self, selector)

        self.func = func

    def __call__(self, node_stack):
        return self.func(self.selector(node_stack))


class NamespaceAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).namespaces


class InFilter(object):
    """Checks if what is returned from the accessor is 'in' in the members"""

    def __init__(self, accessor, members):

        self.accessor = accessor
        self.members = members

    def allow(self, node_stack):

        name = self.accessor(node_stack)

        return name in self.members


class GlobFilter(object):

    def __init__(self, accessor, glob):

        self.accessor = accessor
        self.glob = glob

    def allow(self, node_stack):

        text = self.accessor(node_stack)
        return self.glob.match(text)


class FilePathFilter(object):

    def __init__(self, accessor, target_file, path_handler):

        self.accessor = accessor
        self.target_file = target_file
        self.path_handler = path_handler

    def allow(self, node_stack):

        location = self.accessor(node_stack).file

        if self.path_handler.includes_directory(self.target_file):
            # If the target_file contains directory separators then
            # match against the same length at the ned of the location
            #
            location_match = location[-len(self.target_file):]
            return location_match == self.target_file

        else:
            # If there are not separators, match against the whole filename
            # at the end of the location
            #
            # This is to prevent "Util.cpp" matching "PathUtil.cpp"
            #
            location_basename = self.path_handler.basename(location)
            return location_basename == self.target_file


class NamespaceFilter(object):

    def __init__(self, namespace_accessor, name_accessor):

        self.namespace_accessor = namespace_accessor
        self.name_accessor = name_accessor

    def allow(self, node_stack):

        namespaces = self.namespace_accessor(node_stack)
        name = self.name_accessor(node_stack)

        try:
            namespace, name = name.rsplit("::", 1)
        except ValueError:
            namespace, name = "", name

        return namespace in namespaces


class OpenFilter(object):

    def allow(self, node_stack):

        return True


class ClosedFilter(object):

    def allow(self, node_stack):

        return False


class NotFilter(object):

    def __init__(self, child_filter):
        self.child_filter = child_filter

    def allow(self, node_stack):

        return not self.child_filter.allow(node_stack)



class AndFilter(object):

    def __init__(self, *filters):

        self.filters = filters

    def allow(self, node_stack):

        # If any filter returns False then return False
        for filter_ in self.filters:
            if not filter_.allow(node_stack):
                return False

        return True


class OrFilter(object):
    """Provides a short-cutted 'or' operation between two filters"""

    def __init__(self, *filters):

        self.filters = filters

    def allow(self, node_stack):

        # If any filter returns True then return True
        for filter_ in self.filters:
            if filter_.allow(node_stack):
                return True

        return False


class Glob(object):

    def __init__(self, method, pattern):

        self.method = method
        self.pattern = pattern

    def match(self, name):

        return self.method(name, self.pattern)


class GlobFactory(object):

    def __init__(self, method):

        self.method = method

    def create(self, pattern):

        return Glob(self.method, pattern)


class Gather(object):

    def __init__(self, accessor, names):

        self.accessor = accessor
        self.names = names

    def allow(self, node_stack):

        self.names.extend(self.accessor(node_stack))

        return False


class FilterFactory(object):

    def __init__(self, globber_factory, path_handler):

        self.globber_factory = globber_factory
        self.path_handler = path_handler

    def create_class_filter(self, options):

        return AndFilter(
            self.create_members_filter(options),
            self.create_outline_filter(options),
            self.create_show_filter(options),
            )

    def create_show_filter(self, options):
        """
        Currently only handles the header-file entry
        """

        try:
            text = options["show"]
        except KeyError:
            # Allow through everything except the header-file includes nodes
            return OrFilter(
                NotFilter(InFilter(NodeTypeAccessor(Parent()), ["compounddef"])),
                NotFilter(InFilter(NodeTypeAccessor(Node()), ["inc"]))
                )

        if text == "header-file":
            # Allow through everything, including header-file includes
            return OpenFilter()

        # Allow through everything except the header-file includes nodes
        return OrFilter(
            NotFilter(InFilter(NodeTypeAccessor(Parent()), ["compounddef"])),
            NotFilter(InFilter(NodeTypeAccessor(Node()), ["inc"]))
            )

    def create_members_filter(self, options):

        section = options.get("sections", "")

        if not section.strip():
            section_filter = GlobFilter(KindAccessor(Node()),
                                        self.globber_factory.create("public*"))
        else:
            sections = set([x.strip() for x in section.split(",")])

            section_filter = GlobFilter(
                KindAccessor(Node()),
                self.globber_factory.create(sections.pop())
                )
            while len(sections) > 0:
                section_filter = OrFilter(
                    section_filter,
                    GlobFilter(
                        KindAccessor(Node()),
                        self.globber_factory.create(sections.pop())
                        )
                    )

        if "members" not in options:
            return OrFilter(
                NotFilter(InFilter(NodeTypeAccessor(Parent()), ["sectiondef"])),
                NotFilter(InFilter(NodeTypeAccessor(Node()), ["memberdef"]))
                )

        text = options["members"]
        if not text.strip():
            return OrFilter(
                NotFilter(InFilter(NodeTypeAccessor(Node()), ["sectiondef"])),
                section_filter,
                InFilter(KindAccessor(Node()), ["user-defined"])
                )

        # Matches sphinx-autodoc behaviour of comma separated values
        members = set([x.strip() for x in text.split(",")])

        # Accept any nodes which don't have a "sectiondef" as a parent or, if they do, only accept
        # them if their names are in the members list or they are of type description. This accounts
        # for the actual description of the sectiondef
        return OrFilter(
            NotFilter(InFilter(NodeTypeAccessor(Parent()), ["sectiondef"])),
            InFilter(NodeTypeAccessor(Node()), ["description"]),
            InFilter(NameAccessor(Node()), members),
            )

    def create_outline_filter(self, options):

        if 'outline' in options:
            return NotFilter(InFilter(NodeTypeAccessor(Node()), ["description"]))
        else:
            return OpenFilter()

    def create_file_filter(self, filename, options):

        valid_names = []

        filter_ = AndFilter(
            NotFilter(
                # Gather the "namespaces" attribute from the
                # compounddef for the file we're rendering and
                # store the information in the "valid_names" list
                #
                # Gather always returns false, so, combined with
                # the NotFilter this chunk always returns true and
                # so does not affect the result of the filtering
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
                    InFilter(KindAccessor(Node()), ["file"]),
                    FilePathFilter(
                        LambdaAccessor(Node(), lambda x: x.location),
                        filename, self.path_handler
                        ),
                    Gather(LambdaAccessor(Node(), lambda x: x.namespaces), valid_names)
                    )
                ),
            NotFilter(
                # Take the valid_names and everytime we handle an
                # innerclass or innernamespace, check that its name
                # was one of those initial valid names so that we
                # never end up rendering a namespace or class that
                # wasn't in the initial file. Notably this is
                # required as the location attribute for the
                # namespace in the xml is unreliable.
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"]),
                    NotFilter(
                        InFilter(
                            LambdaAccessor(Node(), lambda x: x.content_[0].getValue()),
                            valid_names
                            )
                        )
                    )
                ),
            NotFilter(
                # Ignore innerclasses and innernamespaces that are inside a
                # namespace that is going to be rendered as they will be
                # rendered with that namespace and we don't want them twice
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"]),
                    NamespaceFilter(
                        NamespaceAccessor(Parent()),
                        LambdaAccessor(Node(), lambda x: x.content_[0].getValue())
                        )
                    )
                ),
            NotFilter(
                # Ignore memberdefs from files which are different to
                # the one we're rendering. This happens when we have to
                # cross into a namespace xml file which has entries
                # from multiple files in it
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["memberdef"]),
                    NotFilter(
                        FilePathFilter(LambdaAccessor(Node(), lambda x: x.location),
                                       filename, self.path_handler)
                        )
                    )
                ),
            NotFilter(
                # Ignore compounddefs which are from another file
                # (normally means classes and structs which are in a
                # namespace that we have other interests in) but only
                # check it if the compounddef is not a namespace
                # itself, as for some reason compounddefs for
                # namespaces are registered with just a single file
                # location even if they namespace is spread over
                # multiple files
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
                    NotFilter(InFilter(KindAccessor(Node()), ["namespace"])),
                    NotFilter(
                        FilePathFilter(LambdaAccessor(Node(), lambda x: x.location),
                                       filename, self.path_handler)
                        )
                    )
                )
            )

        return AndFilter(
            self.create_outline_filter(options),
            filter_
            )

    def create_group_content_filter(self):
        """Returns a filter which matches the contents of the group but not the group name or
        description.

        This allows the groups to be used to structure sections of the documentation rather than to
        structure and further document groups of documentation
        """

        # Display the contents of the sectiondef nodes and any innerclass or innernamespace
        # references
        return OrFilter(
            InFilter(NodeTypeAccessor(Parent()), ["sectiondef"]),
            AndFilter(
                InFilter(NodeTypeAccessor(Node()), ["ref"]),
                InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"]),
                )
            )

    def create_index_filter(self, options):

        filter_ = AndFilter(
            NotFilter(
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"])
                    )
                ),
            NotFilter(
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(KindAccessor(Parent()), ["group"]),
                    InFilter(NodeTypeAccessor(Node()), ["sectiondef"]),
                    InFilter(KindAccessor(Node()), ["func"])
                    )
                )
            )

        return AndFilter(
            self.create_outline_filter(options),
            filter_
            )

    def create_open_filter(self):
        """Returns a completely open filter which matches everything"""

        return OpenFilter()

    def create_file_finder_filter(self, filename):

        filter_ = AndFilter(
            InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
            InFilter(KindAccessor(Node()), ["file"]),
            FilePathFilter(LambdaAccessor(Node(), lambda x: x.location), filename,
                           self.path_handler)
            )

        return filter_

    def create_group_finder_filter(self, name):
        """Returns a filter which looks for the compound node from the index which is a group node
        (kind=group) and has the appropriate name

        The compound node should reference the group file which we can parse for the group
        contents."""

        filter_ = AndFilter(
            InFilter(NodeTypeAccessor(Node()), ["compound"]),
            InFilter(KindAccessor(Node()), ["group"]),
            InFilter(NameAccessor(Node()), [name])
            )

        return filter_

