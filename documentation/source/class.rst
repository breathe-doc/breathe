
.. _class-example:

doxygenclass Directive
======================

This directive generates the appropriate output for a single class. It takes the
standard ``project``, ``path``, ``outline`` and ``no-link`` options and
additionally the ``members``, ``protected-members``, ``private-members`` and
``undoc-members`` options.

``members``
   Designed to behavior in a similar manner to the ``members`` option for the
   ``autoclass`` directive that comes with the Sphinx ``autodoc`` extension.

   If you do not specify this option you will not get any information about the
   class members, just the general class documentation. If you provide it
   without arguments, then Breathe adds all the public members and their
   documentation.  If you specify it with **comma separated** arguments, then
   Breathe will treat the arguments as names of members and provide
   documentation for only those members that have been named.

``protected-members``
   If specified, the protected members of the class will be displayed.

``private-members``
   If specified, the private members of the class will be displayed.

``undoc-members``
   If specified, the undocumented members of the class will be displayed.

If you would like to always specify some combination of ``members``,
``protected-members``, ``private-members`` and ``undoc-members`` then you can
use the :ref:`breathe_default_members <breathe-default-members>` configuration
variable to set it in the ``conf.py``.

The output includes references to any base classes and derived classes of the
specified class.

.. contents::


Basic Example
-------------

This displays the class documentation without any members:

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :no-link:


Template Specialisation Example
-------------------------------

You can reference class template specialisations by include the specialisation
in the name:

.. code-block:: rst

   .. doxygenclass:: TemplateClass< T * >
      :project: template_specialisation

Produces this output:

.. doxygenclass:: TemplateClass< T * >
   :project: template_specialisation
   :no-link:

Where as without the specialisation, the directive references the generic
declaration:

.. code-block:: rst

   .. doxygenclass:: TemplateClass
      :project: template_specialisation

Produces this output:

.. doxygenclass:: TemplateClass
   :project: template_specialisation
   :no-link:


Members Example
---------------

This directive call will display the class documentation with all the public
members:

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members:
   :no-link:


Specific Members Example
------------------------

This displays the class documentation with only the members listed in the
``:members:`` option:

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members: crack, isCracked

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members: crack, isCracked
   :no-link:


Protected Members
-----------------

This displays only the protected members of the class. Normally this is combined
with the ``:members:`` option to show the public members as well.

.. code-block:: rst

   .. doxygenclass:: GroupedClassTest
      :project: group
      :protected-members:

It produces this output:

.. doxygenclass:: GroupedClassTest
   :project: group
   :protected-members:
   :no-link:


Private Members
---------------

This displays only the private members of the class. Normally this is combined
with the ``:members:`` option to show the public members as well.

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell
      :private-members:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :private-members:
   :no-link:

Undocumented Members
--------------------

This displays the undocumented members of the class which are suppressed by
default. Undocumented public members are only shown if the ``:members:`` option
is also used. The same goes for the undocumented private members and the
``private-members`` option.

.. code-block:: rst

   .. doxygenclass:: ClassTest
      :project: class
      :members:
      :private-members:
      :undoc-members:

It produces this output:

.. doxygenclass:: ClassTest
   :project: classtest
   :members:
   :private-members:
   :undoc-members:
   :no-link:

.. note::

   Undocumented classes are still not shown in the output due to an implementation
   issue. Please post an issue on github if you would like this resolved.

Outline Example
---------------

This displays only the names of the class members and not their
documentation. The ``:members:`` and ``:private-members:`` options determine
which members are displayed.

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members:
      :outline:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members:
   :outline:
   :no-link:


Qt Slots Example
----------------

Doxygen is aware of Qt Slots and so Breathe can pick them up and display them in
the output. They are displayed in appropriate ``Public Slots``, ``Protected
Slots`` and ``Private Slots`` sections.

.. code-block:: rst

   .. doxygenclass:: QtSlotExample
      :project: qtslots
      :members:

Produces the following output:

.. doxygenclass:: QtSlotExample
   :project: qtslots
   :members:
   :no-link:

Failing Example
---------------

This intentionally fails:

.. code-block:: rst

   .. doxygenclass:: made_up_class
      :project: class
      :members:

It produces the following warning message:

.. warning:: doxygenclass: Cannot find class “made_up_class” in doxygen xml
   output for project “class” from directory: ../../examples/doxygen/class/xml/


