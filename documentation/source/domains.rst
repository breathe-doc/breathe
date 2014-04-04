
Domains
=======

Breathe has some limited support for Sphinx domains. It tries to output targets
that the Sphinx domain references expect. This should allow you to use Sphinx
domain roles like ``:c:func:`foo``` to link to output from Breathe.

The following targets are supported:

* C & C++ functions
* C++ classes


Class Example
-------------

Given the following Breathe directives::

   .. doxygenclass:: testnamespace::NamespacedClassTest
      :path: ../examples/specific/class/xml

Which create formatted output like:

   .. doxygenclass:: testnamespace::NamespacedClassTest
      :path: ../examples/specific/class/xml

We can refer to **NamespacedClassTest** using:: 

   :cpp:class:`testnamespace::NamespacedClassTest`
   
which renders as :cpp:class:`testnamespace::NamespacedClassTest`, or using::

   :cpp:class:`another reference <testnamespace::NamespacedClassTest>`
   
which renders as: :cpp:class:`another reference <testnamespace::NamespacedClassTest>`.

Function Examples
-----------------

Given the following Breathe directives::

   .. doxygenfunction:: testnamespace::NamespacedClassTest::function
      :path: ../examples/specific/class/xml

   .. doxygenfunction:: frob_foos
      :path: ../examples/specific/alias/xml

Which create formatted output like:

   .. doxygenfunction:: testnamespace::NamespacedClassTest::function
      :path: ../examples/specific/class/xml

   .. doxygenfunction:: frob_foos
      :path: ../examples/specific/alias/xml

We can refer to **function** using:: 

   :cpp:func:`testnamespace::NamespacedClassTest::function()`
   
which renders as :cpp:func:`testnamespace::NamespacedClassTest::function()`, or using::

   :cpp:func:`another reference <testnamespace::NamespacedClassTest::function()>`
   
which renders as: :cpp:func:`another reference <testnamespace::NamespacedClassTest::function()>`.
Note the use of the **cpp** domain.

And we can refer to **frob_foos** using:: 
   
   :c:func:`frob_foos()`

which renders as: :c:func:`frob_foos()`, or using::

   :c:func:`another reference <frob_foos()>` 
   
which renders as: :c:func:`another reference <frob_foos()>`. Note the use of the **c** domain.


