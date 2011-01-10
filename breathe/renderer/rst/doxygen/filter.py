from breathe.renderer.rst.doxygen.compound import CompoundDefTypeSubRenderer, FuncMemberDefTypeSubRenderer, EnumMemberDefTypeSubRenderer, VariableMemberDefTypeSubRenderer

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



# Rendering filters
# -----------------


class RenderingFilter(object):
    
    filter_rules = []
    
    def match_rule(self, renderer, callee='', context=''):
        ''' Runs through all rules, returns False upon match.
        
            renderer - Renderer instance
            callee  - Caller method
            context - Context within caller method
        '''
        
        for rule in self.filter_rules:
            if rule[0] and not isinstance(renderer, rule[0]):
                continue
            if rule[1] and (rule[1] != callee):
                continue
            if rule[2] and (rule[2] != context):
                continue
            
            self.print_trace(renderer, callee, context, False)
            return False
        
        # None of the rules matched
        self.print_trace(renderer, callee, context, True)
        return True
    
    def print_trace(self, renderer, callee, context, status):
        ''' Prints a stack trace of matches
        
            renderer - Renderer instance
            callee  - Caller method
            context - Context within caller method
        '''
        
        message = '%s: %s' % (renderer.__class__.__name__, callee)
        if context:
            message = "%s@%s" % (message, context)
        if not status:
            print '  [!!]  %s' % message
        print ' [OK]  %s' % message
    
    def continue_rendering(self, renderer, callee='', context=''):
        return self.match_rule(renderer, callee, context)

class NullRenderingFilter(RenderingFilter):
    def continue_rendering(self, renderer, callee='', context=''):
        return True

class OutlineRenderingFilter(RenderingFilter):
    ''' Filters out all descriptions, in order to display a compact outline '''
    
    filter_rules = [
        (CompoundDefTypeSubRenderer,       'render',      'description'),
        (FuncMemberDefTypeSubRenderer,     'description', ''),
        (EnumMemberDefTypeSubRenderer,     'description', ''),
        (VariableMemberDefTypeSubRenderer, 'description', ''),
        ]

class RenderingFilterCollection(RenderingFilter):
    pass

class RenderingFilterFactory(object):
    def create_filter(self, options):
        if options.has_key('outline'):
            return OutlineRenderingFilter()
        return NullRenderingFilter()