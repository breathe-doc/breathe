
Breathe
=======

This is an extension to restructured text and Sphinx to be able to read and
render the Doxygen xml output.

Status
------

Basic functionality is in place with a reasonable output of the doxygen
information and some cross linking. The result of the testsuite is visible
here::

   http://michaeljones.github.com/breathe/

Running Testsuite
-----------------

This process assumes the ``sphinx-build`` script is on your path. If it is not,
then either edit ``testsuite/Makefile`` to point at it or create a link to it in
the ``testsuite`` directory.

First run ``make`` for each folder in the examples directory, then::

   cd testsuite
   make html

Then view the resulting html with your browser of choice.


