
import breathe.parser.doxygen.index
import breathe.parser.doxygen.compound
import os

class ParserError(Exception):
    pass

class Parser(object):

    def __init__(self, cache, path_handler, app):

        self.cache = cache
        self.path_handler = path_handler
        self.app = app

    def store_file_state(self, filename):
        if not hasattr(self.app.env, 'file_state'):
            self.app.env.file_state = {}
        newmtime = os.path.getmtime(filename)
        mtime, docnames = self.app.env.file_state.setdefault(
            filename, (newmtime, set()))
        self.app.env.file_state[filename] = (newmtime, docnames)
        docnames.add(self.app.env.docname)

class DoxygenIndexParser(Parser):

    def __init__(self, cache, path_handler, app):
        Parser.__init__(self, cache, path_handler, app)

    def parse(self, project_info):
        filename = self.path_handler.join(project_info.path(), "index.xml")
        self.store_file_state(filename)

        try: 
            # Try to get from our cache
            return self.cache[filename]
        except KeyError:

            # If that fails, parse it afresh
            try:
                result = breathe.parser.doxygen.index.parse(filename)
                self.cache[filename] = result
                return result
            except breathe.parser.doxygen.index.ParseError:
                raise ParserError(filename)

class DoxygenCompoundParser(Parser):

    def __init__(self, cache, path_handler, project_info, app):
        Parser.__init__(self, cache, path_handler, app)

        self.project_info = project_info

    def parse(self, refid):

        filename = self.path_handler.join(self.project_info.path(), "%s.xml" % refid)
        self.store_file_state(filename)

        try: 
            # Try to get from our cache
            return self.cache[filename]
        except KeyError:

            # If that fails, parse it afresh
            try:
                result = breathe.parser.doxygen.compound.parse(filename)
                self.cache[filename] = result
                return result
            except breathe.parser.doxygen.compound.ParseError:
                raise ParserError(filename)

class CacheFactory(object):

    def create_cache(self):

        # Return basic dictionary as cache
        return {}

class DoxygenParserFactory(object):

    def __init__(self, cache, path_handler, app):

        self.cache = cache
        self.path_handler = path_handler
        self.app = app

    def create_index_parser(self):

        return DoxygenIndexParser(self.cache, self.path_handler, self.app)

    def create_compound_parser(self, project_info):

        return DoxygenCompoundParser(self.cache, self.path_handler,
                                     project_info, self.app)



