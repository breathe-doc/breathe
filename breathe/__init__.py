
from docutils import nodes

# Nodes
# -----

class DoxygenClass(nodes.General, nodes.Element):

    @staticmethod
    def visit(visitor, node):
        visitor.body.append(node.name)

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


def doxygenfunction_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):

    return [DoxygenFunction("")]



# Setup
# -----

def setup(app):

    app.add_directive("doxygenclass", doxygenclass_directive, content=0, arguments=(1,0,0))

    app.add_node(DoxygenClass, html=(DoxygenClass.visit, DoxygenClass.depart))

    app.add_config_value("breathe_path", [], True)




