
.. _function-example:

doxygenfunction Directive Example
=================================

Working Example
---------------

This should work::

   .. doxygenfunction:: open
      :project: structcmd

It produces this output:

.. doxygenfunction:: open
   :project: structcmd

Failing Example
---------------

This intentionally fails::

   .. doxygenfunction:: made_up_function
      :project: structcmd

It produces the following warning message:

.. warning:: doxygenfunction: Cannot find function "made_up_function" in doxygen xml output

