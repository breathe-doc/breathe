
.. _enum-example:

doxygenenum Directive Example
===============================

Working Example
---------------

This should work::

   .. doxygenenum:: NodeType
      :project: tinyxml

It produces this output:

.. doxygenenum:: NodeType
  :project: tinyxml

Failing Example
---------------

This intentionally fails::

   .. doxygenenum:: made_up_enum
      :project: restypedef

It produces the following warning message:

.. warning:: doxygenenum: Cannot find enum "made_up_enum" in doxygen xml output

