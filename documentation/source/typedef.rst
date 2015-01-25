
.. _typedef-example:

doxygentypedef Directive Example
================================

Working Example
---------------

This should work::

   .. doxygentypedef:: UINT32
      :project: structcmd

It produces this output:

.. doxygentypedef:: UINT32
  :project: structcmd
  :no-link:

Example with Namespace
----------------------

This should work::

   .. doxygentypedef:: foo::ns::MyInt
      :project: namespace

It produces this output:

.. doxygentypedef:: foo::ns::MyInt
   :project: namespace
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygentypedef:: made_up_typedef
      :project: restypedef

It produces the following warning message:

.. warning:: doxygentypedef: Cannot find typedef "made_up_typedef" in doxygen xml output

