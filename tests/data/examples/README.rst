tests/data/examples
============================

Each direct child folder of "tests/data/examples", that starts with "test\_",
contains a test. The tests are read and run by "tests/test_examples.py" when
run by pytest.

Each test works by first creating an input file for Doxygen based on the
template "tests/data/examples/doxyfile_template", in a temporary folder. If a
file named "extra_dox_opts.txt" exists in the test folder, its contents are
appended to the input file. Doxygen is run with the current directory set to the
test folder, thus any source code files are automatically read by Doxygen. The
output is stored in the temporary folder. Sphinx is run on "input.rst" with the
following options:

.. code-block:: python

    project = "test"
    breathe_default_project = "example"
    breathe_show_include = False
    extensions = ["breathe", "sphinx.ext.graphviz"]
    breathe_projects = {"example": SOME_TEMPORARY_FOLDER}

plus any options specified by "extra_conf.py", if such a file exists in the test
folder. The output format is set to XML. The test folder contains "compare.xml"
and may contain one or more "compare-{version}.xml" files, where ``{version}``
is a dotted version number. The version number is compared to the version of
Doxygen being used. The file with the greatest version number that is not
greater than the version of Doxygen, is used, or "compare.xml" is used if no
such file exists. The output of Sphinx and the "compare" file are compared as a
series of start tags, end tags and text nodes. Other kinds of content are
ignored. The contents of the files must match, except the output can have
attributes that do not appear in the "compare" file, as long as every attribute
that is in the "compare" file is also in the output (the order of the attributes
does not matter); and the text nodes have all leading and trailing whitespace
stripped before being compared.

Certain attributes in Sphinx's XML output are either irrelevant or are dependant
on unimportant factors, such as the location of the input file or the version of
docutils. Thus, the "compare" files are always stripped of the following
attributes:

- ``ids``
- ``names``
- ``no-contents-entry``
- ``no-index``
- ``no-index-entry``
- ``no-typesetting``
- ``nocontentsentry``
- ``noindex``
- ``noindexentry``
- ``is_multiline``
- ``multi_line_parameter_list``
- ``add_permalink``
- ``xml:space``
- ``source``
- ``translation_progress``
- ``options``
- ``original_uri``
- ``_toc_name``
- ``_toc_parts``
- ``xmlns:c``
- ``xmlns:changeset``
- ``xmlns:citation``
- ``xmlns:cpp``
- ``xmlns:index``
- ``xmlns:js``
- ``xmlns:math``
- ``xmlns:py``
- ``xmlns:rst``
- ``xmlns:std``

Writing the "compare" files by hand is tedious and error-prone. It is far easier
to simply run Sphinx, check that it is correct (if it's not, fix the problem and
run it again) and take out the unneeded attributes. To this end: the script
"scripts/generate_test_results.py" exists. When run, for each test, it checks if
"compare.xml" exists. If it doesn't, it creates "compare_draft.xml", by running
Sphinx, taking the XML output and stripping the unneeded attributes.

Checking that the generated "compare_draft.xml" is correct is also tedious, thus
it includes a link to a style sheet ("tests/data/docutils.css"). This allows the
file to be opened in a browser (I have only tested Firefox and Chrome) and is
made much more readable.