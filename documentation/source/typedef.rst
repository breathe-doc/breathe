
.. _typedef-example:

doxygentypedef Directive Example
================================

Working Example
---------------

.. cpp:namespace:: @ex_typedef_example

This should work::

   .. doxygentypedef:: UINT32
      :project: structcmd

It produces this output:

.. doxygentypedef:: UINT32
  :project: structcmd

Example with Namespace
----------------------

.. cpp:namespace:: @ex_typedef_namespace

This should work::

   .. doxygentypedef:: foo::ns::MyInt
      :project: namespace

It produces this output:

.. doxygentypedef:: foo::ns::MyInt
   :project: namespace

Failing Example
---------------

.. cpp:namespace:: @ex_typedef_failing

This intentionally fails::

   .. doxygentypedef:: made_up_typedef
      :project: restypedef

It produces the following warning message:

.. warning:: doxygentypedef: Cannot find typedef "made_up_typedef" in doxygen xml output

