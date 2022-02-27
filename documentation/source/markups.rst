
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

.. cpp:namespace:: @ex_markups_rst

Breathe supports reStructuredText within doxygen **verbatim** blocks which begin
with the markup **embed:rst**. This means that a comment block like this:

.. code-block:: cpp

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

.. cpp:namespace:: @ex_markups_leading_star

Note that doxygen captures **all** content in a **verbatim** block.  This can
be rather an annoyance if you use a leading-asterisk style of comment block
such as the following:

.. code-block:: cpp

   /*!
    * Inserting additional reStructuredText information.
    *
    * \verbatim embed:rst
    *     Some example code
    *
    *     .. code-block:: cpp
    *
    *        int example(int x) {
    *            return x * 2;
    *        }
    * \endverbatim
    */

As the leading asterisks are captured in the **verbatim** block this will
appear to be an incorrectly formatted bullet list.  Due to the syntactical
problems Sphinx will issue warnings and the block will render as:

..
   Here we fake the bad output without actually using a bad example otherwise
   we'll get warnings in the build output.

void **rawBadAsteriskVerbatim**\ ()

   Inserting additional reStructuredText information.

   - Some example code:
   - int example(int x) {
   - return x \* 2;
   - }

To prevent this, use an **embed:rst:leading-asterisk** tag:

.. code-block:: cpp

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

----

Handling Leading Slashes
~~~~~~~~~~~~~~~~~~~~~~~~

.. cpp:namespace:: @ex_markups_leading_slash

Similar troubles can be encountered when using comment blocks that start with a
triple forward slash. For example:

.. code-block:: cpp

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
   /// @note Documentation using `///` should begin and end in a blank line.

For these kinds of blocks, you can use an **embed:rst:leading-slashes** tag as
shown in the above example.

This will appropriately handle the leading slashes and render as:

----

.. doxygenfunction:: TestClass::rawLeadingSlashesVerbatim
   :project: rst

----

Inline rST
~~~~~~~~~~

.. cpp:namespace:: @ex_markups_inline

Normal verbatim elements result in block elements. But sometimes you'll want
to generate rST references where they need to be rendered inline with the text.
For example:

.. code-block:: cpp

   /// Some kind of method
   ///
   /// @param something a parameter
   /// @returns the same value provided in something param
   ///
   /// @verbatim embed:rst:inline some inline text @endverbatim

For these kinds of references, you can use an **embed:rst:inline** tag as
shown in the above example.

This will appropriately handle the leading slashes and render as:

----

.. doxygenfunction:: TestClass::rawInlineVerbatim
   :project: rst

.. doxygenfunction:: TestClass::rawVerbatim
   :project: rst
   :outline:

----

Aliases
~~~~~~~

.. cpp:namespace:: @ex_markups_aliases

To make these blocks appear as more appropriate doxygen-like markup in your
comments you can add the following aliases to your doxygen configuration file:

.. code-block:: text

   ALIASES = "rst=^^\verbatim embed:rst^^"
   ALIASES += "endrst=\endverbatim"

Which allow you to write comments like:

.. code-block:: cpp

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

.. note::

   The character sequence ``^^`` in an ALIAS definition inserts a line break.
   The leading ``^^`` ensures that a RST ``\verbatim`` block never starts in a brief description
   (which would break the output), even if you put it on the first line of a comment.
   The trailing ``^^`` allows to start with RST content on the same line of the ``\rst`` command.

The ALIAS given above only works for comment blocks without a leading comment character on each line.
If you use a comment style with a leading comment character on each new line,
use these aliases instead:

.. code-block:: text

   ALIASES = "rst=^^\verbatim embed:rst:leading-asterisk^^"
   ALIASES += "endrst=\endverbatim"

Due to an `undocumented behavior in doxygen <https://github.com/doxygen/doxygen/issues/8907>`_,
all leading comment characters (``*``, ``///`` or ``//!``) encountered in a verbatim section
will be converted to asterisk (``*`` ) by Doxygen, when ``\verbatim`` is part of an alias.
Therefore, the ALIAS above works in all comment blocks with leading line comment characters.

If you want to hide reStructuredText output from Doxygen html and only include it in sphinx,
use the Doxygen command ``\xmlonly``.
This is an example alias that enables all RST sections in XML only:

.. code-block:: text

    ALIASES = "rst=^^\xmlonly<verbatim>embed:rst:leading-asterisk^^"
    ALIASES += "endrst=</verbatim>\endxmlonly"
