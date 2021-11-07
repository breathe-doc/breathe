Using Dot Graphs
================

.. _graphviz: https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html#module-sphinx.ext.graphviz
.. _dot: https://www.doxygen.nl/manual/commands.html#cmddot
.. _dotfile: https://www.doxygen.nl/manual/commands.html#cmddotfile

By default, breathe will translate any dot_ and dotfile_ commands into
Sphinx graphviz_ directives. However, there are some caveats:

1. The only graphviz_ option supported is the ``caption`` option. Graph captions are optionally
   specified using the dot_ or dotfile_ command syntax. All other graphviz_ directive options
   fallback to their default behavior.

   - any size hints from Doxygen's dot_ or dotfile_ commands are ignored.
2. Using Doxygen's ``@ref`` command within any dot syntax is functionally ignored and treated as
   literal text.

Sphinx graphviz prerequisites
-----------------------------

To use Sphinx's graphviz_ directive at all, the project documentation's ``conf.py`` file must have
``sphinx.ext.graphviz`` added to the list of ``extensions``.

.. code-block:: python

    extensions = ["breathe", "sphinx.ext.graphviz"]

.. seealso::
    To obtain the dot executable from the Graphviz library, see
    `the library's downloads section <https://graphviz.org/download/>`_.
.. note::
    Typically, the dot executable's path should be added to your system's ``PATH`` environment
    variable. This is required for Sphinx (not Doxygen when only outputting XML), although
    the configuration option,
    `graphviz_dot <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html#confval-graphviz_dot>`_,
    can compensate for abnormal dot executable installations.
