
Breathe
=======

.. image:: https://travis-ci.org/michaeljones/breathe.svg?branch=travis
    :target: https://travis-ci.org/michaeljones/breathe

This is an extension to reStructuredText and Sphinx to be able to read and
render the Doxygen xml output.

Download
--------

Breathe is available from github and `PyPI, the Python Package Index
<http://pypi.python.org/pypi/breathe>`_

Documentation
-------------

The documentation is available `here <http://breathe.readthedocs.org/>`__. Thank
you to the people running `Read the Docs <http://readthedocs.org>`_ for such an
excellent service.

The source for the documentation is in the ``documentation`` folder if you want
to built it and read it locally.

Testing
-------

Breathe doesn't have a set of tests at the moment. The documentation does a good
job of running the different parts of the Breathe functionality but there is
nothing to check that the output is appropriate.

To build the documentation, run ``make`` in the root of the project. 

This will run doxygen over the example code and then run the Breathe
documentation. View the results at::

   documentation/build/html/index.html

Requirements
------------

Development is currently done with:
 
- Python 2.7.4
- Docutils 0.11
- Sphinx 1.2.2
- Doxygen 1.8.4

Doxygen 1.5.1 seems to produce xml with repeated sections which causes Breathe
some confusion. Not sure when this was resolved but it might be best to go for
the latest possible.

Mailing List
------------

There is a mailing list available on Google groups:

    https://groups.google.com/forum/#!forum/sphinx-breathe

The previous mailing list was on `librelist.com <http://librelist.com>`__ and the
archives are available `here <http://librelist.com/browser/breathe/>`__.

Examples
--------

Examples of Breathe used by other projects:

- `cppformat <http://cppformat.readthedocs.org/en/latest/>`_
  [`pdf <https://media.readthedocs.org/pdf/cppformat/master/cppformat.pdf>`_]

If you have an example you would like listed here, please make a github issue
with the details.

Alternatives
------------

Breathe is not the only solution to this problem. These are the alternatives
that we know about. We are very happy to list others if you'd like to provide a
link in a github issue or get in touch on the mailing list.

- `Gasp <https://github.com/troelsfr/Gasp>`_
- `Robin <https://bitbucket.org/reima/robin>`_

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
- `magro11 <https://github.com/magro11>`_
- `scopatz <https://github.com/scopatz>`_
- `vitaut <https://github.com/vitaut>`_
- `vonj <https://github.com/vonj>`_
- `jmnas <https://github.com/jmnas>`_
- `donkopotamus <https://github.com/donkopotamus>`_
- `jo3w4rd <https://github.com/jo3w4rd>`_
- `Anthony Truchet <https://github.com/AnthonyTruchet>`_
- `Daniel Matz <https://github.com/danielmatz>`_
- `Andrew Hundt <https://github.com/ahundt>`_
- `sebastinas <https://github.com/sebastinas>`_
- `robo9k <https://github.com/robo9k>`_
- `sieben <https://github.com/sieben>`_
- `rweickelt <https://github.com/rweickelt>`_
- `sam-roth <https://github.com/sam-roth>`_
- `bnewbold <https://github.com/bnewbold>`_
- `serge-sans-paille <https://github.com/serge-sans-paille>`_

For their contributions; reporting issues and improving the code and
documentation. And thanks to:

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx-doc.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and reStructuredText. 

Change Log
----------

Inspired by `Keepachangelog.com <http://keepachangelog.com/>`__.

- Changes since the last release

  - Nothing

- 2014-11-09 - Breathe v3.2.0

  - Nothing Added, Deprecated or Removed

  - Fixed

    - Changed docutils/Sphinx node usage to fix latex/pdf output.

    - When checking for path separators check for both ``/`` and ``\``
      regardless of the platform.

    - ``KeyError`` when using ``auto`` directives without specifying the
      ``:project:`` option even though the default project config setting was
      set.

    - Use of ``doxygenfunction`` no longer inappropriately triggers the
      duplicate target check and fails to output link targets.

    - Support for inline urls in the doxygen comments.

    - Support for array notation in function parameters.

    - Reduced intention by changing ``section-defs`` to use ``container`` &
      ``rubric`` nodes rather than ``desc`` nodes with signatures & content. Now
      headings like 'Public Functions' appear inline with their subject matter.

- 2014-09-07 - Breathe v3.1.0

  - Nothing Deprecated or Removed

  - Added

    - The ``doxygenclass`` directive can now reference template specialisations
      by specifying the specialisation in the argument name.

  - Fixed

    - Displaying function parameters for Qt slots output. Previously they were
      missing even though Qt Slots are essentially just functions.

    - Displaying headings from doxygen comments as emphasized text.

    - Crash when generating warning about being unable to find a define,
      variable, enum, typedef or union.

    - Only output the definition name for a function parameter if the declartion
      name is not available. Previously, where they were both available we were
      getting two names next to each other for no good reason.

- 2014-08-04 - Breathe v3.0.0

  - Improve output of const, volatile, virtual and pure-virtual keywords.

  - Fix css class output for HTML so that object types rather than names are
    output as the css classes. eg. 'function' instead of 'myFunction'.

  - Fix issue with Breathe getting confused over functions appearing in header
    and implementation files.

  - Improve matching for overloaded functions when using ``doxygenfunction``
    directive. Also, provide a list of potential matches when no match is found.

  - Improved ``:members:`` implementation to handle inner classes properly.

  - Updated ``doxygenstruct`` to share the ``doxygenclass`` implementation path
    which grants it the options from ``doxygenclass`` directive.

  - Added ``:outline:`` option support to ``doxygengroup`` &
    ``doxygennamespace`` directives.

  - Added ``doxygennamespace`` directive.

  - Added ``:undoc-members:`` option to ``doxygenclass`` & ``doxygengroup``
    directives.

  - **Breaking change**: Removed ``:sections:`` option for ``doxygenclass`` &
    ``doxygengroup`` directives and replaced it with ``:members:``,
    ``:protected-members:`` and ``:private-members:``, and changed
    ``breathe_default_sections`` config variable to ``breathe_default_members``.
    This is designed to more closely match the Sphinx autodoc functionality and
    interface.

- 2014-06-15 - Breathe v2.0.0

  - Add compare script for checking changes to documentation caused by changes
    in the implementation.

  - Switched to ``https`` reference for MathJax Javascript.

  - **Breaking change**: Change ``autodoxygen*`` directives to require
    explicitly declared source files in the ``conf.py`` rather than attempting
    to detect them from the directive arguments.

  - Switch documentation hosting to ReadTheDocs.org.

  - **Breaking change**: Switch to assuming all relative paths are relative to
    the directory holding the ``conf.py`` file. Previously, it would assume they
    were relative to the user's current working directory. This breaks projects
    which use separate build & source directories.

  - Add ``doxygenunion`` directive.

  - Add ``doxygengroup`` directive.

  - Add support for lists in the output. They were previously ignored.

  - Updated implementation to use the docutils nodes that Sphinx does where
    possible.

- Breathe v1.2.0

  - Change log not recorded.

