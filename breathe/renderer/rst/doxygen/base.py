
class Renderer(object):

    def __init__(self,
            project_info,
            context,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler,
            domain_directive_factories
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
        self.domain_directive_factories = domain_directive_factories

    def create_template_node(self, decl):
        """Creates a node for the ``template <...>`` part of the declaration."""
        if not decl.templateparamlist:
            return None
        context = self.context.create_child_context(decl.templateparamlist)
        renderer = self.renderer_factory.create_renderer(context)
        nodes = [self.node_factory.Text("template <")]
        nodes.extend(renderer.render())
        nodes.append(self.node_factory.Text(">"))
        signode = self.node_factory.desc_signature()
        signode.extend(nodes)
        return signode


class RenderContext(object):

    def __init__(self, node_stack, mask_factory):
        self.node_stack = node_stack
        self.mask_factory = mask_factory

    def create_child_context(self, data_object):

        node_stack = self.node_stack[:]
        node_stack.insert(0, self.mask_factory.mask(data_object))
        return RenderContext(node_stack, self.mask_factory)
