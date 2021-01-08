Breathe
=======

**Packagers:** PGP signing key changes for Breathe >= v4.23.0.
https://github.com/michaeljones/breathe/issues/591

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

Command for releasing source bundle & wheel to PyPI::

    python setup.py sdist bdist_wheel upload

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

Change Log
----------

Inspired by `Keepachangelog.com <http://keepachangelog.com/>`__.

- 2021-01-08 - Breathe v4.26.0

  - Add test for ellipsis ('...') in args. #610
  - Sphinx 3.4.x compatibility. #617
  - Adapt friendclass to Doxygen 1.9. #618

- 2020-12-16 - Breathe v4.25.1

  - Addendum to #606, for functions with '...'. #609

- 2020-12-15 - Breathe v4.25.0

  - Add support for \parblock parsing and rendering. #603
  - Allow lookup in doxygenfunction without writing param names. #606

- 2020-12-01 - Breathe v4.24.1

  - Fix anchors on pages generated by Doxygen >= 1.8.17. #602

- 2020-11-15 - Breathe v4.24.0

  - Update CI for Sphinx 3.3.x and fix test mock. #597
  - Add support for xrefitem based page generation (doxygenpage). #596

- 2020-10-20 - Breathe v4.23.0

  - Add initial xrefsect support. #589

- 2020-09-26 - Breathe v4.22.1

  - Fix anonymous struct/union usage in C domain. #585

- 2020-09-19 - Breathe v4.22.0

  - Fix Read the Docs build (again). #576
  - New boolean `breathe_show_enumvalue_initializer` option specifying
    whether value of enumvalue should be displayed. #581

- 2020-09-10 - Breathe v4.21.0

  - Fix Read the Docs build. #567
  - Document doxygenclass template specialisation spacing. #570
  - Update upper Sphinx release to <3.4. #571
  - Reuse breathe.__version__ in setup.py. #572
  - Document :inner: for the doxygengroup section. #573
  - Add support for verbatim inline elements. #560
  - Fix wrong refid when Doxygen SEPARATE_MEMBER_PAGES is YES. #566

- 2020-08-19 - Breathe v4.20.0

  - Allow Sphinx 3.2. #561
  - Update CI scripts with new Sphinx versions. #552
  - Add support for C# using sphinx-csharp. #550
  - Doc, fix typo, :source: -> :project:. #551
  - Add support for innergroup. #556
  - Avoid duplicate doxygen targets when debug tracing. #563
  - Remove Travis badge from README file. #564

- 2020-06-17 - Breathe v4.19.2

  - Fix crash when visiting typedef. #547

- 2020-06-08 - Breathe v4.19.1

  - Mark package as compatible with Sphinx 3.1.

- 2020-06-07 - Breathe v4.19.0

  - Refactoring. #528
  - Make debug config variables available in conf.py. #533
  - Fix warning formatting for function lookup. #535
  - Correctly reverse nested namespaces in get_qualification. #540

- 2020-05-10 - Breathe v4.18.1

  - Fix friend class rendering and allow friend struct. #522
  - Add extern examples to doc and remove variable hack. #526
  - Render function candidates without using Sphinx directives. #524

- 2020-05-02 - Breathe v4.18.0

  - Support tiles in verbatim blocks. #517

- 2020-05-01 - Breathe v4.17.0

  - Scoped rendering, better integration with Sphinx, misc fixes. #512

- 2020-04-19 - Breathe v4.16.0

  - Strictly depend on Sphinx's minor version. #498
  - Simplifications and fixes, use more of modern Sphinx natively. #503
  - Add section option to the doxygen(auto)file directive. #501
  - Fix link generation when enum is inside a group (enum FQDN). #508
  - Fix creation of LaTeX math formulas. #506
  - Improve documentation for doxygen(auto)file section option. #509

- 2020-04-07 - Breathe v4.15.0

  - Add license file to distribution. #492
  - Update for Sphinx 3. #491

- 2020-04-07 - Breathe v4.14.2

  - Add GitHub actions. #474
  - Fixes to use Sphinx 2.4.4. #486
  - Add nose to python development requirements. #484.
  - Switch to pytest from nose. #487

- 2020-02-02 - Breathe v4.14.1

  - Use sphinx core instead of mathbase ext. #469
  - Fix test failure for Sphinx >= 2.2.2. #472
  - Update travis to Sphinx 2.3.1. #471

- 2019-11-26 - Breathe v4.14.0

  - Add events attribute to MockApp. #452
  - Add bit field support for C/C++. #454
  - Add alias and variable template support. #461

- 2019-08-01 - Breathe v4.13.1

  - Fix for template method pointer parameter issue. #449

- 2019-04-23 - Breathe v4.13.0.post0

  - Drop support for python 2, require Sphinx >= 2.0. #432

- 2019-04-21 - Breathe v4.13.0

  - Adapt to upcoming Sphinx 2.0. #411
  - Add support for rendering parameter direction information. #428

- 2019-03-15 - Breathe v4.12.0

  - Adapt to Sphinx 1.8. #410
  - Let Sphinx handle more things. #412
  - Use standard windows EOL for batch file. #417
  - Fix flake8 F632 warnings. #418
  - Update dep versions in readme, setup, requirements. #419
  - Add option to render function parameters after the description. #421
  - Remove spurious "typedef" in type declaration when using "using". #424

- 2018-12-11 - Breathe v4.11.1

  - Sphinxrenderer: handle typeless parameters gracefully. #404

- 2018-10-31 - Breathe v4.11.0

  - Fix typo in quickstart. #393
  - Add support for QtSignals. #401

- 2018-08-07 - Breathe v4.10.0

  - Explicitly use Sphinx 1.7.5 for CI and dev. #385
  - Print filename when printing ParserException. #390

- 2018-06-03 - Breathe v4.9.1

  - Don't append separator for paragraph type. #382

- 2018-06-01 - Breathe v4.9.0

  - Render newlines as separate paragraphs. #380

- 2018-05-26 - Breathe v4.8.0

  - Add quiet option to apidoc. #375
  - Add PHP domain. #351
  - Keep templates on adjacent lines. #300
  - Show reference qualification for methods. #332
  - Adapt tests/CI to newest Sphinx version. #377
  - More robust name regex in renderer. #370
  - Show base classes using Sphinx's cpp domain. #295
  - Fix domain detection when rendering groups. #365
  - Return parallel_{read,write}_safe true for Sphinx's -j. #376

- 2017-10-09 - Breathe v4.7.3

  - Support for enums in the cpp domain.
  - Handle case where compoundref does not have a refid value associated.

- 2017-08-15 - Breathe v4.7.2

  - Fix issue with packaging on Python 2.7 with wheels.

- 2017-08-13 - Breathe v4.7.1

  - Fixed bug regarding code snippets inside Doxygen comments.

- 2017-08-09 - Breathe v4.7.0

  - New `outtypes` option to prevent documenting namespace and files

  - New boolean `breathe_show_define_initializer` option specifying whether
    value of macros should be displayed.

  - New boolean `breathe_use_project_refids` option controlling whether the
    refids generated by breathe for doxygen elements contain the project name
    or not.

  - Fixed

    - Support for Sphinx 1.6

- 2017-02-25 - Breathe v4.6.0

  - Support for the Interface directive

  - Display the contents of defines

- 2017-02-12 - Breathe v4.5.0

  - Improve handling of c typedefs

  - Support new `desc_signature_line` node

  - Add `--project` flag to breathe-apidoc helper

  - Dropped testing for Python 3.3 and added 3.6

- 2016-11-13 - Breathe v4.4.0

  - Improve single line parameter documentation rendering

- 2016-11-05 - Breathe v4.3.1

  - Version bump package confusion with wheel release

- 2016-11-05 - Breathe v4.3.0

  - Rewritten rendering approach to use the visitor pattern

  - Dropped support for 2.6 & added testing for 3.5

  - Fixed

    - Issue with running breathe-apidoc for the first time.

    - Improved handling of qualifiers, eg. const & volatile.

    - Supports functions in structs

    - Supports auto-doxygen code path on Windows

- 2016-03-19 - Breathe v4.2.0

  - Added

    - Output links to a class' parents & children.

    - Support for Sphinx's `needs_extensions` config option.

    - breathe-apidoc script for generating ReStructuredText stub files with
      Breathe directives from doxygen xml files.

  - Fixed

    - Handling default values in parameter declarations

    - Output order not being reproducible due to iteration over Set.

    - Handling of multiple pointers and references

    - `SEVERE: Duplicate ID` warnings when using function overloads.

    - Use project name for link references when using default project. So we use
      the project name instead of 'project0'.

- 2015-08-27 - Breathe v4.1.0

  - Added

    - ``breathe_doxygen_config_options`` config variable which allows for adding
      more config lines to the doxygen file used for the auto-directives.

  - Fixed

    - Display of array & array reference parameters for functions.

    - Handling of links to classes with template arguments.

    - Handling of unnamed enums in C.

    - Naming of template parameter section.

    - Finding functions that are within groups.

    - Rendering of 'typename' and 'class' keywords for templates.

- 2015-04-02 - Breathe v4.0.0

  - Significant work on the code base with miminal reStructureText interface
    changes. To be documented.

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

