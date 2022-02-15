
Code Blocks
===========

Breathe supports rendering code blocks with syntax highlighting provided by the
`Pygments <https://pygments.org/>`_ library. By default, Breathe will assume
that code blocks match the language of the source file, but you can also specify
the language of the code blocks using
`Doxygen's code command <https://www.doxygen.nl/manual/commands.html#cmdcode>`_
or `MarkDown's fenced code blocks <https://www.doxygen.nl/manual/markdown.html#md_fenced>`_.

.. note::
   Any hyperlinked text found within the code blocks rendered with Doxygen's HTML output
   will not be hyperlinked in any Sphinx output due to the use of the Pygments library.
   As a benefit, a code-block's syntax highlighting can be any syntax supported by
   Pygments (which is much more than only the languages supported by Doxygen's parsers).

The Doxygen syntax for code blocks supports specifying the language as follows:

.. code-block::

   \code{.py}
   class Python:
      pass
   \endcode

   @code{.cpp}
   class Cpp {};
   @endcode

This technique can also be utilized from MarkDown syntax/files

.. code-block:: markdown

   ```py
   class Python:
      pass
   ```

   ```cpp
   class Cpp {};
   ```

Breathe will pass the language specified to Pygments to get accurate
highlighting. If no language is explicitly provided (either from ``\code``
command or via Doxygen's XML output about the language documented), then
Pygments will try to guess what syntax the code block is using (based on
the code block's contents).

Examples
--------

The following should render with standard C/C++ highlighting. Notice, the
syntax is automatically highlighted as C++ because the documented function
exists in a C++ source file.

----

.. code-block:: cpp

   /** A function with an unannotated code block with C/C++ code.
    *
    * @code
    * char *buffer = new char[42];
    * int charsAdded = sprintf(buffer, "Tabs are normally %d spaces\n", 8);
    * @endcode
    */
   void with_standard_code_block();

----

.. doxygenfunction:: with_standard_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

----

The following should render with no detected highlighting.
Notice, there is no syntax highlighting because Pygments does not
recognize the code block's contained syntax as a C++ snippet.

----

.. code-block:: cpp

   /** A function with an unannotated code block with non-C/C++ code.
    *
    * @code
    * set(user_list A B C)
    * foreach(element ${user_list})
    *     message(STATUS "Element is ${element}")
    * endforeach()
    * @endcode
    * 
    * Another code-block that explicitly remains not highlighted.
    * @code{.unparsed}
    * Show this as is.
    * @endcode
    */
   void with_unannotated_cmake_code_block();

----

.. doxygenfunction:: with_unannotated_cmake_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

----

The following should render with specified CMake highlighting. Here, the syntax
highlighting is explicitly recognized as a CMake script snippet which overrides
the inherent C++ context.

----

.. code-block:: cpp

   /** A function with an annotated cmake code block.
    *
    * @code{.cmake}
    * set(user_list A B C)
    * foreach(element ${user_list})
    *     message(STATUS "Element is ${element}")
    * endforeach()
    * @endcode
    */
   void with_annotated_cmake_code_block();

----

.. doxygenfunction:: with_annotated_cmake_code_block
   :path: ../../examples/specific/code_blocks/xml
   :no-link:

.. warning::
   Pygments will raise a warning in the Sphinx build logs if
   the specified syntax does conform the specified syntax's convention(s).
