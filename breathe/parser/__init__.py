
import breathe.parser.doxygen.index
import breathe.parser.doxygen.compound

class ParserError(Exception):
    pass

class Parser(object):

    def __init__(self, cache, path_handler, file_state_cache):

        self.cache = cache
        self.path_handler = path_handler
        self.file_state_cache = file_state_cache

class DoxygenIndexParser(Parser):

    def __init__(self, cache, path_handler, file_state_cache):
        Parser.__init__(self, cache, path_handler, file_state_cache)

    def parse(self, project_info):

        filename = self.path_handler.join(project_info.path(), "index.xml")

        self.file_state_cache.update(filename)

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

    def __init__(self, cache, path_handler, file_state_cache, project_info):
        Parser.__init__(self, cache, path_handler, file_state_cache)

        self.project_info = project_info

    def parse(self, refid):

        filename = self.path_handler.join(self.project_info.path(), "%s.xml" % refid)

        self.file_state_cache.update(filename)

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

    def __init__(self, cache, path_handler, file_state_cache):

        self.cache = cache
        self.path_handler = path_handler
        self.file_state_cache = file_state_cache

    def create_index_parser(self):

        return DoxygenIndexParser(self.cache, self.path_handler, self.file_state_cache)

    def create_compound_parser(self, project_info):

        return DoxygenCompoundParser(
                self.cache,
                self.path_handler,
                self.file_state_cache,
                project_info
                )



