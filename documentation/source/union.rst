
.. _union-example:

doxygenunion Directive Example
==============================

Working Example
---------------

.. cpp:namespace:: @ex_union_example

This should work::

   .. doxygenunion:: SeparateUnion
      :project: union

It produces this output:

.. doxygenunion:: SeparateUnion
  :project: union

Example with Namespace
----------------------

.. cpp:namespace:: @ex_union_namespace

This should work::

   .. doxygenunion:: foo::MyUnion
      :project: union

It produces this output:

.. doxygenunion:: foo::MyUnion
   :project: union

Failing Example
---------------

.. cpp:namespace:: @ex_union_failing

This intentionally fails::

   .. doxygenunion:: made_up_union
      :project: union

It produces the following warning message:

.. warning:: doxygenunion: Cannot find union "made_up_union" in doxygen XML
   output for project "union" from directory: ../../examples/specific/union/xml/

