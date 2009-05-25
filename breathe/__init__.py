
from docutils import nodes
from docutils.parsers.rst.directives import unchanged_required

import os
import sys
import copy

from docutils.parsers import rst
import breathe.doxparsers.index
import breathe.doxparsers.compound

class ElementDescription(object):

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


class DoxygenBase(object):

    def get_path(self):

        index_path = DoxygenBase.projects[ DoxygenBase.default_project ]

        if self.options.has_key("project"):
            try:
                index_path = DoxygenBase.projects[ self.options["project"] ]
            except KeyError, e:
                sys.stderr.write(
                        "Unable to find project '%s' in breathe_projects dictionary" % self.options["project"]
                        )

        if self.options.has_key("path"):
            index_path = self.options["path"]

        return index_path



# Directives
# ----------

class DoxygenIndexDirective(rst.Directive, DoxygenBase):

    required_arguments = 0
    optional_arguments = 2
    option_spec = {
            "path" : unchanged_required,
            "project" : unchanged_required,
            }
    has_content = False 

    def run(self):

        index_path = self.get_path()

        index_file = os.path.join(index_path, "index.xml")

        root_object = doxparsers.index.parse( index_file )

        return root_object.rst_nodes(index_path)


class DoxygenFunctionDirective(rst.Directive, DoxygenBase):

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
            "path" : unchanged_required,
            "project" : unchanged_required,
            }
    has_content = False 

    def run(self):

        function_name = self.arguments[0]

        index_path = self.get_path()
        index_file = os.path.join(index_path, "index.xml")

        root_object = doxparsers.index.parse( index_file )

        # Find function in the index file
        details = ElementDescription(name=function_name, kind="function")
        results = root_object.find_compounds_and_members( details )

        if not results:
            warning = 'doxygenfunction: Cannot find function "%s" in doxygen xml output' % function_name
            return [ nodes.warning( "", nodes.paragraph("", "", nodes.Text(warning))),
                    self.state.document.reporter.warning( warning, line=self.lineno) ]

        objects = []

        # Find functions in files suggested by index
        for entry in results:

            ref_xml_path = os.path.join( index_path, "%s.xml" % entry[0].refid )
            root_object = breathe.doxparsers.compound.parse( ref_xml_path )

            for memberdef in entry[1]:
                
                criteria = copy.deepcopy(details)
                criteria.refid = memberdef.refid

                objects.append(root_object.find(criteria))

        if not objects:
            warning = 'doxygenfunction: Cannot find %s in doxygen xml output' % function_name
            return [ self.state.document.reporter.warning( warning, line=self.lineno) ]

        elif len( objects ) > 1:
            warning =  'doxygenfunction: Found multiple matches for "%s" in doxygen xml output.' % function_name
            warning += '                 Please be more specific.'
            return [ self.state.document.reporter.warning( warning, line=self.lineno) ]


        return objects[0].rst_nodes()



def get_config_values(app):

    DoxygenBase.projects = app.config.breathe_projects
    DoxygenBase.default_project = app.config.breathe_default_project


# Setup
# -----

def setup(app):

    app.add_directive(
            "doxygenindex",
            DoxygenIndexDirective,
            )

    app.add_directive(
            "doxygenfunction",
            DoxygenFunctionDirective,
            )

    app.add_config_value("breathe_projects", {}, True)
    app.add_config_value("breathe_default_project", "", True)

    app.connect("builder-inited", get_config_values)

