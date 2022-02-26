
..  This is more or less the class documentation with s/class/struct/g

.. _struct-example:

doxygenstruct Directive
=======================

This directive generates the appropriate output for a single struct. It takes the
standard ``project``, ``path``, ``outline`` and ``no-link`` options and
additionally the ``members``, ``protected-members``, ``private-members``,
``undoc-members``, ``membergroups`` and ``members-only`` options.

``members``
   Designed to behavior in a similar manner to the ``members`` option for the
   ``autostruct`` directive that comes with the Sphinx ``autodoc`` extension.

   If you do not specify this option you will not get any information about the
   struct members, just the general struct documentation. If you provide it
   without arguments, then Breathe adds all the public members and their
   documentation.  If you specify it with **comma separated** arguments, then
   Breathe will treat the arguments as names of members and provide
   documentation for only those members that have been named.

``protected-members``
   If specified, the protected members of the struct will be displayed.

``private-members``
   If specified, the private members of the struct will be displayed.

``undoc-members``
   If specified, the undocumented members of the struct will be displayed.

``membergroups``
  If specified, only the groups in a space-delimited list following this
  directive will be displayed.

``members-only``
  This will allow to show only the members, not the struct information. Child
  classes and structs are also not shown.

If you would like to always specify some combination of ``members``,
``protected-members``, ``private-members`` and ``undoc-members`` then you can
use the :ref:`breathe_default_members <breathe-default-members>` configuration
variable to set it in the ``conf.py``.



Basic Example
-------------

.. cpp:namespace:: @ex_struct_basic

This displays the struct documentation without any members:

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct


Members Example
---------------

.. cpp:namespace:: @ex_struct_members

This directive call will display the struct documentation with all the public
members:

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :members:

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :members:
   :no-link:

Specific Members Example
------------------------

.. cpp:namespace:: @ex_struct_members_specific

This displays the struct documentation with only the members listed in the
``:members:`` option:

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :members: publicFunction, protectedFunction

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :members: publicFunction, protectedFunction
   :no-link:

Protected Members
-----------------

.. cpp:namespace:: @ex_struct_members_protected

This displays only the protected members of the struct. Normally this is combined
with the ``:members:`` option to show the public members as well.

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :protected-members:

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :protected-members:
   :no-link:

Private Members
---------------

.. cpp:namespace:: @ex_struct_members_private

This displays only the private members of the struct. Normally this is combined
with the ``:members:`` option to show the public members as well.

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :private-members:

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :private-members:
   :no-link:

Undocumented Members
--------------------

.. cpp:namespace:: @ex_struct_members_undocumented

This displays the undocumented members of the struct which are suppressed by
default. Undocumented public members are only shown if the ``:members:`` option
is also used. The same goes for the undocumented private members and the
``private-members`` option.

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :members:
      :private-members:
      :undoc-members:

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :members:
   :private-members:
   :undoc-members:
   :no-link:

.. note::

   Undocumented internal classes are still not shown in the output due to an
   implementation issue. Please post an issue on github if you would like this
   resolved.


Membergroups
------------

.. cpp:namespace:: @ex_struct_membersgroups

Lists one or more names member groups.

See the :ref:`doxygenclass documentation <class-example-membergroups>`.


Members-only
------------

See the :ref:`doxygenclass documentation <class-example-membersonly>`.


Outline Example
---------------

.. cpp:namespace:: @ex_struct_outline

This displays only the names of the struct members and not their
documentation. The ``:members:`` and ``:private-members:`` options determine
which members are displayed.

.. code-block:: rst

   .. doxygenstruct:: StructTest
      :project: struct
      :members:
      :outline:

It produces this output:

.. doxygenstruct:: StructTest
   :project: struct
   :members:
   :outline:
   :no-link:

Failing Example
---------------

.. cpp:namespace:: @ex_struct_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenstruct:: made_up_struct
      :project: struct
      :members:

It produces the following warning message:

.. warning::
   doxygenstruct: Cannot find struct "made_up_struct" in doxygen xml
   output for project “struct” from directory: ../../examples/doxygen/struct/xml/
