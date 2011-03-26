
.. _file-example:

doxygenfile Directive Example
=============================

Example
-------

This should work::

   .. doxygenfile:: nutshell.h
      :project: nutshell

It produces this output:

.. doxygenfile:: nutshell.h
   :project: nutshell


Failing Example
---------------

This intentionally fails::

   .. doxygenfile:: made_up_file.h
      :project: nutshell

It produces the following warning message:

.. warning:: doxygenclass: Cannot find file "made_up_file" in doxygen xml output
