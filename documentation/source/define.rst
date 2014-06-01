
.. _define-example:

doxygendefine Directive Example
===============================

Working Example
---------------

This should work::

   .. doxygendefine:: WRITE_TREE_MISSING_OK
      :project: c_file

It produces this output:

.. doxygendefine:: WRITE_TREE_MISSING_OK
  :project: c_file

Failing Example
---------------

This intentionally fails::

   .. doxygendefine:: MADEUPDEFINE
      :project: define

It produces the following warning message:

.. warning:: doxygendefine: Cannot find define "MADEUPDEFINE" in doxygen xml
             output for project "define" in directory: ../../examples/specific/define/xml

