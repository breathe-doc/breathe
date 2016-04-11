
class RenderContext(object):

    def __init__(self, node_stack, mask_factory, directive_args, domain='', child=False):
        self.node_stack = node_stack
        self.mask_factory = mask_factory
        self.directive_args = directive_args
        self.domain = domain
        self.child = child

    def create_child_context(self, data_object):

        node_stack = self.node_stack[:]
        node_stack.insert(0, self.mask_factory.mask(data_object))
        return RenderContext(node_stack, self.mask_factory, self.directive_args, self.domain, True)
