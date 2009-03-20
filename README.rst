
Breathe
=======

This is an extension to restructured text and Sphinx to be able to read and
render the Doxygen xml output.

Status
------

Still in planning and basic design stage.

Running Testsuite
-----------------

The ``generateDS.py`` scripts referenced below is Dave Kuhlman's Python module
available from `http://www.rexx.com/~dkuhlman/generateDS.html#download`.

::
   cd doxparsers/
   cp /path/to/generateDS.py generateDS.py
   ./generate.sh
   cd ../testsuite
   make html

Then view the resulting html with your browser of choice.

