
.. _file-example:

doxygenfile Directive
=====================

This directive generates the appropriate output for a single source file. It
takes the standard ``project``, ``path``, ``outline`` and ``no-link`` options
and additionally the ``sections`` options.

For the standard option refer to the documentation on the main directives page.
The directive-specific options are documented below.

``sections``
   Limit the sections to render for the given source file to the given list.
   Many of the names come from Doxygen and Breathe internals and may not make
   sense from an external point of view. Nevertheless it is hoped this table is
   useful.

   .. csv-table:: Section types
      :header: "Type", "Description"

      "briefdescription", "Brief description"
      "dcop-func", "DCOP Function"
      "define", "Define"
      "derivedcompoundref", "Derived compound reference"
      "detaileddescription", "Detailed description"
      "enum", "Enumerator"
      "event", "Events"
      "friend", "Friend"
      "func", "Function"
      "innerclass", "**Must be given to show sections inside a class**"
      "innernamespace", "**Must be given to show sections inside a namespace**"
      "package-attrib", "Package attribute"
      "package-func", "Package function"
      "package-static-attrib", "Package static attribute"
      "package-static-func", "Package static function"
      "package-type", "Package type"
      "private-attrib", "Private attribute"
      "private-func", "Private function"
      "private-slot", "Private slot"
      "private-static-attrib", "Private static attribute"
      "private-static-func", "Private static function"
      "private-type", "Private type"
      "property", "Properties"
      "protected-attrib", "Protected attribute"
      "protected-func", "Protected function"
      "protected-slot", "Protected slot"
      "protected-static-attrib", "Protected static attribute"
      "protected-static-func", "Protected static function"
      "protected-type", "Protected type"
      "prototype", "Prototype"
      "public-attrib", "Public attribute"
      "public-func", "Public function"
      "public-slot", "Public slot"
      "public-static-attrib", "Public static attribute"
      "public-static-func", "Public static function"
      "public-type", "Public type"
      "related", "Related"
      "signal", "Signal"
      "typedef", "Type definition"
      "user-defined", "User defined"
      "var", "Variable"


Example
-------

.. cpp:namespace:: @ex_file_example

This should work:

.. code-block:: rst

   .. doxygenfile:: nutshell.h
      :project: nutshell

It produces this output:

----

.. doxygenfile:: nutshell.h
   :project: nutshell

Example with Selected and Ordered Sections
------------------------------------------

.. cpp:namespace:: @ex_file_section

The following will only show the **briefdescription** and **public-type**
sections, in that order:

.. code-block:: rst

   .. doxygenfile:: nutshell.h
      :project: nutshell
      :sections: briefdescription innerclass public-type

It produces this output:

----

.. doxygenfile:: nutshell.h
   :project: nutshell
   :sections: briefdescription innerclass public-type
   :no-link:

Example with Nested Namespaces
------------------------------

.. cpp:namespace:: @ex_file_namespace

This should work:

.. code-block:: rst

   .. doxygenfile:: namespacefile.h
      :project: namespace

It produces this output:

----

.. doxygenfile:: namespacefile.h
   :project: namespace


Example for Multiple Files
--------------------------

.. cpp:namespace:: @ex_file_multiple_files

When there are multiple files with the same name in the project, you need to be
more specific with the filename you provide. For example, in a project with the
following two files:

.. code-block:: text

   /some/long/project/path/parser/Util.h
   /some/long/project/path/finder/Util.h

You should specify:

.. code-block:: rst

   .. doxygenfile:: parser/Util.h

   .. doxygenfile:: finder/Util.h

To uniquely identify them.

Failing Example
---------------

.. cpp:namespace:: @ex_file_failing

This intentionally fails:

.. code-block:: rst

   .. doxygenfile:: made_up_file.h
      :project: nutshell

It produces the following warning message:

.. warning::
   Cannot find file "made_up_file.h" in doxygen xml output for project "nutshell" from directory: ../../examples/specific/nutshell/xml/
