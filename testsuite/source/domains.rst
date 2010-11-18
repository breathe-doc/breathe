
Domain Tests
============

.. doxygenfunction:: testnamespace::NamespacedClassTest::function
   :path: ../examples/specific/class/xml

.. doxygenfunction:: frob_foos
   :path: ../examples/specific/alias/xml

Domain Reference
----------------

Through Breathe
~~~~~~~~~~~~~~~

Sphinx domains linking to Breathe output.

This is a reference to a c func: :c:func:`frob_foos()`.

This is :c:func:`another reference <frob_foos()>` to a c func.

This is a reference to a c++ func: :cpp:func:`testnamespace::NamespacedClassTest::function()`.

This is :cpp:func:`another reference <testnamespace::NamespacedClassTest::function()>` to a cpp func.


Through Sphinx
~~~~~~~~~~~~~~

Pure Sphinx functionality.

.. c:function:: void* c_function(int)

This is :c:func:`c_function()` to a c func.

This is :c:func:`another reference <c_function()>` to a c func.

.. cpp:function:: void* mynamespace::MyClass::cppFunction(int param)

This is a reference to a c++ func: :cpp:func:`mynamespace::MyClass::cppFunction()`.

This is :cpp:func:`another reference <mynamespace::MyClass::cppFunction()>` to a cpp func.

