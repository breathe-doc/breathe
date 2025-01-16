
Specific Examples Test Suite
============================


Template Type Alias
-------------------

.. cpp:namespace:: @ex_specific_alias_template

.. doxygentypedef:: IsFurry
   :path: ../../examples/specific/template_type_alias/xml

.. doxygentypedef:: IsFuzzy
   :path: ../../examples/specific/template_type_alias/xml

Typedef Examples
----------------

.. cpp:namespace:: @ex_specific_typedef

.. doxygenindex::
   :path: ../../examples/specific/typedef/xml

Namespaced Function Examples
----------------------------

.. cpp:namespace:: @ex_specific_namespaced_function

.. doxygenfunction:: TestNamespaceClasses::NamespacedClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: TestNamespaceClasses::ClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: TestNamespaceClasses::ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: ClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: f0
   :path: ../../examples/specific/class/xml
.. doxygenfunction:: f0< std::string >
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: NS1::f1
   :path: ../../examples/specific/class/xml
.. doxygenfunction:: NS1::f1< std::string >
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: NS1::NS2::f2
   :path: ../../examples/specific/class/xml
.. doxygenfunction:: NS1::NS2::f2< std::string >
   :path: ../../examples/specific/class/xml


Extern Examples
---------------

.. cpp:namespace:: @ex_specific_extern_examples

.. doxygenfunction:: cache_tree_free
   :project: c_file
.. doxygenstruct:: cache_tree
   :project: c_file
   :outline:

Fixed Width Font
----------------

.. cpp:namespace:: @ex_specific_fixed_width

.. doxygenclass:: Out
   :path: ../../examples/specific/fixedwidthfont/xml
   :members:

Function Overloads
------------------

.. cpp:namespace:: @ex_specific_function_overloads

.. doxygenfunction:: f(int, int)
   :project: functionOverload

.. doxygenfunction:: f(double, double)
   :project: functionOverload

.. doxygenfunction:: test::g(int,int)
   :project: functionOverload

.. doxygenfunction:: test::g(double, double)
   :project: functionOverload

.. doxygenfunction:: h(std::string, MyType)
   :project: functionOverload

.. doxygenfunction:: h(std::string, MyOtherType)
   :project: functionOverload

.. doxygenfunction:: h(std::string, const int)
   :project: functionOverload

.. doxygenfunction:: h(std::string, const T, const U)
   :project: functionOverload

Program Listing
---------------

.. cpp:namespace:: @ex_specific_program_listing

.. doxygenclass:: Vector
   :project: programlisting

.. doxygenfunction:: center
   :project: programlisting

Image
-----

.. cpp:namespace:: @ex_specific_image

.. doxygenclass:: ImageClass
   :project: image

Array Parameter
---------------

.. doxygenfunction:: foo
   :project: array

.. doxygenfunction:: bar
   :project: array

C Struct
--------

.. doxygenfile:: c_struct.h
   :project: c_struct

C Union
-------

.. doxygenfile:: c_union.h
   :project: c_union

C Enum
------

.. doxygenenum:: GSM_BackupFormat
   :project: c_enum

C Typedef
---------

.. doxygenfile:: c_typedef.h
   :project: c_typedef

C Macro
-------

.. doxygenfile:: c_macro.h
   :project: c_macro

C++ Macro
---------

.. doxygenfile:: define.h
   :project: define

Multifile
---------

.. cpp:namespace:: @ex_specific_multifile

.. doxygenfunction:: TestTemplateFunction
   :project: multifile

Interface Class
---------------

.. cpp:namespace:: @ex_specific_interface

.. doxygeninterface:: InterfaceClass
   :project: interface

C++ Anonymous Entities
----------------------

.. cpp:namespace:: @ex_specific_cpp_anon

.. doxygenfile:: cpp_anon.h
   :project: cpp_anon

C++ Union
---------

.. cpp:namespace:: @ex_specific_cpp_union

.. doxygenfile:: cpp_union.h
   :project: cpp_union

C++ Enums
---------

.. cpp:namespace:: @ex_specific_cpp_enum

.. doxygenfile:: cpp_enum.h
   :project: cpp_enum

C++ Functions
-------------

.. cpp:namespace:: @ex_specific_cpp_function

.. doxygenfile:: cpp_function.h
   :project: cpp_function

C++ Friend Classes
------------------

.. cpp:namespace:: @ex_specific_cpp_friendclass

.. doxygenfile:: cpp_friendclass.h
   :project: cpp_friendclass

C++ Inherited Members
---------------------

.. cpp:namespace:: @ex_specific_cpp_inherited_members

.. doxygenclass:: Base
   :project: cpp_inherited_members
.. doxygenclass:: A
   :project: cpp_inherited_members
.. doxygenclass:: B
   :project: cpp_inherited_members

C++ Template Specialization with Namespace
------------------------------------------

.. cpp:namespace:: @ex_specific_cpp_ns_template_specialization

.. doxygenfile:: cpp_ns_template_specialization.h
   :project: cpp_ns_template_specialization

C++ Trailing Return Type
------------------------

.. cpp:namespace:: @ex_specific_cpp_trailing_return_type

.. doxygenfile:: cpp_trailing_return_type.h
   :project: cpp_trailing_return_type

C++ Constexpr Handling
------------------------

.. cpp:namespace:: @ex_specific_cpp_constexpr_hax

Test for issue 717.


.. doxygenfile:: cpp_constexpr_hax.h
   :project: cpp_constexpr_hax

C++ Function Lookup
-------------------

.. cpp:namespace:: @ex_specific_cpp_function_lookup

.. doxygenfunction:: fNoexcept()
   :project: cpp_function_lookup
.. doxygenfunction:: fFinal()
   :project: cpp_function_lookup
.. doxygenfunction:: fOverride()
   :project: cpp_function_lookup

This one should actually have ``[[myattr]]`` but Doxygen seems to not put attributes into the XML:

.. doxygenfunction:: fAttr()
   :project: cpp_function_lookup
.. doxygenfunction:: fFInit()
   :project: cpp_function_lookup
.. doxygenfunction:: fTrailing()
   :project: cpp_function_lookup

.. doxygenfunction:: fInit(int)
   :project: cpp_function_lookup
.. doxygenfunction:: fPlain(int)
   :project: cpp_function_lookup
.. doxygenfunction:: fPtr(int*)
   :project: cpp_function_lookup
.. doxygenfunction:: fLRef(int&)
   :project: cpp_function_lookup
.. doxygenfunction:: fRRef(int&&)
   :project: cpp_function_lookup
.. doxygenfunction:: fParamPack(T...)
   :project: cpp_function_lookup
.. doxygenfunction:: fMemPtr(int A::*)
   :project: cpp_function_lookup
.. doxygenfunction:: fParen(void (*)())
   :project: cpp_function_lookup

.. doxygenfunction:: fParenPlain(void (*)(int))
   :project: cpp_function_lookup


Doxygen xrefsect
----------------

.. doxygenfile:: xrefsect.h
   :project: xrefsect


Doxygen simplesect
------------------

.. doxygenfile:: simplesect.h
   :project: simplesect
