
.. _enumvalue-example:

doxygenenumvalue Directive Example
==================================

Working Example
---------------

.. cpp:namespace:: @ex_enumvalue_example

This should work:

.. code-block:: rst

   .. doxygenenumvalue:: TIXML_NO_ERROR
      :project: tinyxml

It produces this output:

.. doxygenenumvalue:: TIXML_NO_ERROR
  :project: tinyxml

Example with Namespace
----------------------

.. cpp:namespace:: @ex_enumvalue_namespace

This should work:

.. code-block:: rst

   .. doxygenenumvalue:: foo::ns::A
      :project: namespace

It produces this output:

.. doxygenenumvalue:: foo::ns::A
   :project: namespace

Failing Example
---------------

.. cpp:namespace:: @ex_enumvalue_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenenumvalue:: made_up_enumvalue
      :project: restypedef

It produces the following warning message:

.. warning::
   doxygenenumvalue: Cannot find enumvalue "made_up_enumvalue" in doxygen xml output
