
Supported Markups
=================

All comments in your code must be formatted in a doxygen-compliant way so that
doxygen can do its job. Doxygen provides support for formatting your text with
tags, such as ``\b`` for adding bold text, this information appears in the xml
output and Breathe attempts to reproduce it accurately.

In addition to this, is it possible to add restructured text into your comments
within appropriately demarcated sections. 

Restructured Text
-----------------

Breathe supports restructed text within doxygen **verbatim** blocks which begin
with the markup **embed:rst**. This means that a comment block like this::

   /*!
   Inserting additional restructured text information.
   \verbatim embed:rst
   .. note::
   
      This restructured text has been handled correctly.
   \endverbatim
   */

Will be rendered as:

.. doxygenfunction:: TestClass::rawVerbatim
   :project: rst

Aliases
~~~~~~~

To make these blocks appears as more appropriate doxygen-like markup in your
comments you can add the following aliases to your doxygen cofiguration file::

   ALIASES = "rst=\verbatim embed:rst"
   ALIASES += "endrst=\endverbatim"

Which allow you to write comments like::

    /*!
    Inserting additional restructured text information.

    \rst

    This is some funky non-xml compliant text: <& !><

    .. note::
        
       This restructured text has been handled correctly.
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


