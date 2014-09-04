
Deviations from Doxygen & Autodoc
=================================

As Breathe attempts to bridge the gap between Sphinx and Doxygen it is confined
by both what Doxygen outputs in its XML and what Sphinx will accept through the
Docutils document model.

This leads to a few differences between Breathe output and the Doxygen HTML
output and the Sphinx Autodoc output.

These are incomplete lists but we're keen to expand them as issues are brought
to our attention.

Doxygen
-------

- Doxygen allows both HTML and Markdown syntax for headings in comments. These
  are rendered as standard HTML headings in the output (h1, h2, h3, etc.)

  RestructuredText only allows headings at the start of document sections and
  you cannot put arbitrary sections into the output to gain the appearance of
  headings so any headings found in the doxygen comments are rendered as
  emphasized text in the Breathe HTML output.


Sphinx Autodoc
--------------

- No differences highlighted yet, though they certainly exist.
