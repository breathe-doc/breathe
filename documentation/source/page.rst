
.. _page-example:

doxygenpage Directive
=====================

This directive generates the appropriate output for the contents of a doxygen
page. A doxygen page is created for each "key" of every \\xrefitem command used
for markup in the source comments. For more information check the
`doxygen documentation`_.

It takes the standard ``project`` and ``path`` options.

.. code-block:: rst

   .. doxygenpage:: <page name>
      :project: ...
      :path: ...

.. _doxygen documentation: https://www.doxygen.nl/manual/commands.html#cmdxrefitem



Basic Example
-------------

.. cpp:namespace:: @ex_page_basic

The plain ``doxygenpage`` directive will output the page name and description
and any variable entries which were defined to be part of this page (with an
\xrefitem usage).

.. code-block:: rst

   .. doxygenpage:: xrefsample
      :project: xrefsect

It produces this output:

.. doxygenpage:: xrefsample
   :project: xrefsect


Failing Example
---------------

.. cpp:namespace:: @ex_page_failing

This intentionally fails:

.. code-block:: rst

   .. doxygengroup:: madeuppage
      :project: xrefsect

It produces the following warning message:

.. warning::
   Cannot find file "madeuppage" in doxygen xml output for project
   "xrefsect" from directory: ../../examples/specific/xrefsect/xml/
