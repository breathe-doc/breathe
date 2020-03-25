
.. _file-example:

doxygenfile Directive Example
=============================

Example
-------

.. cpp:namespace:: @ex_file_example

This should work::

   .. doxygenfile:: nutshell.h
      :project: nutshell

It produces this output:

----

.. doxygenfile:: nutshell.h
   :project: nutshell

Example with Nested Namespaces
------------------------------

.. cpp:namespace:: @ex_file_namespace

This should work::

   .. doxygenfile:: namespacefile.h
      :project: namespace

It produces this output:

----

.. doxygenfile:: namespacefile.h
   :project: namespace


Example for Multiple Files
--------------------------

.. cpp:namespace:: @ex_file_multiple_files

When there are multiple files with the same name in the project, you need to be
more specific with the filename you provide. For example, in a project with the
following two files::

   /some/long/project/path/parser/Util.h
   /some/long/project/path/finder/Util.h

You should specify::

   .. doxygenfile:: parser/Util.h

   .. doxygenfile:: finder/Util.h

To uniquely identify them.

Failing Example
---------------

.. cpp:namespace:: @ex_file_failing

This intentionally fails::

   .. doxygenfile:: made_up_file.h
      :project: nutshell

It produces the following warning message:

.. warning:: Cannot find file "made_up_file.h" in doxygen xml output for project "nutshell" from directory: ../../examples/specific/nutshell/xml/
