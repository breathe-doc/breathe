
Groups
======

Breathe has basic support for the grouping functionality that Doxygen provides.

Using the example from the Doxygen docs:

.. literalinclude:: code/groups.h
   :language: cpp

If we reference this with a directive, for example::

   .. doxygenclass:: Test
      :project: userdefined
      :members:
      :protected-members:

It renders as:

.. doxygenclass:: Test
   :project: userdefined
   :members:
   :protected-members:


.. note::

   Any groups which are not named in the original source code will appear as
   **Unnamed Group** in the final output. This is different to Doxygen which
   will number the groups and so name them as Group1, Group2, Group3, etc.


