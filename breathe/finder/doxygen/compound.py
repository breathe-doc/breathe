
from breathe.finder.doxygen.base import ItemFinder 

class DoxygenTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef)
        return compound_finder.find(matcher_stack)

class CompoundDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        results = []
        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            results.extend(finder.find(matcher_stack))

        return results

        
class SectionDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        results = []
        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            results.extend(finder.find(matcher_stack))

        return results

class MemberDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        if matcher_stack.match("member", self.data_object):
            return [self.data_object]
        else:
            return []

