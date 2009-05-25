
Breathe Specification
=====================




Directives
----------

In each case the ``project`` and ``path`` options have the following meaning.

Where:

``project``
   Specifies which project, as defined in the breathe_projects config value,
   should be used for this directive. This overrides the default project if one
   has been specified.

``path``
   Directly specifies the patht to the folder with the doxygen output. This
   overrides the project and default project if they have bee specified.



doxygenindex
~~~~~~~~~~~~

This will generate output for everything referenced by a Doxygen ``index.xml``
file. The syntax is::

   .. doxygenindex::
      :project: ...
      :path: ...

doxygenclass
~~~~~~~~~~~~

This will generate output for a single class. The syntax is::

   .. doxygenclass:: <class name>
      :project: ...
      :path: ...


doxygenfunction
~~~~~~~~~~~~~~~

This will generate output for a single function. The syntax is::

   .. doxygenfunction:: <function name>
      :project: ...
      :path: ...


Config Variables
~~~~~~~~~~~~~~~~

**breathe_projects**
   This should be a dictionary in which the keys are project names and the values are
   paths to the folder containing the doxygen output for that project.

**breathe_default_project**
   This should match one of the keys in the **breathe_projects** dictionary and
   indicates which project should be used when the project is not specified on
   the directive.


Roles
-----

No restructured text roles are planned.

Nodes
-----

No additional nodes are planned.

References 
----------

All interesting atoms of data should output references by which they can be
linked to from other parts of the documentation.

