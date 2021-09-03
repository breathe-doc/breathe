Breathe
=======

**Packagers:** Breathe packages on PyPI are PGP signed for Breathe >= v4.28.0.

**Packagers:** Breathe tarballs on GitHub are PGP signed for Breathe >= v4.29.0.

.. image:: https://github.com/michaeljones/breathe/workflows/unit%20tests/badge.svg
    :target: https://github.com/michaeljones/breathe/actions?query=workflow%3A%22unit+tests%22

This is an extension to reStructuredText and Sphinx to be able to read and
render the Doxygen xml output.

Download
--------

Breathe is available from github and `PyPI, the Python Package Index
<http://pypi.python.org/pypi/breathe>`_. It can be installed with::

    pip install breathe

Documentation
-------------

The documentation is available `here <http://breathe.readthedocs.org/>`__. Thank
you to the people running `Read the Docs <http://readthedocs.org>`_ for such an
excellent service.

The source for the documentation is in the ``documentation`` folder if you want
to built it and read it locally.

Note
~~~~

Breathe does not always get the attention it deserves but I am keen to keep it
moving forward. If you report an issue, please keep reminding me about it until
it is fixed. I should be better at this but in silence I tend to move to other
things so keep reminding me.

Testing
-------

The testsuite can be run with::

    make dev-test

The documentation also does a good effort of covering the available
functionality with different examples. To build the documentation, run::

    make

This will run doxygen over the example code and then run the Breathe
documentation. View the results at::

    documentation/build/html/index.html

Further to this if you want to compare the current documentation output against
a previous state in order to check for regressions there is a ``compare`` script
in the ``documentation`` folder. It takes two arguments which are two commit
references that you'd like to compare. This means that all your changes have to
be committed first. Also the script does not resolve state dependent references
like ``HEAD`` so provide concrete commit references like sha1s or branch names.
A typical example is to compare your current branch output to master::

    # Make sure all your changes are committed first
    cd documentation
    ./compare master my-branch

This will do a checkout and build at each commit and then run ``meld`` against
the resulting directories so you can see the differences introduced by your
branch.

Requirements
------------

Development is currently done with:

- Python 3.5
- Docutils 0.12
- Sphinx 2.3.1
- Doxygen 1.8.4

Doxygen 1.5.1 seems to produce xml with repeated sections which causes Breathe
some confusion. Not sure when this was resolved but it might be best to go for
the latest possible.

Mailing List Archives
---------------------

The archive for the Google groups list can be found
`here <https://groups.google.com/forum/#!forum/sphinx-breathe>`__.

The previous mailing list was on `librelist.com <http://librelist.com>`__ and the
archives are available `here <http://librelist.com/browser/breathe/>`__.

Please post new questions as GitHub issues.

Examples
--------

Examples of Breathe used by other projects:

- `fmt <http://fmtlib.net/latest>`_
- `Lasso C API <http://lassoguide.com/api/lcapi-reference.html>`_
  [`pdf <http://lassoguide.com/LassoGuide9.2.pdf>`__]

If you have an example you would like listed here, please make a github issue
with the details.

Alternatives
------------

Breathe is not the only solution to this problem. These are the alternatives
that we know about. We are very happy to list others if you'd like to provide a
link in a GitHub issue.

- `Gasp <https://github.com/troelsfr/Gasp>`_
- `Robin <https://bitbucket.org/reima/robin>`_
- `sphinxcontrib-autodoc_doxygen <https://github.com/rmcgibbo/sphinxcontrib-autodoc_doxygen>`_

Release
-------

See the mkrelease utility in the root of the repository.

Credits
-------

Breathe is currently maintained by `vermeeren <https://github.com/vermeeren>`_
and was formerly maintained by `michaeljones <https://github.com/michaeljones>`_
& `vitaut <https://github.com/vitaut>`_, contributors include:

- `nijel <https://github.com/nijel>`_
- `sebastianschaetz <https://github.com/sebastianschaetz>`_
- `mbolivar <https://github.com/mbolivar>`_
- `queezythegreat <https://github.com/queezythegreat>`_
- `abingham <https://github.com/abingham>`_
- `davidm <https://github.com/davidm>`_
- `hobu <https://github.com/hobu>`_
- `magro11 <https://github.com/magro11>`_
- `scopatz <https://github.com/scopatz>`_
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
- `dean0x7d <https://github.com/dean0x7d>`_
- `Andne <https://github.com/Andne>`_
- `Tiwalun <https://github.com/Tiwalun>`_
- `eric-wieser <https://github.com/eric-wieser>`_
- `olitheolix <https://github.com/olitheolix>`_
- Many more, this list is rather outdated. Refer to the git history.

Thanks to:

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx-doc.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and reStructuredText.

Changelog
---------

See the `CHANGELOG.rst
<https://github.com/michaeljones/breathe/blob/master/CHANGELOG.rst>`_
