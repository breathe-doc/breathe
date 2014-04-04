
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

Example with Namespace
----------------------

This should work::

   .. doxygentypedef:: foo::ns::MyInt
      :project: namespacefile

It produces this output:

.. doxygentypedef:: foo::ns::MyInt
   :project: namespacefile
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygentypedef:: made_up_typedef
      :project: restypedef

It produces the following warning message:

.. warning:: doxygentypedef: Cannot find typedef "made_up_typedef" in doxygen xml output

