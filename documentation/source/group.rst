
.. _group-example:

doxygengroup Directive
======================

This directive generates the appropriate output for the contents of a doxygen
group. A doxygen group can be declared with specific doxygen markup in the
source comments as cover in the `doxygen documentation`_.

It takes the standard ``project``, ``path``, ``outline`` and ``no-link`` options
and additionally the ``content-only`` and ``private-members`` options.

``content-only``
   If this flag is specified, then the directive does not output the name of the
   group or the group description and instead outputs the contents of the group.
   This can be useful if the groups are only used for organizational purposes
   and not to provide additional information.

``private-members``
   If specified, the private members of any classes in the group output will be
   displayed.

.. _doxygen documentation: http://www.stack.nl/~dimitri/doxygen/manual/grouping.html


Basic Example
-------------

The plain ``doxygengroup`` directive will output the group name and description:

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


Private-Members Example
-----------------------

The ``private-members`` option changes the output to only include the private
members of any classes as well as the public members. The output for any class
in the group should be the same as if it had be produced by the
:ref:`doxygenclass directive <class-example>` with the ``members`` and
``private-members`` options specified.

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :private-members:

Produces this output:

.. doxygengroup:: mygroup
   :project: group
   :private-members:
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

