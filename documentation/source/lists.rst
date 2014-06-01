Lists
======

Breathe has support for lists in the doxygen documentation. They are output as
follows.

For unordered lists with list items prefixed with **+** ::

   .. doxygenclass:: SimpleList_1
      :project: lists

It renders as:

----

.. doxygenclass:: SimpleList_1
   :project: lists

----

Unordered lists with list items prefixed with **-** render as:

----

.. doxygenclass:: SimpleList_2
   :project: lists

----

Unordered lists with list items prefixed with **\*** render as:

----

.. doxygenclass:: SimpleList_3
   :project: lists

----

Unordered lists defined using HTML tags **<ul><li>** render as:

----

.. doxygenclass:: SimpleList_6
   :project: lists

----

Auto-numbered lists with list items prefixed with **-#** render as:

----

.. doxygenclass:: SimpleList_4
   :project: lists

----

Numbered lists with list items prefixed with Arabic numerals **1. 2. ...** render as:

----

.. doxygenclass:: SimpleList_5
   :project: lists

----

.. note:: Numbered lists support for the moment only Arabic numerals.

   
Nested lists are supported in all combinations, as long as they are valid doxygen markup.
Below are a couple of examples of different nested lists documentation and their corresponding 
breathe output.

Documentation looking like this:

.. literalinclude:: code/nested_list_1.h
   :language: cpp

renders as:

----

.. doxygenclass:: NestedLists_1
   :project: lists

----

Documentation looking like this:

.. literalinclude:: code/nested_list_2.h
   :language: cpp

renders as:

----

.. doxygenclass:: NestedLists_2
   :project: lists

----

Documentation looking like this:

.. literalinclude:: code/nested_list_3.h
   :language: cpp

renders as:

----

.. doxygenclass:: NestedLists_3
   :project: lists

----

Documentation looking like this:

.. literalinclude:: code/nested_list_4.h
   :language: cpp

renders as:

----

.. doxygenclass:: NestedLists_4
   :project: lists

----

Documentation looking like this:

.. literalinclude:: code/nested_list_5.h
   :language: cpp

renders as:

----

.. doxygenclass:: NestedLists_5
   :project: lists
