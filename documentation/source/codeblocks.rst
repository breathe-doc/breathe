
Code Blocks
===========

Breathe suppports rendering code blocks with syntax highlighting provided by the
`Pygments <https://pygments.org/>`_ library.

The Doxygen syntax for code blocks supports specifying the language as follows:

.. code-block::

  \code{.py}
  class Python:
     pass
  \endcode

  @code{.cpp}
  class Cpp {};
  @endcode

Breathe will pass the language specified to Pygments to get accurate
highlighting.

Examples
--------

The following should render with standard C/C++ highlighting.

----

.. code-block:: cpp

   /** A function with an unannotated code block with C/C++ code.
    *
    * @code
    * int result = with_standard_code_block()
    * @endcode
    */
   void with_standard_code_block();

----

.. doxygenfunction:: with_standard_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

----

The following should render with no detected highlighting.

----

.. code-block:: cpp

   /** A function with an unannotated code block with non-C/C++ code.
    *
    * @code
    * set(user_list A B C)
    * for(element in ${user_list})
    *     message(STATUS "Element is ${element}")
    * endfor()
    * @endcode
    */
   void with_unannotated_cmake_code_block();

----

.. doxygenfunction:: with_unannotated_cmake_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

----

The following should render with specified cmake highlighting.

----

.. code-block:: cpp

   /** A function with an annotated cmake code block.
    *
    * @code{.cmake}
    * set(user_list A B C)
    * for(element in ${user_list})
    *     message(STATUS "Element is ${element}")
    * endfor()
    * @endcode
    */
   void with_annotated_cmake_code_block();

----

.. doxygenfunction:: with_annotated_cmake_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

