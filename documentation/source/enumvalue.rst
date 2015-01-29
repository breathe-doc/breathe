
.. _enumvalue-example:

doxygenenumvalue Directive Example
==================================

Working Example
---------------

This should work::

   .. doxygenenumvalue:: TIXML_NO_ERROR
      :project: tinyxml

It produces this output:

.. doxygenenumvalue:: TIXML_NO_ERROR
  :project: tinyxml
  :no-link:

Example with Namespace
----------------------

This should work::

   .. doxygenenumvalue:: foo::ns::A
      :project: namespace

It produces this output:

.. doxygenenumvalue:: foo::ns::A
   :project: namespace
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygenenumvalue:: made_up_enumvalue
      :project: restypedef

It produces the following warning message:

.. warning:: doxygenenumvalue: Cannot find enumvalue "made_up_enumvalue" in doxygen xml output

