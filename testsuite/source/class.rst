
doxygenclass Directive Example
==============================

Working Example
---------------

This should work::

   .. doxygenclass:: Test
      :project: class

It produces this output:

.. doxygenclass:: Test
   :project: class

Failing Example
---------------

This intentionally fails::

   .. doxygenclass:: made_up_class
      :project: class

It produces the following warning message:

.. doxygenclass:: made_up_class
   :project: class

