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

Run ``make`` in the root of the project. 

This will run doxygen over the example code and then run the Breathe
documentation/testsuite. View the results at::

   testsuite/build/html/index.html

Requirements
------------

Development is currently done with:
 
- Python 2.5
- Docutils 0.7
- Sphinx 1.0.7
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
- `queezythegreat <https://github.com/queezythegreat>`_

For their contributions; improving the code and the documentation. And thanks to:

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx.pocoo.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and Restructured Text. 

