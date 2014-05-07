
.. _group-example:

doxygengroup Directive Example
==============================

The doxygengroup directive renders the contents of the doxygen group as well as
the group name and any documentation for the group itself.

Example
-------

This should work::

   .. doxygengroup:: mygroup
      :project: group

It produces this output:

----

.. doxygengroup:: mygroup
   :project: group
   :no-link:

---- 

The directive also accepts a ``:content-only:`` option which changes the output
to only include the content of the group and not the group name or description.
So this::

   .. doxygengroup:: mygroup
      :project: group
      :content-only:

Produces this output:

----

.. doxygengroup:: mygroup
   :project: group
   :content-only:
   :no-link:



Failing Example
---------------

This intentionally fails::

   .. doxygengroup:: madeupgroup
      :project: group

It produces the following warning message:

.. warning:: Cannot find file "madeupgroup" in doxygen xml output for project
             "group" from directory: ../examples/specific/group/xml/
