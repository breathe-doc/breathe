
.. _class-example:

doxygenclass Directive Example
==============================

Working Example
---------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members:

Working Example with Specific Members
-------------------------------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members: crack, isCracked
      :no-link:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members: crack, isCracked
   :no-link:

Failing Example
---------------

This intentionally fails::

   .. doxygenclass:: made_up_class
      :project: class
      :members:

It produces the following warning message:

.. warning:: doxygenclass: Cannot find class "made_up_class" in doxygen xml output

