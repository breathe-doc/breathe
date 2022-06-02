.. raw:: html

   <div align="center">
     <a href="https://www.breathe-doc.org">
       <img width="200" height="200" src="https://www.breathe-doc.org/img/logo.svg">
     </a>
   </div>

   <h1 align="center">
     Breathe
   </h1>

   <p align="center">
      Your technical docs, beautifully integrated
   </p>

   <p align="center">
        <a href="https://www.breathe-doc.org/">Website</a>
      • <a href="https://breathe.readthedocs.io/en/latest/">Documentation</a>
      • <a href="https://opencollective.com/breathe">Sponsor</a>
   </p>

   <p align="center">
      <a href="https://github.com/michaeljones/breathe/actions?query=workflow%3A%22unit+tests%22">
         <img src="https://github.com/michaeljones/breathe/workflows/unit%20tests/badge.svg">
      </a>
   </p>


**Sponsor**: If you benefit from using Breathe as a company or an individual, you
can financially support the Breathe project with recurring or one off
contributions via `Open Collective <https://opencollective.com/breathe>`_.

----

Breathe is a Sphinx plugin providing beautifully integrated Doxygen output in
your user-facing documentation. It allows you to combine Doxygen's excellent
technical understanding of your code base with the superb long form
documentation output of the Sphinx system.

For Packagers
-------------

- Breathe packages on PyPI are PGP signed for Breathe >= v4.28.0.
- Breathe tarballs on GitHub are PGP signed for Breathe >= v4.29.0.

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

Breathe requires Python 3.6+, Sphinx 4.0+ and Doxygen 1.8+.

Mailing List Archives
---------------------

The archive for the Google groups list can be found
`here <https://groups.google.com/forum/#!forum/sphinx-breathe>`__.

The previous mailing list was on `librelist.com <http://librelist.com>`__ and the
archives are available `here <http://librelist.com/browser/breathe/>`__.

Please post new questions as GitHub issues.

Projects Using Breathe
----------------------

Examples of projects that use Breathe:

- `PyTorch <https://github.com/pytorch/pytorch>`_
- `OpenPilot <https://github.com/commaai/openpilot>`_
- `XGBoost <https://github.com/dmlc/xgboost>`_
- `NumPy <https://github.com/numpy/numpy>`_
- `Mozilla's DeepSpeech <https://github.com/mozilla/DeepSpeech>`_
- `Microsoft's LightGBM <https://github.com/microsoft/LightGBM>`_
- `PyBind11 <https://github.com/pybind/pybind11>`_
- `Ceph <https://github.com/ceph/ceph>`_
- `Apache Arrow <https://github.com/apache/arrow>`_
- `LVGL <https://github.com/lvgl/lvgl>`_
- `Espressif IoT Development Framework <https://github.com/espressif/esp-idf>`_
- `Zephyr Project <https://github.com/zephyrproject-rtos/zephyr>`_
- `Plaid ML <https://github.com/plaidml/plaidml>`_
- `Sony's Neural Network Libraries <https://github.com/sony/nnabla>`_
- `fmt <http://fmtlib.net/latest>`_

Release
-------

See the ``mkrelease`` utility in the root of the repository.

Useful vim command for changelog conversion to the git tag format:
``%s/\v`(#[0-9]+) \<[^`]*`__/\1/g``.

Maintainers
-----------

Breathe is currently maintained by `vermeeren <https://github.com/vermeeren>`_ & `jakobandersen <https://github.com/jakobandersen>`_
and was formerly maintained by `michaeljones <https://github.com/michaeljones>`_
& `vitaut <https://github.com/vitaut>`_.

See `CONTRIBUTORS </CONTRIBUTORS.rst>`_ for the full list.

Acknowledgements
----------------

- Dimitri van Heesch for `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_.
- Georg Brandl for `Sphinx <http://sphinx-doc.org>`_.
- David Goodger for `Docutils <http://docutils.sourceforge.net/>`_ and reStructuredText.

Changelog
---------

See the `CHANGELOG.rst
<https://github.com/michaeljones/breathe/blob/master/CHANGELOG.rst>`_
