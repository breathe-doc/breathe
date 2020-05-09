from docutils import nodes


class _TargetHandler(object):
    def __init__(self, project_info, document):
        self.project_info = project_info
        self.document = document

    def create_target(self, id_):
        """Creates a target node and registers it with the document and returns it in a list"""

        target = nodes.target(ids=[id_], names=[id_])
        try:
            self.document.note_explicit_target(target)
        except Exception:
            # TODO: We should really return a docutils warning node here
            print("Warning: Duplicate target detected: %s" % id_)
        return [target]


class _NullTargetHandler(object):
    def create_target(self, refid):
        return []


def create_target_handler(options, project_info, document):
    if "no-link" in options:
        return _NullTargetHandler()
    return _TargetHandler(project_info, document)
