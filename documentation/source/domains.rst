
Domains
=======

Breathe has some limited support for Sphinx domains. It tries to output targets
that the Sphinx domain references expect. This should allow you to use Sphinx
domain roles like ``:c:func:`foo``` to link to output from Breathe.

Class Example
-------------

.. cpp:namespace:: @ex_domains_class

Given the following Breathe directives:

.. code-block:: rst

   .. doxygenclass:: TestNamespaceClasses::NamespacedClassTest
      :path: ../../examples/specific/class/xml

Which create formatted output like:

   .. doxygenclass:: TestNamespaceClasses::NamespacedClassTest
      :path: ../../examples/specific/class/xml

We can refer to **NamespacedClassTest** using:

.. code-block:: rst

   :cpp:class:`TestNamespaceClasses::NamespacedClassTest`

which renders as :cpp:class:`TestNamespaceClasses::NamespacedClassTest`, or using:

.. code-block:: rst

   :cpp:class:`another reference <TestNamespaceClasses::NamespacedClassTest>`

which renders as: :cpp:class:`another reference <TestNamespaceClasses::NamespacedClassTest>`.

Inner Class Example
-------------------

.. cpp:namespace:: @ex_domains_inner_class

Given the following Breathe directive::

   .. doxygenclass:: OuterClass
      :path: ../../examples/specific/class/xml
      :members:

Which create formatted output like:

   .. doxygenclass:: OuterClass
      :path: ../../examples/specific/class/xml
      :members:

We can refer to **OuterClass::InnerClass** using::

   :cpp:class:`OuterClass::InnerClass`

which renders as :cpp:class:`OuterClass::InnerClass`.

Function Examples
-----------------

.. cpp:namespace:: @ex_domains_function

Given the following Breathe directives:

.. code-block:: rst

   .. doxygenfunction:: TestNamespaceClasses::NamespacedClassTest::function
      :path: ../../examples/specific/class/xml

   .. doxygenfunction:: frob_foos
      :path: ../../examples/specific/alias/xml

Which create formatted output like:

   .. doxygenfunction:: TestNamespaceClasses::NamespacedClassTest::function
      :path: ../../examples/specific/class/xml

   .. doxygenfunction:: frob_foos
      :path: ../../examples/specific/alias/xml

We can refer to **namespaceFunc** using:

.. code-block:: rst

   :cpp:func:`TestNamespaceFunction::namespaceFunc()`

which renders as :cpp:func:`TestNamespaceFunction::namespaceFunc()`, or using:

.. code-block:: rst

   :cpp:func:`another reference <namespaceFunc()>`

which renders as: :cpp:func:`another reference <TestNamespaceFunction::namespaceFunc()>`.
Note the use of the **cpp** domain.

And we can refer to **frob_foos** using:

.. code-block:: rst

   :c:func:`frob_foos()`

which renders as: :c:func:`frob_foos()`, or using:

.. code-block:: rst

   :c:func:`another reference <frob_foos()>`

which renders as: :c:func:`another reference <frob_foos()>`. Note the use of the **c** domain.

Typedef Examples
----------------

.. cpp:namespace:: @ex_domains_typedef

Given the following Breathe directives:

.. code-block:: rst

   .. doxygentypedef:: TestTypedef
      :path: ../../examples/specific/typedef/xml

   .. doxygennamespace:: TypeDefNamespace
      :path: ../../examples/specific/typedef/xml

   .. doxygenclass:: TestClass
      :path: ../../examples/specific/typedef/xml
      :members:

which create formatted output like:

   .. doxygentypedef:: TestTypedef
      :path: ../../examples/specific/typedef/xml

   .. doxygennamespace:: TypeDefNamespace
      :path: ../../examples/specific/typedef/xml

   .. doxygenclass:: TestClass
      :path: ../../examples/specific/typedef/xml
      :members:

We can refer to **TestTypedef** using:

.. code-block:: rst

   :cpp:type:`TestTypedef`

which renders as :cpp:type:`TestTypedef`, to **TypeDefNamespace::AnotherTypedef** using:

.. code-block:: rst

   :cpp:type:`TypeDefNamespace::AnotherTypedef`

which renders as :cpp:type:`TypeDefNamespace::AnotherTypedef` and to **TestClass::MemberTypedef** using:

.. code-block:: rst

   :cpp:type:`TestClass::MemberTypedef`

which renders as :cpp:type:`TestClass::MemberTypedef`.

Enum Value Examples
-------------------

.. cpp:namespace:: @ex_domains_enum

Given the following Breathe directives:

.. code-block:: rst

   .. doxygenenumvalue:: VALUE
      :path: ../../examples/specific/enum/xml

   .. doxygenenumvalue:: TestEnumNamespace::FIRST
      :path: ../../examples/specific/enum/xml

Which create formatted output like:

   .. doxygenenumvalue:: VALUE
      :path: ../../examples/specific/enum/xml

   .. doxygenenumvalue:: TestEnumNamespace::FIRST
      :path: ../../examples/specific/enum/xml

We can refer to **VALUE** using:

.. code-block:: rst

   :cpp:enumerator:`VALUE`

which renders as :cpp:enumerator:`VALUE` and to **TestEnumNamespace::FIRST** using:

.. code-block:: rst

   :cpp:enumerator:`TestEnumNamespace::FIRST`

which renders as :cpp:enumerator:`TestEnumNamespace::FIRST`.
