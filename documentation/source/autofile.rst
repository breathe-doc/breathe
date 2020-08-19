
.. _autodoxygenfile-example:

autodoxygenfile Directive Example
=================================

For more details and directive documentation please see :ref:`file-example`,
which is very similar to this directive.

Working Example
---------------

This should work::

   .. autodoxygenfile:: auto_class.h
      :project: auto

With the following config value::

   breathe_projects_source = {
        "auto" : ( "../examples/specific", ["auto_class.h"] )
        }

It produces this output:

.. autodoxygenfile:: auto_class.h
   :project: auto
