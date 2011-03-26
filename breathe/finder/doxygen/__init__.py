
from breathe.finder.doxygen import index as indexfinder
from breathe.finder.doxygen import compound as compoundfinder

from breathe.parser.doxygen import index, compound

class MissingLevelError(Exception):
    pass

class Matcher(object):
    pass

class ItemMatcher(Matcher):

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def match(self, data_object):
        return self.name == data_object.name and self.type_ == data_object.kind

    def __repr__(self):
        return "<ItemMatcher - name:%s, type_:%s>" % (self.name, self.type_)

class NameMatcher(Matcher):

    def __init__(self, name):
        self.name = name

    def match(self, data_object):
        return self.name == data_object.name


class RefMatcher(Matcher):

    def __init__(self, refid):

        self.refid = refid

    def match(self, data_object):
        return self.refid == data_object.refid

class AnyMatcher(Matcher):

    def match(self, data_object):
        return True


class MatcherStack(object):

    def __init__(self, matchers, lowest_level):

        self.matchers = matchers
        self.lowest_level = lowest_level

    def match(self, level, data_object):

        try:
            return self.matchers[level].match(data_object)
        except KeyError:
            return False

    def full_match(self, level, data_object):

        try:
            return self.matchers[level].match(data_object) and level == self.lowest_level
        except KeyError:
            raise MissingLevelError(level)


class ItemMatcherFactory(Matcher):

    def create_name_type_matcher(self, name, type_):

        return ItemMatcher(name, type_)

    def create_name_matcher(self, name):

        return NameMatcher(name) if name else AnyMatcher()

    def create_ref_matcher(self, ref):

        return RefMatcher(ref)

    def create_matcher_stack(self, matchers, lowest_level):

        return MatcherStack(matchers, lowest_level)

    def create_ref_matcher_stack(self, class_, ref):

        matchers = {
                "compound" : ItemMatcher(class_, "class") if class_ else AnyMatcher(),
                "member" : RefMatcher(ref),
                }

        return MatcherStack(matchers, "member")


class CreateCompoundTypeSubFinder(object):

    def __init__(self, parser_factory, matcher_factory):

        self.parser_factory = parser_factory
        self.matcher_factory = matcher_factory

    def __call__(self, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexfinder.CompoundTypeSubItemFinder(self.matcher_factory, compound_parser, project_info, *args)



class DoxygenItemFinderFactory(object):

    def __init__(self, finders, project_info):

        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object):

        return self.finders[data_object.node_type](self.project_info, data_object, self)


class DoxygenItemFinderFactoryCreator(object):

    def __init__(self, parser_factory, matcher_factory):

        self.parser_factory = parser_factory
        self.matcher_factory = matcher_factory

    def create_factory(self, project_info):

        finders = {
            "doxygen" : indexfinder.DoxygenTypeSubItemFinder,
            "compound" : CreateCompoundTypeSubFinder(self.parser_factory, self.matcher_factory),
            "member" : indexfinder.MemberTypeSubItemFinder,
            "doxygendef" : compoundfinder.DoxygenTypeSubItemFinder,
            "compounddef" : compoundfinder.CompoundDefTypeSubItemFinder,
            "sectiondef" : compoundfinder.SectionDefTypeSubItemFinder,
            "memberdef" : compoundfinder.MemberDefTypeSubItemFinder,
            }

        return DoxygenItemFinderFactory(finders, project_info)



