
Specific Examples Test Suite
============================


Typedef Examples
----------------

.. doxygenindex::
   :path: ../../examples/specific/typedef/xml
   :no-link:


Namespaced Function Examples
----------------------------

.. doxygenfunction:: testnamespace::NamespacedClassTest::function
   :path: ../../examples/specific/class/xml
   :no-link:

.. doxygenfunction:: testnamespace::ClassTest::function
   :path: ../../examples/specific/class/xml
   :no-link:

.. doxygenfunction:: testnamespace::ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml
   :no-link:

.. doxygenfunction:: ClassTest::function
   :path: ../../examples/specific/class/xml
   :no-link:

.. doxygenfunction:: ClassTest::anotherFunction
   :path: ../../examples/specific/class/xml
   :no-link:

Alias Example
-------------

.. doxygenfunction:: frob_foos
   :path: ../../examples/specific/alias/xml
   :no-link:

Fixed Width Font
----------------

.. doxygenclass:: Out
   :path: ../../examples/specific/fixedwidthfont/xml
   :members:
   :no-link:

Function Overloads
------------------

.. doxygenfunction:: f(int, int)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: f(double, double)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: test::g(int,int)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: test::g(double, double)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: h(std::string, MyType)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: h(std::string, MyOtherType)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: h(std::string, const int)
   :project: functionOverload
   :no-link:

.. doxygenfunction:: h(std::string, const T, const U)
   :project: functionOverload
   :no-link:

Program Listing
---------------

.. doxygenclass:: Vector
   :project: programlisting
   :no-link:

.. doxygenfunction:: center
   :project: programlisting
   :no-link:

Image
-----

.. doxygenclass:: ImageClass
   :project: image
   :no-link:


Array Parameter
---------------

.. doxygenfunction:: foo
   :project: array
   :no-link:

.. doxygenfunction:: bar
   :project: array
   :no-link:


C Enum
------

.. doxygenenum:: GSM_BackupFormat
   :project: c_enum
   :no-link:

   
C Typedef
---------

.. doxygenfile:: c_typedef.h
   :project: c_typedef
   :no-link:

C Typedef
---------

.. doxygenfile:: define.h
   :project: define
   :no-link:
   
Multifile
---------

.. doxygenfunction:: TestTemplateFunction
   :project: multifile
   :no-link:

Interface Class
---------------

.. doxygeninterface:: InterfaceClass
   :project: interface
   :no-link:
