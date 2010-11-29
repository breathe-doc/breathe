
Directives & Config Variables
=============================

.. toctree::
   :hidden:

   function
   struct
   class
   enum
   typedef

The available directives are shown below. In each case the ``project`` and
``path`` options have the following meaning:  

``project``
   Specifies which project, as defined in the breathe_projects config value,
   should be used for this directive. This overrides the default project if one
   has been specified.

``path``
   Directly specifies the path to the folder with the doxygen output. This
   overrides the project and default project if they have been specified.

.. _doxygenindex:

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

Checkout the :ref:`example <function-example>` to see it in action.

doxygenstruct Directive
~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single struct. The struct
name is required to be unique in the project.

::

   .. doxygenstruct:: <struct name>
      :project: ...
      :path: ...

Checkout the :ref:`example <function-example>` to see it in action.

doxygenenum Directive
~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single enum. It behaves
the same as the doxygenstruct directive.

::

   .. doxygenenum:: <enum name>
      :project: ...
      :path: ...

Checkout the :ref:`example <enum-example>` to see it in action.

doxygentypedef Directive
~~~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single typedef. It behaves
the same as the doxygenstruct directive.

::

   .. doxygentypedef:: <typedef name>
      :project: ...
      :path: ...

Checkout the :ref:`example <typedef-example>` to see it in action.

.. _doxygenclass:

doxygenclass Directive
~~~~~~~~~~~~~~~~~~~~~~

This directive generates the appropriate output for a single class. It behaves
the same as the doxygenstruct directive.

::

   .. doxygenclass:: <class name>
      :project: ...
      :path: ...

Checkout the :ref:`example <class-example>` to see it in action.


Config Values
-------------

.. confval:: breathe_projects

   This should be a dictionary in which the keys are project names and the values are
   paths to the folder containing the doxygen output for that project.

.. confval:: breathe_default_project

   This should match one of the keys in the :confval:`breathe_projects` dictionary and
   indicates which project should be used when the project is not specified on
   the directive.

.. confval:: breathe_domain_by_extension

   Allows you to specify domains for particular files according to their
   extension.

   For example::

      breathe_domain_by_extension = {
              "h" : "cpp",
              }

.. confval:: breathe_domain_by_file_pattern

   Allows you to specify domains for particular files by wildcard syntax. This
   is checked after :confval:`breathe_domain_by_extension` and so will override
   it when necessary.

   For example::

      breathe_domain_by_file_pattern = {
              "\*/alias.h" : "c",
              }

   If you wanted all ``.h`` header files to be treated as being in the **cpp**
   domain you might use the :confval:`breathe_domain_by_extension` example
   above. But if you had one ``.h`` file that should be treated as being in the
   **c** domain then you can override as above.


