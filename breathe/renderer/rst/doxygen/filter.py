
class NameAccessor(object):

    def __call__(self, data_object):
        return data_object.name

class NodeNameAccessor(object):

    def __call__(self, data_object):
        try:
            return data_object.node_name
        except AttributeError, e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                return "unicode"
            else:
                raise e

class KindAccessor(object):

    def __call__(self, data_object):
        return data_object.kind

class NameFilter(object):

    def __init__(self, accessor, members):

        self.accessor = accessor
        self.members = members

    def allow(self, parent_name, data_object):

        name = self.accessor(data_object)

        return name in self.members

class GlobFilter(object):

    def __init__(self, accessor, glob):

        self.accessor = accessor
        self.glob = glob

    def allow(self, parent_name, data_object):

        text = self.accessor(data_object)
        return self.glob.match(text)


class OpenFilter(object):

    def allow(self, parent_name, data_object):

        return True

class ClosedFilter(object):

    def allow(self, parent_name, data_object):

        return False

class ParentFilter(object):

    def __init__(self, parent_name):

        self.parent_name = parent_name

    def allow(self, parent_name, data_object):

        return parent_name == self.parent_name

class NotFilter(object):

    def __init__(self, child_filter):
        self.child_filter = child_filter

    def allow(self, parent_name, data_object):

        return not self.child_filter.allow(parent_name, data_object)

class AndFilter(object):

    def __init__(self, first_filter, second_filter):

        self.first_filter = first_filter
        self.second_filter = second_filter

    def allow(self, parent_name, data_object):

        return self.first_filter.allow(parent_name, data_object) \
                and self.second_filter.allow(parent_name, data_object)

class OrFilter(object):

    def __init__(self, first_filter, second_filter):

        self.first_filter = first_filter
        self.second_filter = second_filter

    def allow(self, parent_name, data_object):

        return self.first_filter.allow(parent_name, data_object) \
                or self.second_filter.allow(parent_name, data_object)

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


class FilterFactory(object):

    def __init__(self, globber_factory):

        self.globber_factory = globber_factory

    def create_filter(self, options):

        return AndFilter(
                self.create_members_filter(options),
                self.create_outline_filter(options),
                )

    def create_members_filter(self, options):

        try:
            text = options["members"]
        except KeyError:
            return OrFilter(
                    NotFilter(ParentFilter("sectiondef")),
                    NotFilter(NameFilter(NodeNameAccessor(),["memberdef"]))
                    )

        if not text.strip():
            return OrFilter(
                    NotFilter(NameFilter(NodeNameAccessor(), ["sectiondef"])),
                    GlobFilter(KindAccessor(), self.globber_factory.create("public*"))
                    )

        # Matches sphinx-autodoc behaviour of comma separated values
        members = set([x.strip() for x in text.split(",")])

        return OrFilter(
                NotFilter(ParentFilter("sectiondef")),
                NameFilter(NameAccessor(), members)
                )

    def create_outline_filter(self, options):

        if options.has_key("outline"):
            return NotFilter(NameFilter(NodeNameAccessor(), ["description"]))
        else:
            return OpenFilter()

    def create_open_filter(self):

        return OpenFilter()

