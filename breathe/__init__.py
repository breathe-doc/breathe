
from docutils import nodes
from docutils.parsers.rst.directives import unchanged_required

import os

from docutils.parsers import rst
import breathe.doxparsers.index
import breathe.doxparsers.compound

# Directives
# ----------

class DoxygenIndexDirective(rst.Directive):

    required_arguments = 0
    optional_arguments = 1
    option_spec = { "path" : unchanged_required }
    has_content = False 

    def run(self):

        path = self.options["path"]

        index_file = os.path.join(path, "index.xml")

        root_object = doxparsers.index.parse( index_file )

        return root_object.rst_nodes(path)

# Setup
# -----

def setup(app):

    app.add_directive(
            "doxygenindex",
            DoxygenIndexDirective,
            )

    app.add_config_value("breathe_path", [], True)




