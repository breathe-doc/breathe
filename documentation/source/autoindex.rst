
.. _autodoxygenindex-example:

autodoxygenindex Directive Example
==================================

Working Example
---------------

This should work:

.. code-block:: rst

   .. autodoxygenindex::
      :project: auto

With the following config value:

.. code-block:: python

   breathe_projects_source = {
       "auto" : ( "../examples/specific", ["auto_function.h", "auto_class.h"] )
   }

It produces this output:

.. cpp:namespace:: @ex_autoindex

.. autodoxygenindex::
   :project: auto
