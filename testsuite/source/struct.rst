
.. _struct-example:

doxygenstruct Directive Example
===============================

Example with Full Description
-----------------------------

This should work::

   .. doxygenstruct:: CoordStruct
      :project: restypedef

It produces this output:

.. doxygenstruct:: CoordStruct
   :project: restypedef


Example with Outline
--------------------

This should work::

   .. doxygenstruct:: CoordStruct
      :project: restypedef
      :outline:

It produces this output:

.. doxygenstruct:: CoordStruct
   :project: restypedef
   :outline:
   :no-link:


Failing Example
---------------

This intentionally fails::

   .. doxygenstruct:: made_up_struct
      :project: restypedef

It produces the following warning message:

.. warning:: doxygenstruct: Cannot find struct "made_up_struct" in doxygen xml output

