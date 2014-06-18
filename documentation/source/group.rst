
.. _group-example:

doxygengroup Directive
======================

This directive generates the appropriate output for the contents of a doxygen
group. A doxygen group can be declared with specific doxygen markup in the
source comments as cover in the `doxygen documentation`_.

It takes the standard ``project``, ``path``, ``outline`` and ``no-link`` options
and additionally the ``content-only`` and ``sections`` options.

``content-only``
   If this flag is specified, then the directive does not output the name of the
   group or the group description and instead outputs the contents of the group.
   This can be useful if the groups are only used for organizational purposes
   and not to provide additional information.

``sections``
   This option can be used to determine the Doxygen XML ``sections`` which are
   allowed in the output for the group. The terminology here is a little coarse
   as it based on the names used in the Doxygen XML. The clearest application of
   this option is to determine whether to output private members from classes
   within the group.  For instance, if you want to display the all protected and
   public members, functions, etc, then specify ``:sections: public*,
   protected*``.

   By default, Breathe specifies ``public*, func*``, however this can be
   overridden in the ``conf.py`` with the :ref:`breathe_default_sections
   <breathe-default-sections>` config variable.

   Note that if your Doxygen project uses properties, these are excluded by
   default. Specify ``:sections: public*, property`` to include both public
   members and properties. (The section names correspond to the values of the
   ``kind`` attribute of the Doxygen XML ``sectiondef`` elements.)

.. _doxygen documentation: http://www.stack.nl/~dimitri/doxygen/manual/grouping.html


Basic Example
-------------

This should work:

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group

It produces this output:

----

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

----

.. doxygengroup:: mygroup
   :project: group
   :content-only:
   :no-link:

Sections Example
----------------

The ``sections`` option changes the output of public, protected and private
content as well as properties. For example:

.. code-block:: rst

   .. doxygengroup:: mygroup
      :project: group
      :content-only:
      :sections: public*, private*

Produces this output:

----

.. doxygengroup:: mygroup
   :project: group
   :content-only:
   :members:
   :no-link:

----

.. doxygengroup:: mygroup
   :project: group
   :content-only:
   :members:
   :private-members:
   :no-link:

----

In which the private functions are listed as well as the public ones due to the
specification of ``private*`` for the ``sections`` option, and the
``void groupedFunction()`` is not listed as the ``sections`` option has
overridden the global :ref:`breathe_default_sections <breathe-default-sections>`
and removed the ``func*`` element.

Failing Example
---------------

This intentionally fails:

.. code-block:: rst

   .. doxygengroup:: madeupgroup
      :project: group

It produces the following warning message:

.. warning:: Cannot find file "madeupgroup" in doxygen xml output for project
             "group" from directory: ../../examples/specific/group/xml/

