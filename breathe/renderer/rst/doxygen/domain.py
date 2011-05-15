

class DomainHelper(object):
    pass

class NullDomainHelper(DomainHelper):
    pass

class CppDomainHelper(DomainHelper):

    def __init__(self, definition_parser, substitute):

        self.definition_parser = definition_parser
        self.substitute = substitute

        self.duplicates = {}

    def check_cache(self, _id):
        try:
            return True, self.duplicates[_id]
        except KeyError:
            return False, ""

    def cache(self, _id, project_info):
        self.duplicates[_id] = project_info

    def remove_word(self, word, definition):
        return self.substitute(r"(\s*\b|^)%s\b\s*" % word, "", definition)


class CDomainHelper(DomainHelper):

    def __init__(self):

        self.duplicates = set()

    def is_duplicate(self, name):
        return name in self.duplicates

    def remember(self, name):
        self.duplicates.add(name)



class DomainHandler(object):

    def __init__(self, node_factory, document, env, helper, project_info):

        self.node_factory = node_factory
        self.document = document
        self.env = env
        self.helper = helper
        self.project_info = project_info

class NullDomainHandler(DomainHandler):

    def __init__(self):
        pass

    def create_function_id(self, data_object):
        return ""

    def create_function_target(self, data_object):
        pass

    def create_class_id(self, data_object):
        return ""

    def create_class_target(self, data_object):
        pass

class CDomainHandler(DomainHandler):

    def create_function_id(self, data_object):

        name = data_object.definition.split()[-1]

        return name

    def create_function_target(self, data_object):

        name = data_object.definition.split()[-1]

        if self.helper.is_duplicate(name):
            print ( "Warning: Ignoring duplicate '%s'. As C does not support overloaded "
                    "functions. Perhaps you should be using the cpp domain?" % name )
            return

        self.helper.remember(name)

        signode = self.node_factory.desc_signature()

        signode["names"].append(name)
        signode["ids"].append(name)

        self.document.note_explicit_target(signode)

        inv = self.env.domaindata['c']['objects']
        if name in inv:
            self.env.warn(
                self.env.docname,
                'duplicate C object description of %s, ' % name +
                'other instance in ' + self.env.doc2path(inv[name][0]),
                self.lineno)
        inv[name] = (self.env.docname, "function")


class CppDomainHandler(DomainHandler):

    def create_class_id(self, data_object):

        def_ = data_object.name

        parser = self.helper.definition_parser(def_)
        sigobj = parser.parse_class()

        return sigobj.get_id()

    def create_class_target(self, data_object):

        _id = self.create_class_id(data_object)

        in_cache, project = self.helper.check_cache(_id)
        if in_cache:
            print "Warning: Ignoring duplicate domain reference '%s'. " \
                  "First found in project '%s'" % (_id, project.reference())
            return

        self.helper.cache(_id, self.project_info)

        signode = self.node_factory.desc_signature()

        signode["names"].append(_id)
        signode["ids"].append(_id)

        name = data_object.name
        self.document.settings.env.domaindata['cpp']['objects'].setdefault(name,
                (self.document.settings.env.docname, "class", _id))

        self.document.note_explicit_target(signode)

    def create_function_id(self, data_object):

        definition = self.helper.remove_word("virtual", data_object.definition)
        argstring = data_object.argsstring

        explicit = "explicit " if data_object.explicit == "yes" else ""

        def_ = "%(explicit)s%(definition)s%(argstring)s" % {
                        "explicit" : explicit,
                        "definition" : definition,
                        "argstring" : argstring,
                    }

        parser = self.helper.definition_parser(def_)
        sigobj = parser.parse_function()

        return sigobj.get_id()

    def create_function_target(self, data_object):

        _id = self.create_function_id(data_object)

        in_cache, project = self.helper.check_cache(_id)
        if in_cache:
            print "Warning: Ignoring duplicate domain reference '%s'. " \
                  "First found in project '%s'" % (_id, project.reference())
            return

        self.helper.cache(_id, self.project_info)

        signode = self.node_factory.desc_signature()

        signode["names"].append(_id)
        signode["ids"].append(_id)

        name = data_object.definition.split()[-1]
        self.document.settings.env.domaindata['cpp']['objects'].setdefault(name,
                (self.document.settings.env.docname, "function", _id))

        self.document.note_explicit_target(signode)


class DomainHandlerFactory(object):

    def __init__(self, project_info, node_factory, document, env, helpers):

        self.project_info = project_info
        self.node_factory = node_factory
        self.document = document
        self.env = env
        self.domain_helpers = helpers

    def create_null_domain_handler(self):

        return NullDomainHandler()

    def create_domain_handler(self, file_):

        domains_handlers = {
                "c" : CDomainHandler,
                "cpp" : CppDomainHandler,
                }

        domain = self.project_info.domain_for_file(file_)

        try:
            helper = self.domain_helpers[domain]
        except KeyError:
            helper = NullDomainHelper()

        try:
            return domains_handlers[domain](self.node_factory, self.document, self.env, helper, self.project_info)
        except KeyError:
            return NullDomainHandler()

class NullDomainHandlerFactory(object):

    def create_null_domain_handler(self):

        return NullDomainHandler()

    def create_domain_handler(self, file_):

        return NullDomainHandler()

class DomainHandlerFactoryCreator(object):

    def __init__(self, node_factory, helpers):

        self.node_factory = node_factory
        self.helpers = helpers

    def create_domain_handler_factory(self, project_info, document, env, options):

        if "no-link" in options:
            return NullDomainHandlerFactory()

        return DomainHandlerFactory(project_info, self.node_factory, document, env, self.helpers)

