
.. _variable-example:

doxygenvariable Directive Example
=================================

Working Example
---------------

This should work::

   .. doxygenvariable:: global_cache_tree
      :project: c_file

It produces this output:

.. doxygenvariable:: global_cache_tree
  :project: c_file

Failing Example
---------------

This intentionally fails::

   .. doxygenvariable:: made_up_variable
      :project: define

It produces the following warning message:

.. warning:: doxygenvariable: Cannot find variable “made_up_variable” in doxygen XML output for project “tinyxml” from directory: ../../examples/tinyxml/tinyxml/xml/
