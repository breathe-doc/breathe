
Namespaces
==========

Breathe has basic support for namespaces.

Using the example from the Doxygen docs:

.. literalinclude:: code/namespaces.h
   :language: cpp

If we reference this with a directive, for example::

   .. doxygennamespace:: test_namespace
      :project: userdefined
      :members:

It renders as:

.. doxygennamespace:: test_namespace
   :project: userdefined
   :members:


.. note::
