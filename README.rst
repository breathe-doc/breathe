Breathe
=======

This is an extension to reStructuredText and Sphinx to be able to read and
render the Doxygen xml output.

Download
--------

Breathe is available from github and `PyPI, the Python Package Index
<http://pypi.python.org/pypi/breathe>`_

Documentation
-------------

Documentation is available in the ``testsuite`` folder and up in full `here
<http://michaeljones.github.com/breathe>`_.

Running Testsuite
-----------------

Run ``make`` in the root of the project. 

This will run doxygen over the example code and then run the Breathe
documentation/testsuite. View the results at::

   testsuite/build/html/index.html

Requirements
------------

Development is currently done with:
 
- Python 2.7
- Docutils 0.7
- Sphinx 1.0.7
- Doxygen 1.7.2

Doxygen 1.5.1 seems to produce xml with repeated sections which causes Breathe
some confusion. Not sure when this was resolved but it might be best to go for
the latest possible.

Mailing List
------------

There is a mailing list available thanks to `LibreList <http://librelist.com>`_::

    breathe@librelist.com

The archives are available `here <http://librelist.com/browser/breathe/>`_.

Credits
-------

Thank you to:

- `nijel <https://github.com/nijel>`_
- `sebastianschaetz <https://github.com/sebastianschaetz>`_
- `mbolivar <https://github.com/mbolivar>`_
- `queezythegreat <https://github.com/queezythegreat>`_
- `abingham <https://github.com/abingham>`_
- `davidm <https://github.com/davidm>`_
- `hobu <https://github.com/hobu>`_

For their contributions; improving the code and the documentation. And thanks to:

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx.pocoo.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and reStructuredText. 

