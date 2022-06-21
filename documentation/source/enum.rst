
.. _enum-example:

doxygenenum Directive Example
===============================

Working Example
---------------

.. cpp:namespace:: @ex_enum_example

This should work:

.. code-block:: rst

   .. doxygenenum:: NodeType
      :project: tinyxml

It produces this output:

.. doxygenenum:: NodeType
  :project: tinyxml

Example with Namespace
----------------------

.. cpp:namespace:: @ex_enum_namespace

This should work:

.. code-block:: rst

   .. doxygenenum:: foo::ns::Letters
      :project: namespace

It produces this output:

.. doxygenenum:: foo::ns::Letters
   :project: namespace

Failing Example
---------------

.. cpp:namespace:: @ex_enum_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenenum:: made_up_enum
      :project: restypedef

It produces the following warning message:

.. warning::
   doxygenenum: Cannot find enum "made_up_enum" in doxygen xml output
