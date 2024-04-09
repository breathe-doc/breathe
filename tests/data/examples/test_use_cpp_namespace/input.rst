.. doxygenclass:: ClassA

.. cpp:namespace-push:: Namespace

.. doxygenvariable:: Var

.. doxygenclass:: ClassB
    :members:
    :undoc-members:

.. cpp:namespace-push:: ClassB

.. doxygenfunction:: SomeFunc

.. doxygendefine:: SOME_MACRO

.. doxygenenum:: NestedStruct::SomeEnum

.. cpp:namespace-pop::

.. doxygenstruct:: ClassB::NestedStruct

.. doxygentypedef:: SomeType

.. doxygenconcept:: SomeConcept

.. doxygenconcept:: ClassB::NestedConcept

.. doxygenvariable:: ClassB::MemberVar

.. doxygenvariable:: ClassC::SpecialVarA


.. Superfluous spaces added deliberately for testing

.. doxygenvariable:: ClassC<   unsigned  long  >::SpecialVarA

.. cpp:namespace-push:: ClassC<  unsigned   long   >

.. doxygenvariable:: SpecialVarB