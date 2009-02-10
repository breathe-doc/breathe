
from docutils import nodes
from docutils.parsers.rst.directives import unchanged_required

import os

import doxparsers.index as index

# Nodes
# -----

class DoxygenClass(nodes.General, nodes.Element):

    @staticmethod
    def visit(visitor, node):
        visitor.body.append(node.name)

    @staticmethod
    def depart(visitor, node):
        pass


class DoxygenIndex(nodes.General, nodes.Element):

    @staticmethod
    def visit(visitor, node):
        for cls in node.classes:
            visitor.body.append(cls + " ")

    @staticmethod
    def depart(visitor, node):
        pass




class DoxygenFunction(nodes.General, nodes.Element):
    pass

# Directives
# ----------

def doxygenclass_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):

    classname = arguments[0]

    node = DoxygenClass(block_text)

    node.name = classname

    return [node]


def doxygenindex_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):

    # node = DoxygenIndex(block_text)

    # node.classes = []

    path = options["path"]

    index_file = os.path.join(path, "index.xml")

    root_object = index.parse( index_file )

    new_nodes = []

    for entry in root_object.compound:
        if entry.get_kind() == "class":
            cls = nodes.emphasis(text="class")
            name = nodes.strong(text=entry.get_name())
            new_nodes.append(nodes.paragraph("", "", cls, nodes.Text(" "), name))

    return new_nodes


def doxygenfunction_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):

    return [DoxygenFunction("")]



# Setup
# -----

def setup(app):

    app.add_directive(
            "doxygenclass",
            doxygenclass_directive,
            0,
            (1,2,0),
            path = unchanged_required,
            )

    app.add_directive(
            "doxygenindex",
            doxygenindex_directive,
            0,
            (0,1,0),
            path = unchanged_required,
            )

    app.add_node(DoxygenClass, html=(DoxygenClass.visit, DoxygenClass.depart))

    app.add_node(DoxygenIndex, html=(DoxygenIndex.visit, DoxygenIndex.depart))

    app.add_config_value("breathe_path", [], True)




