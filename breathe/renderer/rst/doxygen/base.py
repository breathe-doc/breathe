
class Renderer(object):

    def __init__(self,
            project_info,
            data_object,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler
            ):

        self.project_info = project_info
        self.data_object = data_object
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.domain_handler = domain_handler
        self.target_handler = target_handler


