import inspect

class Renderer(object):

    def __init__(self,
            project_info,
            data_object,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler,
            rendering_filter,
            ):

        self.project_info = project_info
        self.data_object = data_object
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.domain_handler = domain_handler
        self.target_handler = target_handler
        self.rendering_filter = rendering_filter

    def render(self):
        return []

    def continue_rendering(self, context=''):
        return self.rendering_filter.continue_rendering(self, inspect.stack()[1][3], context)
