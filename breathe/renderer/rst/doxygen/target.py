
class TargetHandler(object):

    def __init__(self, project_info, node_factory, document):

        self.project_info = project_info
        self.node_factory = node_factory
        self.document = document

    def create_target(self, refid):

        target = self.node_factory.target(refid=refid, ids=[refid], names=[refid])

        # Tell the document about our target
        try:
            self.document.note_explicit_target(target)
        except Exception, e:
            print "Failed to register id: %s. This is a seemingly harmless bug." % refid

        return [target]

class NullTargetHandler(object):

    def create_target(self, refid):
        return []


class TargetHandlerFactory(object):

    def __init__(self, node_factory):

        self.node_factory = node_factory

    def create(self, options, project_info, document):

        if options.has_key("no-link"):
            return NullTargetHandler()

        return TargetHandler(project_info, self.node_factory, document)

