
Breathe
=======

This is an extension to restructured text and Sphinx to be able to read and
render the Doxygen xml output.

Status
------

Still in planning and basic design stage.

Running Testsuite
-----------------

The ``generateDS.py`` scripts referenced below is Dave Kuhlman's Pytho
module available from:

   `http://www.rexx.com/~dkuhlman/generateDS.html#download`.

This process assumes the ``sphinx-build`` script is on your path. If it is not,
then either edit ``testsuite/Makefile`` to point at it or create a link to it in
the ``testsuite`` directory::

   cd doxparsers/
   cp /path/to/generateDS.py generateDS.py
   ./generate.sh
   cd ../testsuite
   make html

Then view the resulting html with your browser of choice.

