
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
