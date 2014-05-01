
.. _autodoxygenindex-example:

autodoxygenindex Directive Example
==================================

Working Example
---------------

This should work::

   .. autodoxygenindex::
      :project: auto

With the following config value::

   breathe_projects_source = {
        "auto" : ( "../examples/specific", ["auto_function.h", "auto_class.h"] )
        }

It produces this output:

.. autodoxygenindex::
   :project: auto
   :no-link:

