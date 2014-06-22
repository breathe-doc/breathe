
.. _group-example:

doxygengroup Directive
======================

This directive generates the appropriate output for the contents of a doxygen
group. A doxygen group can be declared with specific doxygen markup in the
source comments as cover in the `doxygen documentation`_.

It takes the standard ``project``, ``path``, ``outline`` and ``no-link`` options
and additionally the ``content-only``, ``members``, ``protected-members``,
``private-members`` and ``undoc-members`` options.

``content-only``
   If this flag is specified, then the directive does not output the name of the
   group or the group description and instead outputs the contents of the group.
   This can be useful if the groups are only used for organizational purposes
   and not to provide additional information.

``members``
   If specified, the public members of any classes in the group output will be
   displayed. Unlike the ``doxygenclass`` ``members`` option, this does not
   optionally take a list of member names to display as this will be applied
   across multiple classes within the group.

``protected-members``
   If specified, the protected members of any classes in the group output will
   be displayed.

``private-members``
   If specified, the private members of any classes in the group output will be
   displayed.

``undoc-members``
   If specified, the undocumented members of any classes in the group output
   will be displayed provided the appropriate ``members`` or ``private-members``
   options are specified as well.

If you would like to always specify some combination of ``members``,
``protected-members``, ``private-members`` and ``undoc-members`` then you can
use the :ref:`breathe_default_members <breathe-default-members>` configuration
variable to set it in the ``conf.py``.

.. _doxygen documentation: http://www.stack.nl/~dimitri/doxygen/manual/grouping.html

.. contents::


Basic Example
-------------

The plain ``doxygengroup`` directive will output the group name and description
and any top level publicly visible members of the group.

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group

It produces this output:

.. doxygengroup:: mygroup
   :project: group
   :no-link:

Content-Only Example
--------------------

The ``content-only`` option changes the output to only include the content of
the group and not the group name or description. So this:

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :content-only:

Produces this output:

.. doxygengroup:: mygroup
   :project: group
   :content-only:
   :no-link:

.. note::

   As you can see from the output, section headings like 'Functions' are missing
   from the :content-only: display. This is due to an implementation detail. If
   post an issue on github if you'd like it addressed.


Members Example
---------------

The ``members`` option changes the output to include the public members of any
classes. The output for any class in the group should be the same as if it had
be produced by the :ref:`doxygenclass directive <class-example>` with the
``members`` option specified.

::

   .. doxygengroup:: mygroup
      :project: group
      :members:

It produces this output:

.. doxygengroup:: mygroup
   :project: group
   :members:
   :no-link:


Protected Members Example
-------------------------

The ``protected-members`` option changes the output to include the protected
members of any classes. The output for any class in the group should be the same
as if it had be produced by the :ref:`doxygenclass directive <class-example>`
with the ``protected-members`` option specified.

::

   .. doxygengroup:: mygroup
      :project: group
      :protected-members:

It produces this output:

.. doxygengroup:: mygroup
   :project: group
   :protected-members:
   :no-link:


Private-Members Example
-----------------------

The ``private-members`` option changes the output to include the private members
of any classes. The output for any class in the group should be the same as if
it had be produced by the :ref:`doxygenclass directive <class-example>` with the
``private-members`` option specified.

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :private-members:

Produces this output:

.. doxygengroup:: mygroup
   :project: group
   :private-members:
   :no-link:


Undocumented Members Example
----------------------------

The ``undoc-members`` option changes the output to include any undocumentated
members from the sections (public, protected, private) that are being displayed
for the classes in the group output.

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :private-members:
      :undoc-members:

Produces this output:

.. doxygengroup:: mygroup
   :project: group
   :private-members:
   :undoc-members:
   :no-link:

.. note::

   Undocumented classes are still not shown in the output due to an implementation
   issue. Please post an issue on github if you would like this resolved.


Outline Example
---------------

This displays only the names of the members of the group and not their
documentation. The other options determine which members are displayed.

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :members:
      :outline:

It produces this output:

.. doxygengroup:: mygroup
   :project: group
   :members:
   :outline:
   :no-link:


Failing Example
---------------

This intentionally fails:

.. code-block:: rst

   .. doxygengroup:: madeupgroup
      :project: group

It produces the following warning message:

.. warning:: Cannot find file "madeupgroup" in doxygen xml output for project
             "group" from directory: ../../examples/specific/group/xml/

