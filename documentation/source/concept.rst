
.. _concept-example:

doxygenconcept Directive Example
================================

.. warning::
   C++20 Concepts support was added in Doxygen v1.9.2. Please be sure to use Doxygen v1.9.2 or
   newer with :ref:`doxygenconcept`.

Working Example
---------------

This should work:

.. code-block:: rst

   .. doxygenconcept:: Hashable
      :project: cpp_concept

It produces this output:

.. ifconfig:: doxygen_version < (1, 9, 2)

   .. error::
      The Doxygen version used to generate these docs does not support C++20 Concepts.
      Please upgrade to using Doxygen v1.9.2 or newer.

.. ifconfig:: doxygen_version > (1, 9, 1)

   .. doxygenconcept:: Hashable
      :project: cpp_concept

Failing Example
---------------

This intentionally fails:

.. code-block:: rst

   .. doxygenconcept:: MadeUpConcept
      :project: cpp_concept

It produces the following warning message:

.. warning::
   doxygenconcept: Cannot find concept "MadeUpConcept" in doxygen xml output
