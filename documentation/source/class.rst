
.. _class-example:

doxygenclass Directive Example
==============================

Example without Members
-----------------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :no-link:


Example with Members
--------------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members:
   :no-link:


Working Example with Specific Members
-------------------------------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell
      :members: crack, isCracked

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :members: crack, isCracked
   :no-link:


Example as Outline
------------------

This should work::

   .. doxygenclass:: Nutshell
      :project: nutshell
      :outline:
      :members:

It produces this output:

.. doxygenclass:: Nutshell
   :project: nutshell
   :outline:
   :members:
   :no-link:


Failing Example
---------------

This intentionally fails::

   .. doxygenclass:: made_up_class
      :project: class
      :members:

It produces the following warning message:

.. warning:: doxygenclass: Cannot find class "made_up_class" in doxygen xml output


