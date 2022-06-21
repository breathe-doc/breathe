
.. _variable-example:

doxygenvariable Directive Example
=================================

Working Example
---------------

.. cpp:namespace:: @ex_variable_example

This should work:

.. code-block:: rst

   .. doxygenvariable:: global_cache_tree
      :project: c_file

It produces this output:

.. doxygenvariable:: global_cache_tree
  :project: c_file

Failing Example
---------------

.. cpp:namespace:: @ex_variable_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenvariable:: made_up_variable
      :project: define

It produces the following warning message:

.. warning::
   doxygenvariable: Cannot find variable “made_up_variable” in doxygen XML output for project
   "tinyxml" from directory: ../../examples/tinyxml/tinyxml/xml/
