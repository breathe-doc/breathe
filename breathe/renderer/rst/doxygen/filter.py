
class Selecter(object):
    pass

class Parent(Selecter):

    def __call__(self, parent_data_object, child_data_object):
        return parent_data_object

class Child(Selecter):

    def __call__(self, parent_data_object, child_data_object):
        return child_data_object


class Accessor(object):

    def __init__(self, selecter):
        self.selecter = selecter

class NameAccessor(Accessor):

    def __call__(self, parent_data_object, child_data_object):
        return self.selecter(parent_data_object, child_data_object).name

class NodeNameAccessor(Accessor):

    def __call__(self, parent_data_object, child_data_object):
        return self.selecter(parent_data_object, child_data_object).node_name

class NodeTypeAccessor(Accessor):

    def __call__(self, parent_data_object, child_data_object):

        data_object = self.selecter(parent_data_object, child_data_object)
        try:
            return data_object.node_type
        except AttributeError, e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                return "unicode"
            else:
                raise e

class KindAccessor(Accessor):

    def __call__(self, parent_data_object, child_data_object):
        return self.selecter(parent_data_object, child_data_object).kind

class LambdaAccessor(Accessor):

    def __init__(self, selecter, func):
        Accessor.__init__(self, selecter)

        self.func = func

    def __call__(self, parent_data_object, child_data_object):
        return self.func(self.selecter(parent_data_object, child_data_object))

class NamespaceAccessor(Accessor):

    def __call__(self, parent_data_object, child_data_object):
        return self.selecter(parent_data_object, child_data_object).namespaces

class NameFilter(object):

    def __init__(self, accessor, members):

        self.accessor = accessor
        self.members = members

    def allow(self, parent_data_object, child_data_object):

        name = self.accessor(parent_data_object, child_data_object)
        return name in self.members

class GlobFilter(object):

    def __init__(self, accessor, glob):

        self.accessor = accessor
        self.glob = glob

    def allow(self, parent_data_object, child_data_object):

        text = self.accessor(parent_data_object, child_data_object)
        return self.glob.match(text)


class FilePathFilter(object):

    def __init__(self, accessor, target_file, path_handler):

        self.accessor = accessor
        self.target_file = target_file
        self.path_handler = path_handler

    def allow(self, parent_data_object, child_data_object):

        location = self.accessor(parent_data_object, child_data_object).file

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

    def allow(self, parent_data_object, child_data_object):

        namespaces = self.namespace_accessor(parent_data_object, child_data_object)
        name = self.name_accessor(parent_data_object, child_data_object)

        try:
            namespace, name = name.rsplit("::", 1)
        except ValueError:
            namespace, name = "", name

        return namespace in namespaces

class OpenFilter(object):

    def allow(self, parent_data_object, child_data_object):

        return True

class ClosedFilter(object):

    def allow(self, parent_data_object, child_data_object):

        return False

class NotFilter(object):

    def __init__(self, child_filter):
        self.child_filter = child_filter

    def allow(self, parent_data_object, child_data_object):

        return not self.child_filter.allow(parent_data_object, child_data_object)

class AndFilter(object):

    def __init__(self, first_filter, second_filter):

        self.first_filter = first_filter
        self.second_filter = second_filter

    def allow(self, parent_data_object, child_data_object):

        return self.first_filter.allow(parent_data_object, child_data_object) \
                and self.second_filter.allow(parent_data_object, child_data_object)

class OrFilter(object):

    def __init__(self, first_filter, second_filter):

        self.first_filter = first_filter
        self.second_filter = second_filter

    def allow(self, parent_data_object, child_data_object):

        return self.first_filter.allow(parent_data_object, child_data_object) \
                or self.second_filter.allow(parent_data_object, child_data_object)

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

class PathHandler(object):

    def __init__(self, sep, basename):

        self.sep = sep
        self.basename = basename

    def includes_directory(self, file_path):

        return bool( file_path.count( self.sep ) )

class FilterFactory(object):

    def __init__(self, globber_factory, path_handler):

        self.globber_factory = globber_factory
        self.path_handler = path_handler

    def create_class_filter(self, options):

        return AndFilter(
                self.create_members_filter(options),
                self.create_outline_filter(options),
                )

    def create_members_filter(self, options):

        try:
            text = options["members"]
        except KeyError:
            return OrFilter(
                    NotFilter(NameFilter(NodeTypeAccessor(Parent()), ["sectiondef"])),
                    NotFilter(NameFilter(NodeTypeAccessor(Child()), ["memberdef"]))
                    )

        if not text.strip():
            return OrFilter(
                    NotFilter(NameFilter(NodeTypeAccessor(Child()), ["sectiondef"])),
                    GlobFilter(KindAccessor(Child()), self.globber_factory.create("public*"))
                    )

        # Matches sphinx-autodoc behaviour of comma separated values
        members = set([x.strip() for x in text.split(",")])

        return OrFilter(
                NotFilter(NameFilter(NodeTypeAccessor(Parent()),["sectiondef"])),
                NameFilter(NameAccessor(Child()), members)
                )

    def create_outline_filter(self, options):

        if options.has_key("outline"):
            return NotFilter(NameFilter(NodeTypeAccessor(Child()), ["description"]))
        else:
            return OpenFilter()

    def create_file_filter(self, options):

        filter_ = OrFilter(
                NotFilter(
                    NameFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    ),
                NotFilter(
                    AndFilter(
                        AndFilter(
                            NameFilter(NodeTypeAccessor(Child()),["ref"]),
                            NameFilter(NodeNameAccessor(Child()),["innerclass", "innernamespace"])
                            ),
                        NamespaceFilter(
                            NamespaceAccessor(Parent()),
                            LambdaAccessor(Child(), lambda x: x.content_[0].getValue())
                            )
                        )
                    )
                )

        return AndFilter(
                self.create_outline_filter(options),
                filter_
                )

    def create_index_filter(self, options):

        filter_ = AndFilter(
                NotFilter(
                    AndFilter(
                        NameFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                        AndFilter(
                            NameFilter(NodeTypeAccessor(Child()),["ref"]),
                            NameFilter(NodeNameAccessor(Child()),["innerclass", "innernamespace"])
                            )
                        )
                    ),
                NotFilter(
                    AndFilter(
                        AndFilter(
                            NameFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                            NameFilter(KindAccessor(Parent()), ["group"])
                            ),
                        AndFilter(
                            NameFilter(NodeTypeAccessor(Child()),["sectiondef"]),
                            NameFilter(KindAccessor(Child()),["func"])
                            )
                        )
                    )
                )


        return AndFilter(
                self.create_outline_filter(options),
                filter_
                )

    def create_open_filter(self):

        return OpenFilter()

    def create_file_finder_filter(self, filename):

        filter_ = AndFilter(
                AndFilter(
                    NameFilter(NodeTypeAccessor(Child()), ["compounddef"]),
                    NameFilter(KindAccessor(Child()), ["file"]),
                    ),
                FilePathFilter(LambdaAccessor(Child(), lambda x: x.location), filename, self.path_handler)
                )

        return filter_

