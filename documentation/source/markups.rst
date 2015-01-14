
Supported Markups
=================

All comments in your code must be formatted in a doxygen-compliant way so that
doxygen can do its job. Doxygen provides support for formatting your text with
tags, such as ``\b`` for adding bold text, this information appears in the xml
output and Breathe attempts to reproduce it accurately.

In addition to this, is it possible to add reStructuredText into your comments
within appropriately demarcated sections.

reStructuredText
----------------

Breathe supports reStructuredText within doxygen **verbatim** blocks which begin
with the markup **embed:rst**. This means that a comment block like this::

   /*!
   Inserting additional reStructuredText information.
   \verbatim embed:rst
   .. note::
   
      This reStructuredText has been handled correctly.
   \endverbatim
   */

Will be rendered as:

.. doxygenfunction:: TestClass::rawVerbatim
   :project: rst
   :no-link:

Handling Leading Asterisks
~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that doxygen captures **all** content in a **verbatim** block.  This can
be rather an annoyance if you use a leading-asterisk style of comment block
such as the following::

   /*!
    * Inserting additional reStructuredText information.
    *
    * \verbatim embed:rst
    *     Some example code::
    *
    *        int example(int x) {
    *            return x * 2;
    *        }
    * \endverbatim
    */

As the leading asterisks are captured in the **verbatim** block this will
appear to be an incorrectly formatted bullet list.  Due to the syntactical
problems Sphinx will issue warnings and the block will render as:

.. Here we fake the bad output without actually using a bad example otherwise
   we'll get warnings in the build output.

void **rawBadAsteriskVerbatim**\ ()

   Inserting additional reStructuredText information.

   - Some example code:
   - int example(int x) {
   - return x \* 2;
   - }

To prevent this, use an **embed:rst:leading-asterisk** tag::

   /*!
    * Inserting additional reStructuredText information.
    *
    * \verbatim embed:rst:leading-asterisk
    *     Some example code::
    *
    *        int example(int x) {
    *            return x * 2;
    *        }
    * \endverbatim
    */

This will appropriately handle the leading asterisks and render as:

----

.. doxygenfunction:: TestClass::rawLeadingAsteriskVerbatim
   :project: rst
   :no-link:

----

Handling Leading Slashes
~~~~~~~~~~~~~~~~~~~~~~~~

Similar troubles can be encountered when using comment blocks that start with a
triple forward slash. For example::

   /// Some kind of method
   ///
   /// @param something a parameter
   /// @returns the same value provided in something param
   ///
   /// @verbatim embed:rst:leading-slashes
   ///    .. code-block:: c
   ///       :linenos:
   ///
   ///       bool foo(bool something) {
   ///           return something;
   ///       };
   ///
   /// @endverbatim

For these kinds of blocks, you can use an **embed:rst:leading-slashes** tag as
shown in the above example.

This will appropriately handle the leading slashes and render as:

----

.. doxygenfunction:: TestClass::rawLeadingSlashesVerbatim
   :project: rst
   :no-link:

----

Aliases
~~~~~~~

To make these blocks appears as more appropriate doxygen-like markup in your
comments you can add the following aliases to your doxygen configuration file::

   ALIASES = "rst=\verbatim embed:rst"
   ALIASES += "endrst=\endverbatim"

And, if you use leading asterisks then perhaps::

   ALIASES += "rststar=\verbatim embed:rst:leading-asterisk"
   ALIASES += "endrststar=\endverbatim"

Which allow you to write comments like::

    /*!
    Inserting additional reStructuredText information.

    \rst

    This is some funky non-xml compliant text: <& !><

    .. note::
        
       This reStructuredText has been handled correctly.
    \endrst

    This is just a standard verbatim block with code:

    \verbatim
        child = 0;
        while( child = parent->IterateChildren( child ) )
    \endverbatim

    */

Which will be rendered as:

.. doxygenfunction:: TestClass::function
   :project: rst
   :no-link:


