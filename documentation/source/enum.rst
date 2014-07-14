
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
  :no-link:

Example with Namespace
----------------------

This should work::

   .. doxygenenum:: foo::ns::Letters
      :project: namespace

It produces this output:

.. doxygenenum:: foo::ns::Letters
   :project: namespace
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygenenum:: made_up_enum
      :project: restypedef

It produces the following warning message:

.. warning:: doxygenenum: Cannot find enum "made_up_enum" in doxygen xml output

