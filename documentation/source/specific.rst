
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

.. doxygenfunction:: testnamespace::NamespacedClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: testnamespace::ClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: testnamespace::ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: ClassTest::function
   :path: ../../examples/specific/class/xml

.. doxygenfunction:: ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml

Alias Example
-------------

.. cpp:namespace:: @ex_specific_alias

.. doxygenfunction:: frob_foos
   :path: ../../examples/specific/alias/xml

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

.. this should be switch to the C domain,
   as C++ does not support these array declarators

.. doxygenfunction:: foo
   :project: array

.. doxygenfunction:: bar
   :project: array

C Enum
------

.. doxygenenum:: GSM_BackupFormat
   :project: c_enum
   
C Typedef
---------

.. doxygenfile:: c_typedef.h
   :project: c_typedef

C Typedef
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
