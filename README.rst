Breathe
=======

This is an extension to restructured text and Sphinx to be able to read and
render the Doxygen xml output.

Documentation
-------------

Documentation is available in the ``testsuite`` folder and up in full `here
<http://michaeljones.github.com/breathe>`_.

Running Testsuite
-----------------

This process assumes the ``sphinx-build`` script is on your path. If it is not,
then either edit ``testsuite/Makefile`` to point at it or create a link to it in
the ``testsuite`` directory.

First run ``make`` for each folder in the examples directory, then::

   cd testsuite
   make html

Then view the resulting html with your browser of choice.


Requirements
------------

Development is currently done with:
 
- Python 2.5
- Docutils 0.7
- Sphinx 1.0.4
- Doxygen 1.7.2

Doxygen 1.5.1 seems to produce xml with repeated sections which causes Breathe
some confusion. Not sure when this was resolved but it might be best to go for
the latest possible.

Credits
-------

Thank you to:

- `nijel <http://github.com/nijel>`_
- `sebastianschaetz <http://github.com/sebastianschaetz>`_
- `mbolivar <http://github.com/mbolivar>`_

For their contributions; improving the code and the documentation. And thanks to:

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx.pocoo.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and Restructured Text. 

