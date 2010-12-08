
class NamedFilter(object):

    def __init__(self, members):

        self.members = members

    def allow(self, name):

        return name in self.members

class GlobFilter(object):

    def __init__(self, glob):

        self.glob = glob

    def allow(self, name):

        return self.glob.match(name)


class OpenFilter(object):

    def allow(self, name):

        return True

class ClosedFilter(object):

    def allow(self, name):

        return False

class CombinedFilter(object):

    def __init__(self, section_filter, member_filter):

        self.section_filter = section_filter
        self.member_filter = member_filter

    def allow_section(self, name):

        return self.section_filter.allow(name)

    def allow_member(self, name):

        return self.member_filter.allow(name)


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

        try:
            text = options["members"]
        except KeyError:
            return CombinedFilter(ClosedFilter(), ClosedFilter())

        if not text.strip():
            return CombinedFilter(
                    GlobFilter(self.globber_factory.create("public*")),
                    OpenFilter()
                    )

        # Matches sphinx-autodoc behaviour
        members = set([x.strip() for x in text.split(",")])

        return CombinedFilter(OpenFilter(), NamedFilter(members))

    def create_open_filter(self):

        return CombinedFilter(OpenFilter(), OpenFilter())

