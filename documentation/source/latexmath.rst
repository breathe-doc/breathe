
Latex Math
==========

Breathe has basic support for latex math markup in the doxygen comments.  A
class with a comment like::

   /**
    * @brief A class
    *
    * A inline formula: \f$ f(x) = a + b \f$
    *
    * A display style formula:
    * @f[
    * \int_a^b f(x) dx = F(b) - F(a)
    * @f]
    */
   class MathHelper 
   {
   public:
     MathHelper() {}
     ~MathHelper() {}
   }


Will be renderer as:

.. doxygenclass:: MathHelper
   :project: latexmath
   :members:
   :undoc-members:
   :no-link:


Without any additional configuration except for including a math extension in
the Sphinx ``conf.py``::

   extensions = [ "breathe", "sphinx.ext.mathjax" ]

The specific environment formula fails when using ``sphinx.ext.pngmath`` so more
work is needed.

Implementation
--------------

Breathe uses a internal reStructuredText node provided by
``sphinx.ext.mathbase`` which is then picked up and rendered by the extension
chosen in the ``conf.py``.  It does not pass any additional options through to
the node, so settings like ``label`` and ``nowrap`` are currently not supported.

Credits
-------

Thank you to `dazzlezhang <https://github.com/dazzlezhang>`_ for providing
examples and a full run down of necessary details.  It made the implementation
much easier.

