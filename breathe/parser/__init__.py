
import breathe.parser.doxygen.index
import breathe.parser.doxygen.compound
import os

class ParserError(Exception):
    pass

class Parser(object):

    def __init__(self, cache, path_handler):

        self.cache = cache
        self.path_handler = path_handler


class DoxygenIndexParser(Parser):

    def parse(self, project_info):

        filename = self.path_handler.join(project_info.path(), "index.xml")

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

    def __init__(self, cache, path_handler, project_info):
        Parser.__init__(self, cache, path_handler)

        self.project_info = project_info

    def parse(self, refid):

        filename = self.path_handler.join(self.project_info.path(), "%s.xml" % refid)

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

    def __init__(self, cache, path_handler):

        self.cache = cache
        self.path_handler = path_handler

    def create_index_parser(self):

        return DoxygenIndexParser(self.cache, self.path_handler)

    def create_compound_parser(self, project_info):

        return DoxygenCompoundParser(self.cache, self.path_handler, project_info)



