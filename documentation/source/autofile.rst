
.. _autodoxygenfile-example:

autodoxygenfile Directive Example
=================================

Working Example
---------------

This should work::

   .. autodoxygenfile:: auto_class.h
      :source: auto

With the following config value::

   breathe_projects_source = {
        "auto" : ( "../examples/specific", ["auto_class.h"] )
        }

It produces this output:

.. autodoxygenfile:: auto_class.h
   :project: auto
   :no-link:
