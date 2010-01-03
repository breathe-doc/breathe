
Breathe
=======

This is an extension to restructured text and Sphinx to be able to read and
render the Doxygen xml output.

Status
------

This has passed proof of concept stage and has proved itself to be a useful
tool. The testsuite is currently out of date and no unit tests have been
written. It is usable, but will generate a couple of warnings from time to time.

Running Testsuite
-----------------

This process assumes the ``sphinx-build`` script is on your path. If it is not,
then either edit ``testsuite/Makefile`` to point at it or create a link to it in
the ``testsuite`` directory.

First run ``make`` for each folder in the examples directory, then::

   cd testsuite
   make html

Then view the resulting html with your browser of choice.


