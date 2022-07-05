
.. _class-example:

doxygenclass Directive
======================

This directive generates the appropriate output for a single class. It takes the
standard ``project``, ``path``, ``outline`` and ``no-link`` options and
additionally the ``members``, ``protected-members``, ``private-members``,
``undoc-members``, ``membergroups`` and ``members-only`` options.

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

``membergroups``
  If specified, only the groups in a space-delimited list following this
  directive will be displayed.

``members-only``
  This will allow to show only the members, not the class information. Child
  classes and structs are also not shown.

If you would like to always specify some combination of ``members``,
``protected-members``, ``private-members`` and ``undoc-members`` then you can
use the :ref:`breathe_default_members <breathe-default-members>` configuration
variable to set it in the ``conf.py``.

The output includes references to any base classes and derived classes of the
specified class.


Basic Example
-------------

.. cpp:namespace:: @ex_class_basic

This displays the class documentation without any members:

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell


Template Specialisation Example
-------------------------------

.. cpp:namespace:: @ex_class_template_spec

You can reference class template specialisations by include the specialisation
in the name:

.. code-block:: rst

   .. doxygenclass:: TemplateClass< T * >
      :project: template_specialisation

Produces this output:

.. doxygenclass:: TemplateClass< T * >
   :project: template_specialisation

Where as without the specialisation, the directive references the generic
declaration:

.. code-block:: rst

   .. doxygenclass:: TemplateClass
      :project: template_specialisation

Produces this output:

.. doxygenclass:: TemplateClass
   :project: template_specialisation

Note the spacing inside the ``<>``, it's important: there must be a
space after the ``<`` and before the ``>``.

Members Example
---------------

.. cpp:namespace:: @ex_class_members

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

.. cpp:namespace:: @ex_class_members_specific

This displays the class documentation with only the members listed in the
``:members:`` option:

.. code-block:: rst

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members: Tool, crack, isCracked

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members: Tool, crack, isCracked
   :no-link:

Protected Members
-----------------

.. cpp:namespace:: @ex_class_members_protected

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


Private Members
---------------

.. cpp:namespace:: @ex_class_members_private

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

.. cpp:namespace:: @ex_class_members_undocumented

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


.. _class-example-membergroups:

Membergroups
------------

.. cpp:namespace:: @ex_class_membergroups

This will show only members in the specified member group(s).

.. code-block:: rst

   .. doxygenclass:: GroupedMembers
      :project: membergroups
      :members:
      :membergroups: myGroup

It produces this output:

.. doxygenclass:: GroupedMembers
   :project: membergroups
   :members:
   :membergroups: myGroup
   :no-link:

Without ``:membergroups: myGroup`` it would produce:

.. cpp:namespace:: @ex_class_membergroups_all

.. doxygenclass:: GroupedMembers
   :project: membergroups
   :members:


.. _class-example-membersonly:

Members-only
------------

.. cpp:namespace:: @ex_class_members_only

This will only show the members of a class, and not the class name, child
classes or structs, or any information about the class.

.. code-block:: rst

   .. doxygenclass:: ClassTest
      :project: class
      :members:
      :members-only:

It produces this output:

.. doxygenclass:: ClassTest
   :project: classtest
   :members:
   :members-only:
   :no-link:

Without ``:members-only:`` it would produce:

.. cpp:namespace:: @ex_class_members_all

.. doxygenclass:: ClassTest
   :project: classtest
   :members:
   :no-link:

.. note::

   The members will be shown at the indentation normally reserver for class
   definitions. To prevent this, you may want to indent the block by indenting
   the ``.. doxygenclass`` directive.

.. note::

   In the ``readthedocs`` theme, the members will show up in the color scheme of the
   class definitions. If you would like them rendered as the other members,
   indent like above, create a ``_static/css/custom.css`` file containing

   .. code-block:: css

      /* render as functions not classes when indented (for :members-only:) */
      html.writer-html4 .rst-content blockquote dl:not(.field-list)>dt,
      html.writer-html5 .rst-content blockquote dl[class]:not(.option-list):not(.field-list):not(.footnote):not(.glossary):not(.simple)>dt {
        margin-bottom: 6px;
        border: none;
        border-left: 3px solid #ccc;
        background: #f0f0f0;
        color: #555;
      }

   and add the following to your ``conf.py``

   .. code-block:: python

      html_static_path = ['_static']

      html_css_files = ['css/custom.css']

Outline Example
---------------

.. cpp:namespace:: @ex_class_outline

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

Qt Signals & Slots Example
--------------------------

.. cpp:namespace:: @ex_class_qt

Doxygen is aware of Qt Signals and Slots and so Breathe can pick them up and
display them in the output. They are displayed in appropriate ``Signals``,
``Public Slots``, ``Protected Slots`` and ``Private Slots`` sections.

.. code-block:: rst

   .. doxygenclass:: QtSignalSlotExample
      :project: qtsignalsandslots
      :members:

Produces the following output:

.. doxygenclass:: QtSignalSlotExample
   :project: qtsignalsandslots
   :members:

Failing Example
---------------

.. cpp:namespace:: @ex_class_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenclass:: made_up_class
      :project: class
      :members:

It produces the following warning message:

.. warning::
   doxygenclass: Cannot find class “made_up_class” in doxygen xml
   output for project “class” from directory: ../../examples/doxygen/class/xml/
