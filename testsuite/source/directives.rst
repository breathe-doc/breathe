
Directives
==========

These directives are a work in progress and may change in syntax as the project
develops.

In each case the ``project`` and ``path`` options have the following meaning.

Where:

``project``
   Specifies which project, as defined in the breathe_projects config value,
   should be used for this directive. This overrides the default project if one
   has been specified.

``path``
   Directly specifies the path to the folder with the doxygen output. This
   overrides the project and default project if they have bee specified.


doxygenindex Directive
~~~~~~~~~~~~~~~~~~~~~~

This directive processes and produces output for everything described by the
Doxygen xml output. It reads the ``index.xml`` file and process everything
referenced by it.

::

   .. doxygenindex::
      :project: ...
      :path: ...

doxygenfunction Directive
~~~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single function. The
function name is required to be unique in the project.

::

   .. doxygenfunction:: <function name>
      :project: ...
      :path: ...

doxygenstruct Directive
~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single struct. The struct
name is required to be unique in the project.

::

   .. doxygenstruct:: <struct name>
      :project: ...
      :path: ...

doxygenenum Directive
~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single enum. It behaves
the same as the doxygenstruct directive.

::

   .. doxygenenum:: <enum name>
      :project: ...
      :path: ...

doxygentypedef Directive
~~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single typedef. It behaves
the same as the doxygenstruct directive.

::

   .. doxygentypedef:: <typedef name>
      :project: ...
      :path: ...

doxygenclass Directive
~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single class. It behaves
the same as the doxygenstruct directive.

::

   .. doxygenclass:: <class name>
      :project: ...
      :path: ...



Config Values
-------------

**breathe_projects**
   This should be a dictionary in which the keys are project names and the values are
   paths to the folder containing the doxygen output for that project.

**breathe_default_project**
   This should match one of the keys in the **breathe_projects** dictionary and
   indicates which project should be used when the project is not specified on
   the directive.


Example pages
-------------

.. toctree::
   :maxdepth: 1

   function
   struct
   typedef
   enum
   class

