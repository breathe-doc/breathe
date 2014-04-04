
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
        "auto" : "../examples/auto"
        }

It produces this output:

.. autodoxygenfile:: auto_class.h
   :source: auto
   :no-link:

