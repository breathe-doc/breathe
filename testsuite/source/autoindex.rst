
.. _autodoxygenindex-example:

autodoxygenindex Directive Example
==================================

Working Example
---------------

This should work::

   .. autodoxygen:: class.h
      :source: class

With the following config value::

   breathe_projects_source = {
        "class" : "../examples/doxygen"
        }

It produces this output:

.. autodoxygenindex:: class.h
   :source: class
   :no-link:

