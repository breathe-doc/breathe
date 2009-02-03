
from docutils import nodes

class doxygenclass(nodes.General, nodes.Element):
    pass

class doxygenfunction(nodes.General, nodes.Element):
    pass

def setup(app):

    app.add_directive("doxygenclass", doxygenclass_directive,  0, (0,0) )
    app.add_directive("doxygenfunction", doxygenfunction_directive,  0, (0,0) )



