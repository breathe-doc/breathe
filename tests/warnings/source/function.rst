
Function Warnings
=================

Test 'cannot find project' warning.

.. doxygenfunction:: MyFunction
   :project: nonexistent


Test 'cannot find xml' warning:

.. doxygenfunction:: MyFunction
   :project: invalidproject


Test 'cannot find function' warning.

.. doxygenfunction:: NonExistentFunction
   :project: function


Test 'too many matches' warning.

.. doxygenfunction:: f
   :project: function
