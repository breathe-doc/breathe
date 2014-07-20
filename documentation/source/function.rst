
.. _function-example:

doxygenfunction Directive Example
=================================

This directive generates the appropriate output for a single function. The
function name, including namespace,  is required to be unique in the project.

For functions which have a declaration and definition in separate files, doxygen
generates two entries for the function and Breathe can get confused when faced
with this. As a result Breathe ignores what it considers to be the
implementation files when searching for the XML for the function documentation.
In order to do this, it ignores any entries in files which have filename
extensions listed in the :ref:`breathe_implementation_filename_extensions
<breathe-implementation-filename-extensions>` config variable.

Working Example
---------------

This should work::

   .. doxygenfunction:: open
      :project: structcmd

It produces this output:

.. doxygenfunction:: open
   :project: structcmd
   :no-link:

Separated Declaration & Implementation Example
----------------------------------------------

This should work::

   .. doxygenfunction:: open_di
      :project: decl_impl

It produces this output:

.. doxygenfunction:: open_di
   :project: decl_impl
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygenfunction:: made_up_function
      :project: structcmd

It produces the following warning message:

.. warning:: doxygenfunction: Cannot find function "made_up_function" in doxygen xml output

