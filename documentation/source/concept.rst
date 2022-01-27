
.. _concept-example:

doxygenconcept Directive Example
================================

Working Example
---------------

This should work::

   .. doxygenconcept:: Hashable
      :project: cpp_concept

It produces this output:

.. doxygenconcept:: Hashable
  :project: cpp_concept

Failing Example
---------------

This intentionally fails::

   .. doxygenconcept:: MadeUpConcept
      :project: cpp_concept

It produces the following warning message:

.. warning:: doxygenconcept: Cannot find concept "MadeUpConcept" in doxygen xml output

