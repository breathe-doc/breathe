
class MemberFilter(object):

    def __init__(self, members):

        self.members = members


    def allow(self, name):

        return name in self.members

class OpenFilter(object):

    def allow(self, name):

        return True


class ClosedFilter(object):

    def allow(self, name):

        return False


class MemberFilterFactory(object):

    def create_filter(self, options):

        try:
            text = options["members"]
        except KeyError:
            return ClosedFilter()

        if not text.strip():
            return OpenFilter()

        # Matches sphinx-autodoc behaviour
        members = set([x.strip() for x in text.split(",")])

        return MemberFilter(members)

    def create_open_filter(self):

        return OpenFilter()

