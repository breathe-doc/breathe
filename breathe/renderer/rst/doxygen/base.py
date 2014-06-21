
class Renderer(object):

    def __init__(self,
            project_info,
            context,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler
            ):

        self.project_info = project_info
        self.context = context
        self.data_object = context.node_stack[0]
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.domain_handler = domain_handler
        self.target_handler = target_handler


class RenderContext(object):

    def __init__(self, node_stack):
        self.node_stack = node_stack

    def create_child_context(self, data_object):

        node_stack = self.node_stack[:]
        node_stack.insert(0, data_object)
        return RenderContext(node_stack)
