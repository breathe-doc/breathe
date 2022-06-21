Tables
======

Breathe has support for tables in the doxygen documentation. They are output as
follows.

.. cpp:namespace:: @ex_tables_simple

A simple Markdown syntax table:

.. code-block:: rst

   .. doxygenclass:: Table_1
      :project: tables

It renders as:

----

.. doxygenclass:: Table_1
   :project: tables

----

.. cpp:namespace:: @ex_tables_aligned

A Markdown syntax table with alignment:

.. code-block:: rst

   .. doxygenclass:: Table_2
      :project: tables

It renders as:

----

.. doxygenclass:: Table_2
   :project: tables

----

.. cpp:namespace:: @ex_tables_rowspan

A Markdown syntax table with rowspan (and alignment):

.. code-block:: rst

   .. doxygenclass:: Table_3
      :project: tables

It renders as:

----

.. only:: html

    .. doxygenclass:: Table_3
       :project: tables

----

.. cpp:namespace:: @ex_tables_colspan

A Markdown syntax table with colspan (and alignment):

.. code-block:: rst

   .. doxygenclass:: Table_4
      :project: tables

It renders as:

----

.. only:: html

    .. doxygenclass:: Table_4
       :project: tables

----

.. cpp:namespace:: @ex_tables_doxygen

A Doxygen syntax table:

.. code-block:: rst

   .. doxygenclass:: Table_5
      :project: tables

It renders as:

----

.. only:: html

    .. doxygenclass:: Table_5
       :project: tables
