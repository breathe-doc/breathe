Change Log
----------

Inspired by `Keepachangelog.com <https://keepachangelog.com/>`__.

- 2025-02-22 - **Breathe v4.36.0**

  - Update `test_renderer` so that tests pass with Sphinx 7.2.
    `#976 <https://github.com/breathe-doc/breathe/pull/976>`__
  - Fix PosixPath issue with Sphinx 7.2.
    `#964 <https://github.com/breathe-doc/breathe/pull/964>`__
  - Avoid `RemovedInSphinx80Warning` in path-manipulation code.
    `#977 <https://github.com/breathe-doc/breathe/pull/977>`__
  - Require Sphinx 7.2 or later, Python 3.9 or later,
     and  Doxygen 1.9.2 or later.
    `#887 <https://github.com/breathe-doc/breathe/pull/887>`__,
    `#946 <https://github.com/breathe-doc/breathe/pull/946>`__
    `#955 <https://github.com/breathe-doc/breathe/pull/955>`__
  - Begin to use pathlib.
  - Resolve full title for doxygenpage and doxygengroup
    and allow for omitting the title all together
    `#939 <https://github.com/breathe-doc/breathe/pull/939>`__
  - Insert signature name for use with Sphinx Table of Contents
    `#959 <https://github.com/breathe-doc/breathe/pull/959>`__
  - Fix test failure with latest Sphinx master.
    `#1010 <https://github.com/breathe-doc/breathe/pull/1010>`__
  - Fix error in template specialization with qualified arguments
    `#1010 <https://github.com/breathe-doc/breathe/pull/1012>`__

- 2023-02-28 - **Breathe v4.35.0**

  - Pull lone literal blocks in paragraphs up to produce correct doctree.
    `#833 <https://github.com/breathe-doc/breathe/pull/833>`__
  - Fix tests for changes in Sphinx 5.3.
    `#865 <https://github.com/breathe-doc/breathe/pull/865>`__
  - Bump Python requirement to 3.7.
    `#866 <https://github.com/breathe-doc/breathe/pull/866>`__
  - Support Sphinx 6.
    `#885 <https://github.com/breathe-doc/breathe/pull/885>`__
  - Support ``:sort:`` option to sort sections by name.
    `#879 <https://github.com/breathe-doc/breathe/pull/879>`__

- 2022-06-20 - **Breathe v4.34.0**

  - Treat .unparsed as plain text.
    `#806 <https://github.com/breathe-doc/breathe/pull/806>`__
  - Remove unneeded type: ignore annotations.
    `#813 <https://github.com/breathe-doc/breathe/pull/813>`__
  - Fix internal ``NodeFinder`` visitor for when non-Docutils nodes are
    present in the content of a directive.
    `#812 <https://github.com/breathe-doc/breathe/pull/812>`__
  - Rename lint workflow.
    `#814 <https://github.com/breathe-doc/breathe/pull/814>`__
  - Type check pygments and limit docutils stub version.
    `#819 <https://github.com/breathe-doc/breathe/pull/819>`__
  - Convert dot files' relative path to absolute.
    `#821 <https://github.com/breathe-doc/breathe/pull/821>`__
  - CI, update Sphinx versions to test.
    `#834 <https://github.com/breathe-doc/breathe/pull/834>`__
  - CI, update for Sphinx 5.0.1.
    `#846 <https://github.com/breathe-doc/breathe/pull/846>`__
  - Fix inconsistency in example.
    `#843 <https://github.com/breathe-doc/breathe/pull/843>`__
  - Fix C# enum rendering crash.
    `#849 <https://github.com/breathe-doc/breathe/pull/849>`__
  - Drop Sphinx 3 support, add Sphinx 5 support.
    `#850 <https://github.com/breathe-doc/breathe/pull/850>`__
  - CICD: Disable python 3.6 for Sphinx master tests.
    `#853 <https://github.com/breathe-doc/breathe/pull/853>`__
  - Populate default include text-node's data field instead of raw-source.
    `#828 <https://github.com/breathe-doc/breathe/pull/828>`__

- 2022-02-14 - **Breathe v4.33.1**

  - Avoid warning about multiple graphviz directives.
    `#804 <https://github.com/breathe-doc/breathe/pull/804>`__

- 2022-02-14 - **Breathe v4.33.0**

  - Fix duplicate ``static`` in variable declarations.
    `#794 <https://github.com/breathe-doc/breathe/pull/794>`__
  - Update CICD for Sphinx 4.4.0 series.
    `#795 <https://github.com/breathe-doc/breathe/pull/795>`__
  - Pin version of black in CICD and reformat files.
    `#792 <https://github.com/breathe-doc/breathe/pull/792>`__
  - Fix code block highlighting.
    `#760 <https://github.com/breathe-doc/breathe/pull/760>`__
  - Refactoring, cleanup and typing improvements.
    `#802 <https://github.com/breathe-doc/breathe/pull/802>`__
  - Doxygen dot graphs to Sphinx graphviz.
    `#757 <https://github.com/breathe-doc/breathe/pull/757>`__
  - Support externally hosted images.
    `#705 <https://github.com/breathe-doc/breathe/pull/705>`__
  - Address a peculiarity in Doxygen aliases in doc.
    `#770 <https://github.com/breathe-doc/breathe/pull/770>`__
  - Add flag to doxygengroup, doxygennamespace to display only the description.
    `#718 <https://github.com/breathe-doc/breathe/pull/718>`__
  - Add support for MD block quotes with attribution(s).
    `#759 <https://github.com/breathe-doc/breathe/pull/759>`__

- 2022-01-30 - **Breathe v4.32.0**

  - Added ``breathe_doxygen_aliases`` config variable.
    `#729 <https://github.com/breathe-doc/breathe/pull/729>`__
  - Render ``\remark``/``\remarks`` and ``\see``/``\sa`` using Sphinx/Docutils
    admonition style nodes.
    `#756 <https://github.com/breathe-doc/breathe/pull/756>`__
  - Render C++ scoped enums differently than unscoped enums, and with their
    underlying type.
    `#753 <https://github.com/breathe-doc/breathe/pull/753>`__
  - Render ``\retval`` lists using dedicated field list when Sphinx >= 4.3 is
    used.
    `#749 <https://github.com/breathe-doc/breathe/pull/749>`__
  - Make ``.. doxygenfunction`` handle function template specializations.
    `#750 <https://github.com/breathe-doc/breathe/pull/750>`__
  - Properly handle field-lists and admonitions in the detailed description of
    classes and functions.
    `#764 <https://github.com/breathe-doc/breathe/pull/764>`__
  - Add ``:confval:`breathe_show_include``` to control whether ``#include``
    lines are shown. Defaults to ``True``.
    `#725 <https://github.com/breathe-doc/breathe/pull/725>`__
  - Fix sys.path adjustment in doc config.
    `#734 <https://github.com/breathe-doc/breathe/pull/734>`__
  - Fix sphinx renderer variable and function visitors for C#.
    `#737 <https://github.com/breathe-doc/breathe/pull/737>`__
  - Fix sphinx renderer class visitor for C#.
    `#738 <https://github.com/breathe-doc/breathe/pull/738>`__
  - Auto-format python code with black.
    `#743 <https://github.com/breathe-doc/breathe/pull/743>`__
  - Extend flake8 and address some style issues.
    `#745 <https://github.com/breathe-doc/breathe/pull/745>`__
  - Fix black formatting warning.
    `#747 <https://github.com/breathe-doc/breathe/pull/747>`__
  - Update Sphinx and Python versions tested against.
    `#765 <https://github.com/breathe-doc/breathe/pull/765>`__
  - Fix friend functions for older Doxygen versions.
    `#769 <https://github.com/breathe-doc/breathe/pull/769>`__
  - Doxygen >= 1.9.2 supports C++20 concepts, add support for them.
    `#779 <https://github.com/breathe-doc/breathe/pull/779>`__
  - Change the way directives are added to adhere to the interface,
    e.g., avoiding myst-parser to crash.
    `#780 <https://github.com/breathe-doc/breathe/pull/780>`__
  - Improved list of included files (with cross-references for local includes).
    `#763 <https://github.com/breathe-doc/breathe/pull/763>`__
  - Update flake8 and mypy related stuff.
    `#781 <https://github.com/breathe-doc/breathe/pull/781>`__
  - Update readme with logo and sponsorship info.
    `#784 <https://github.com/breathe-doc/breathe/pull/784>`__
  - Store version number in both setup.py and __init__.py.
    `#789 <https://github.com/breathe-doc/breathe/pull/789>`__
  - CICD: lint: continue with other jobs if black fails.
    `#791 <https://github.com/breathe-doc/breathe/pull/791>`__

- 2021-09-14 - **Breathe v4.31.0**

  - Collapse multiple retvals into a single bullet list. `#697 <https://github.com/breathe-doc/breathe/pull/697>`__
  - Fix mypy issues on CI. `#731 <https://github.com/breathe-doc/breathe/pull/731>`__
  - Print usage message from 'compare' doc script. `#727 <https://github.com/breathe-doc/breathe/pull/727>`__
  - Test against Sphinx 4.0.3, 4.1.2 and 4.1.x branch. `#721 <https://github.com/breathe-doc/breathe/pull/721>`__
  - Fix duplicate ``static`` in function declarations. `#717 <https://github.com/breathe-doc/breathe/issues/717>`__ `#720 <https://github.com/breathe-doc/breathe/pull/720>`__
  - Directive refactoring. `#698 <https://github.com/breathe-doc/breathe/pull/698>`__
  - Handle parsing errors. `#711 <https://github.com/breathe-doc/breathe/pull/711>`__
  - Make doxygenfunction more robust when matching parameters. `#722 <https://github.com/breathe-doc/breathe/issues/722>`__ `#723 <https://github.com/breathe-doc/breathe/pull/723>`__
  - Separate, link and style the changelog. `#735 <https://github.com/breathe-doc/breathe/pull/735>`__
  - Update changelog and readme ahead of release. `#739 <https://github.com/breathe-doc/breathe/pull/739>`__
  - CICD: Track Sphinx 4.2.x development series. `#741 <https://github.com/breathe-doc/breathe/pull/741>`__

- 2021-05-06 - **Breathe v4.30.0**

  - Fix retval rendering. `#687 <https://github.com/breathe-doc/breathe/pull/687>`__
  - Correctly label example as C. `#690 <https://github.com/breathe-doc/breathe/pull/690>`__
  - apidoc: add -m, --members option flag. `#694 <https://github.com/breathe-doc/breathe/pull/694>`__

- 2021-04-30 - **Breathe v4.29.2**

  - Remove stale six dep. `#682 <https://github.com/breathe-doc/breathe/pull/682>`__
  - Render fields with multiple names instead of crashing. `#685 <https://github.com/breathe-doc/breathe/pull/685>`__
  - Start pytest via module instead of exe. `#686 <https://github.com/breathe-doc/breathe/pull/686>`__

- 2021-04-23 - **Breathe v4.29.1**

  - Splice out parameter direction in field lists. `#675 <https://github.com/breathe-doc/breathe/pull/675>`__
  - Fixes for Sphinx v4. `#676 <https://github.com/breathe-doc/breathe/pull/676>`__
  - Fix paragraph in paragraph rendering. `#678 <https://github.com/breathe-doc/breathe/pull/678>`__
  - Strip names before lookup in doxygenfunction. `#679 <https://github.com/breathe-doc/breathe/pull/679>`__
  - When rendering template params, insert name by parsing. `#681 <https://github.com/breathe-doc/breathe/pull/681>`__

- 2021-04-09 - **Breathe v4.29.0**

  - Do not add inline modifier for C#. `#668 <https://github.com/breathe-doc/breathe/pull/668>`__
  - Use add_css_file instead of deprecated/removed add_stylesheet. `#669 <https://github.com/breathe-doc/breathe/pull/669>`__
  - Use native docutils for field lists, notes, and warnings. `#670 <https://github.com/breathe-doc/breathe/pull/670>`__
  - Handle directives returning no nodes on error. `#672 <https://github.com/breathe-doc/breathe/pull/672>`__

- 2021-03-29 - **Breathe v4.28.0**

  - Code and documentation for membergroups and members-only options. `#637 <https://github.com/breathe-doc/breathe/pull/637>`__
  - Add example.tag to gitignore as it gets modified during build process. `#644 <https://github.com/breathe-doc/breathe/pull/644>`__
  - Add support for content-only flag when rendering pages. `#645 <https://github.com/breathe-doc/breathe/pull/645>`__
  - When rendering a section, add target after title. `#647 <https://github.com/breathe-doc/breathe/pull/647>`__
  - Render pages content in order. `#651 <https://github.com/breathe-doc/breathe/pull/651>`__
  - Adds an ID to the rubric created for each section of a group. `#658 <https://github.com/breathe-doc/breathe/pull/658>`__
  - Add missing getter and setter for C#. `#661 <https://github.com/breathe-doc/breathe/pull/661>`__
  - Add support for rowspan/colspan to tables. `#642 <https://github.com/breathe-doc/breathe/pull/642>`__

- 2021-02-16 - **Breathe v4.27.0**

  - Add various specifiers to functions and variables. `#628 <https://github.com/breathe-doc/breathe/pull/628>`__
  - Add multiply inherited class for PHP objects. `#630 <https://github.com/breathe-doc/breathe/pull/630>`__
  - Initial support for table rendering. `#632 <https://github.com/breathe-doc/breathe/pull/632>`__
  - Add rendering of \section, \subsection and \subsubsection. `#635 <https://github.com/breathe-doc/breathe/pull/635>`__
  - Sphinx 3.5 compatibility. `#640 <https://github.com/breathe-doc/breathe/pull/640>`__
  - Fix linking to sections. `#639 <https://github.com/breathe-doc/breathe/pull/639>`__
  - Add table examples to documentation. `#638 <https://github.com/breathe-doc/breathe/pull/638>`__

- 2021-01-21 - **Breathe v4.26.1**

  - Fix doxygenfile causing duplicate IDs for unspecified sections. `#622 <https://github.com/breathe-doc/breathe/pull/622>`__
  - Fixes for doxygenfunction (friend keyword, friend class, arg checks). `#623 <https://github.com/breathe-doc/breathe/pull/623>`__

- 2021-01-08 - **Breathe v4.26.0**

  - Add test for ellipsis ('...') in args. `#610 <https://github.com/breathe-doc/breathe/pull/610>`__
  - Sphinx 3.4.x compatibility. `#617 <https://github.com/breathe-doc/breathe/pull/617>`__
  - Adapt friendclass to Doxygen 1.9. `#618 <https://github.com/breathe-doc/breathe/pull/618>`__

- 2020-12-16 - **Breathe v4.25.1**

  - Addendum to #606, for functions with '...'. `#609 <https://github.com/breathe-doc/breathe/pull/609>`__

- 2020-12-15 - **Breathe v4.25.0**

  - Add support for \parblock parsing and rendering. `#603 <https://github.com/breathe-doc/breathe/pull/603>`__
  - Allow lookup in doxygenfunction without writing param names. `#606 <https://github.com/breathe-doc/breathe/pull/606>`__

- 2020-12-01 - **Breathe v4.24.1**

  - Fix anchors on pages generated by Doxygen >= 1.8.17. `#602 <https://github.com/breathe-doc/breathe/pull/602>`__

- 2020-11-15 - **Breathe v4.24.0**

  - Update CI for Sphinx 3.3.x and fix test mock. `#597 <https://github.com/breathe-doc/breathe/pull/597>`__
  - Add support for xrefitem based page generation (doxygenpage). `#596 <https://github.com/breathe-doc/breathe/pull/596>`__

- 2020-10-20 - **Breathe v4.23.0**

  - Add initial xrefsect support. `#589 <https://github.com/breathe-doc/breathe/pull/589>`__

- 2020-09-26 - **Breathe v4.22.1**

  - Fix anonymous struct/union usage in C domain. `#585 <https://github.com/breathe-doc/breathe/pull/585>`__

- 2020-09-19 - **Breathe v4.22.0**

  - Fix Read the Docs build (again). `#576 <https://github.com/breathe-doc/breathe/pull/576>`__
  - New boolean `breathe_show_enumvalue_initializer` option specifying
    whether value of enumvalue should be displayed. `#581 <https://github.com/breathe-doc/breathe/pull/581>`__

- 2020-09-10 - **Breathe v4.21.0**

  - Fix Read the Docs build. `#567 <https://github.com/breathe-doc/breathe/pull/567>`__
  - Document doxygenclass template specialisation spacing. `#570 <https://github.com/breathe-doc/breathe/pull/570>`__
  - Update upper Sphinx release to <3.4. `#571 <https://github.com/breathe-doc/breathe/pull/571>`__
  - Reuse breathe.__version__ in setup.py. `#572 <https://github.com/breathe-doc/breathe/pull/572>`__
  - Document :inner: for the doxygengroup section. `#573 <https://github.com/breathe-doc/breathe/pull/573>`__
  - Add support for verbatim inline elements. `#560 <https://github.com/breathe-doc/breathe/pull/560>`__
  - Fix wrong refid when Doxygen SEPARATE_MEMBER_PAGES is YES. `#566 <https://github.com/breathe-doc/breathe/pull/566>`__

- 2020-08-19 - **Breathe v4.20.0**

  - Allow Sphinx 3.2. `#561 <https://github.com/breathe-doc/breathe/pull/561>`__
  - Update CI scripts with new Sphinx versions. `#552 <https://github.com/breathe-doc/breathe/pull/552>`__
  - Add support for C# using sphinx-csharp. `#550 <https://github.com/breathe-doc/breathe/pull/550>`__
  - Doc, fix typo, :source: -> :project:. `#551 <https://github.com/breathe-doc/breathe/pull/551>`__
  - Add support for innergroup. `#556 <https://github.com/breathe-doc/breathe/pull/556>`__
  - Avoid duplicate doxygen targets when debug tracing. `#563 <https://github.com/breathe-doc/breathe/pull/563>`__
  - Remove Travis badge from README file. `#564 <https://github.com/breathe-doc/breathe/pull/564>`__

- 2020-06-17 - **Breathe v4.19.2**

  - Fix crash when visiting typedef. `#547 <https://github.com/breathe-doc/breathe/pull/547>`__

- 2020-06-08 - **Breathe v4.19.1**

  - Mark package as compatible with Sphinx 3.1.

- 2020-06-07 - **Breathe v4.19.0**

  - Refactoring. `#528 <https://github.com/breathe-doc/breathe/pull/528>`__
  - Make debug config variables available in conf.py. `#533 <https://github.com/breathe-doc/breathe/pull/533>`__
  - Fix warning formatting for function lookup. `#535 <https://github.com/breathe-doc/breathe/pull/535>`__
  - Correctly reverse nested namespaces in get_qualification. `#540 <https://github.com/breathe-doc/breathe/pull/540>`__

- 2020-05-10 - **Breathe v4.18.1**

  - Fix friend class rendering and allow friend struct. `#522 <https://github.com/breathe-doc/breathe/pull/522>`__
  - Add extern examples to doc and remove variable hack. `#526 <https://github.com/breathe-doc/breathe/pull/526>`__
  - Render function candidates without using Sphinx directives. `#524 <https://github.com/breathe-doc/breathe/pull/524>`__

- 2020-05-02 - **Breathe v4.18.0**

  - Support tiles in verbatim blocks. `#517 <https://github.com/breathe-doc/breathe/pull/517>`__

- 2020-05-01 - **Breathe v4.17.0**

  - Scoped rendering, better integration with Sphinx, misc fixes. `#512 <https://github.com/breathe-doc/breathe/pull/512>`__

- 2020-04-19 - **Breathe v4.16.0**

  - Strictly depend on Sphinx's minor version. `#498 <https://github.com/breathe-doc/breathe/pull/498>`__
  - Simplifications and fixes, use more of modern Sphinx natively. `#503 <https://github.com/breathe-doc/breathe/pull/503>`__
  - Add section option to the doxygen(auto)file directive. `#501 <https://github.com/breathe-doc/breathe/pull/501>`__
  - Fix link generation when enum is inside a group (enum FQDN). `#508 <https://github.com/breathe-doc/breathe/pull/508>`__
  - Fix creation of LaTeX math formulas. `#506 <https://github.com/breathe-doc/breathe/pull/506>`__
  - Improve documentation for doxygen(auto)file section option. `#509 <https://github.com/breathe-doc/breathe/pull/509>`__

- 2020-04-07 - **Breathe v4.15.0**

  - Add license file to distribution. `#492 <https://github.com/breathe-doc/breathe/pull/492>`__
  - Update for Sphinx 3. `#491 <https://github.com/breathe-doc/breathe/pull/491>`__

- 2020-04-07 - **Breathe v4.14.2**

  - Add GitHub actions. `#474 <https://github.com/breathe-doc/breathe/pull/474>`__
  - Fixes to use Sphinx 2.4.4. `#486 <https://github.com/breathe-doc/breathe/pull/486>`__
  - Add nose to python development requirements. #484.
  - Switch to pytest from nose. `#487 <https://github.com/breathe-doc/breathe/pull/487>`__

- 2020-02-02 - **Breathe v4.14.1**

  - Use sphinx core instead of mathbase ext. `#469 <https://github.com/breathe-doc/breathe/pull/469>`__
  - Fix test failure for Sphinx >= 2.2.2. `#472 <https://github.com/breathe-doc/breathe/pull/472>`__
  - Update travis to Sphinx 2.3.1. `#471 <https://github.com/breathe-doc/breathe/pull/471>`__

- 2019-11-26 - **Breathe v4.14.0**

  - Add events attribute to MockApp. `#452 <https://github.com/breathe-doc/breathe/pull/452>`__
  - Add bit field support for C/C++. `#454 <https://github.com/breathe-doc/breathe/pull/454>`__
  - Add alias and variable template support. `#461 <https://github.com/breathe-doc/breathe/pull/461>`__

- 2019-08-01 - **Breathe v4.13.1**

  - Fix for template method pointer parameter issue. `#449 <https://github.com/breathe-doc/breathe/pull/449>`__

- 2019-04-23 - **Breathe v4.13.0**.post0

  - Drop support for python 2, require Sphinx >= 2.0. `#432 <https://github.com/breathe-doc/breathe/pull/432>`__

- 2019-04-21 - **Breathe v4.13.0**

  - Adapt to upcoming Sphinx 2.0. `#411 <https://github.com/breathe-doc/breathe/pull/411>`__
  - Add support for rendering parameter direction information. `#428 <https://github.com/breathe-doc/breathe/pull/428>`__

- 2019-03-15 - **Breathe v4.12.0**

  - Adapt to Sphinx 1.8. `#410 <https://github.com/breathe-doc/breathe/pull/410>`__
  - Let Sphinx handle more things. `#412 <https://github.com/breathe-doc/breathe/pull/412>`__
  - Use standard windows EOL for batch file. `#417 <https://github.com/breathe-doc/breathe/pull/417>`__
  - Fix flake8 F632 warnings. `#418 <https://github.com/breathe-doc/breathe/pull/418>`__
  - Update dep versions in readme, setup, requirements. `#419 <https://github.com/breathe-doc/breathe/pull/419>`__
  - Add option to render function parameters after the description. `#421 <https://github.com/breathe-doc/breathe/pull/421>`__
  - Remove spurious "typedef" in type declaration when using "using". `#424 <https://github.com/breathe-doc/breathe/pull/424>`__

- 2018-12-11 - **Breathe v4.11.1**

  - Sphinxrenderer: handle typeless parameters gracefully. `#404 <https://github.com/breathe-doc/breathe/pull/404>`__

- 2018-10-31 - **Breathe v4.11.0**

  - Fix typo in quickstart. `#393 <https://github.com/breathe-doc/breathe/pull/393>`__
  - Add support for QtSignals. `#401 <https://github.com/breathe-doc/breathe/pull/401>`__

- 2018-08-07 - **Breathe v4.10.0**

  - Explicitly use Sphinx 1.7.5 for CI and dev. `#385 <https://github.com/breathe-doc/breathe/pull/385>`__
  - Print filename when printing ParserException. `#390 <https://github.com/breathe-doc/breathe/pull/390>`__

- 2018-06-03 - **Breathe v4.9.1**

  - Don't append separator for paragraph type. `#382 <https://github.com/breathe-doc/breathe/pull/382>`__

- 2018-06-01 - **Breathe v4.9.0**

  - Render newlines as separate paragraphs. `#380 <https://github.com/breathe-doc/breathe/pull/380>`__

- 2018-05-26 - **Breathe v4.8.0**

  - Add quiet option to apidoc. `#375 <https://github.com/breathe-doc/breathe/pull/375>`__
  - Add PHP domain. `#351 <https://github.com/breathe-doc/breathe/pull/351>`__
  - Keep templates on adjacent lines. `#300 <https://github.com/breathe-doc/breathe/pull/300>`__
  - Show reference qualification for methods. `#332 <https://github.com/breathe-doc/breathe/pull/332>`__
  - Adapt tests/CI to newest Sphinx version. `#377 <https://github.com/breathe-doc/breathe/pull/377>`__
  - More robust name regex in renderer. `#370 <https://github.com/breathe-doc/breathe/pull/370>`__
  - Show base classes using Sphinx's cpp domain. `#295 <https://github.com/breathe-doc/breathe/pull/295>`__
  - Fix domain detection when rendering groups. `#365 <https://github.com/breathe-doc/breathe/pull/365>`__
  - Return parallel_{read,write}_safe true for Sphinx's -j. `#376 <https://github.com/breathe-doc/breathe/pull/376>`__

- 2017-10-09 - **Breathe v4.7.3**

  - Support for enums in the cpp domain.
  - Handle case where compoundref does not have a refid value associated.

- 2017-08-15 - **Breathe v4.7.2**

  - Fix issue with packaging on Python 2.7 with wheels.

- 2017-08-13 - **Breathe v4.7.1**

  - Fixed bug regarding code snippets inside Doxygen comments.

- 2017-08-09 - **Breathe v4.7.0**

  - New `outtypes` option to prevent documenting namespace and files

  - New boolean `breathe_show_define_initializer` option specifying whether
    value of macros should be displayed.

  - New boolean `breathe_use_project_refids` option controlling whether the
    refids generated by breathe for doxygen elements contain the project name
    or not.

  - Fixed

    - Support for Sphinx 1.6

- 2017-02-25 - **Breathe v4.6.0**

  - Support for the Interface directive

  - Display the contents of defines

- 2017-02-12 - **Breathe v4.5.0**

  - Improve handling of c typedefs

  - Support new `desc_signature_line` node

  - Add `--project` flag to breathe-apidoc helper

  - Dropped testing for Python 3.3 and added 3.6

- 2016-11-13 - **Breathe v4.4.0**

  - Improve single line parameter documentation rendering

- 2016-11-05 - **Breathe v4.3.1**

  - Version bump package confusion with wheel release

- 2016-11-05 - **Breathe v4.3.0**

  - Rewritten rendering approach to use the visitor pattern

  - Dropped support for 2.6 & added testing for 3.5

  - Fixed

    - Issue with running breathe-apidoc for the first time.

    - Improved handling of qualifiers, eg. const & volatile.

    - Supports functions in structs

    - Supports auto-doxygen code path on Windows

- 2016-03-19 - **Breathe v4.2.0**

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

- 2015-08-27 - **Breathe v4.1.0**

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

- 2015-04-02 - **Breathe v4.0.0**

  - Significant work on the code base with miminal reStructureText interface
    changes. To be documented.

- 2014-11-09 - **Breathe v3.2.0**

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

- 2014-09-07 - **Breathe v3.1.0**

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

- 2014-08-04 - **Breathe v3.0.0**

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

- 2014-06-15 - **Breathe v2.0.0**

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

- 2014-06-01 - **Breathe v1.2.0**

  - Change log not recorded.

