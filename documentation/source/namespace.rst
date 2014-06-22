
.. _namespace-example:

doxygennamespace Directive
==========================

This directive generates the appropriate output for the contents of a
namespace.

It takes the standard ``project``, ``path``, ``outline`` and ``no-link`` options
and additionally the ``content-only``, ``members``, ``protected-members``,
``private-members`` and ``undoc-members`` options.

``content-only``
   If this flag is specified, then the directive does not output the name of the
   namespace or the namespace description and instead outputs the contents of
   the namespace. This can be useful for structuring your documentation but
   leaving out the namespace declaration itself which is often undocumented.

``members``
   If specified, the public members of any classes in the namespace output will be
   displayed. Unlike the ``doxygenclass`` ``members`` option, this does not
   optionally take a list of member names to display as this will be applied
   across multiple classes within the namespace.

``protected-members``
   If specified, the protected members of any classes in the namespace output will
   be displayed.

``private-members``
   If specified, the private members of any classes in the namespace output will be
   displayed.

``undoc-members``
   If specified, the undocumented members of any classes in the namespace output
   will be displayed provided the appropriate ``members`` or ``private-members``
   options are specified as well.

If you would like to always specify some combination of ``members``,
``protected-members``, ``private-members`` and ``undoc-members`` then you can
use the :ref:`breathe_default_members <breathe-default-members>` configuration
variable to set it in the ``conf.py``.

.. contents::


Basic Example
-------------

The plain ``doxygennamespace`` directive will output the namespace name and
description and any top level publicly visible members of the namespace.

.. code-block:: rst

   .. doxygennamespace:: foo
      :project: namespace

It produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :no-link:

Content-Only Example
--------------------

The ``content-only`` option changes the output to only include the content of
the namespace and not the namespace name or description. So this:

.. code-block:: rst

   .. doxygennamespace:: foo
      :project: namespace
      :content-only:

Produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :content-only:
   :no-link:

.. note::

   As you can see from the output, section headings like 'Functions' are missing
   from the :content-only: display. This is due to an implementation detail. If
   post an issue on github if you'd like it addressed.


Members Example
---------------

The ``members`` option changes the output to include the public members of any
classes. The output for any class in the namespace should be the same as if it had
be produced by the :ref:`doxygenclass directive <class-example>` with the
``members`` option specified.

::

   .. doxygennamespace:: foo
      :project: namespace
      :members:

It produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :members:
   :no-link:


Protected Members Example
-------------------------

The ``protected-members`` option changes the output to include the protected
members of any classes. The output for any class in the namespace should be the same
as if it had be produced by the :ref:`doxygenclass directive <class-example>`
with the ``protected-members`` option specified.

::

   .. doxygennamespace:: foo
      :project: namespace
      :protected-members:

It produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :protected-members:
   :no-link:


Private-Members Example
-----------------------

The ``private-members`` option changes the output to include the private members
of any classes. The output for any class in the namespace should be the same as if
it had be produced by the :ref:`doxygenclass directive <class-example>` with the
``private-members`` option specified.

.. code-block:: rst

   .. doxygennamespace:: foo
      :project: namespace
      :private-members:

Produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :private-members:
   :no-link:


Undocumented Members Example
----------------------------

The ``undoc-members`` option changes the output to include any undocumentated
members from the sections (public, protected, private) that are being displayed
for the classes in the namespace output.

.. code-block:: rst

   .. doxygennamespace:: foo
      :project: namespace
      :private-members:
      :undoc-members:

Produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :private-members:
   :undoc-members:
   :no-link:

.. note::

   Undocumented classes are still not shown in the output due to an
   implementation issue. Please post an issue on github if you would like this
   resolved.


Outline Example
---------------

This displays only the names of the members of the namespace and not their
documentation. The other options determine which members are displayed.

.. code-block:: rst

   .. doxygennamespace:: foo
      :project: namespace
      :members:
      :outline:

It produces this output:

.. doxygennamespace:: foo
   :project: namespace
   :members:
   :outline:
   :no-link:


Nested Example
--------------

The referenced namespace can be nested in another namespace.

.. code-block:: rst

   .. doxygennamespace:: foo::ns
      :project: namespace

Produces this output:

.. doxygennamespace:: foo::ns
   :project: namespace
   :no-link:


Failing Example
---------------

This intentionally fails:

.. code-block:: rst

   .. doxygennamespace:: madeupnamespace
      :project: namespace

It produces the following warning message:

.. warning:: doxygennamespace: Cannot find namespace “madeupnamespace” in
             doxygen xml output for project “namespace” from directory:
             ../../examples/specific/namespacefile/xml/
