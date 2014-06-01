
Running on Read the Docs
=========================

`Read the Docs`_ is an excellent site for hosting project documentation. It
provides hooks into common project hosting sites like Github_ & Bitbucket_ and can
rebuild your documentation automatically whenever you push new code.

The site is designed for documentation written with Sphinx and supports Sphinx
extensions via a correctly configured ``setup.py`` file.

As Breathe is a Sphinx extension you can use it on Read the Docs. However, as
Breathe requires doxygen XML files, some additional configuration is required.

Doxygen Support
---------------

Read the Docs do not explicitly support doxygen however they have had
requests for it to be supported and it is currently installed on their build
servers.

Generating Doxygen XML Files
----------------------------

We assume that you are not checking your doxygen XML files into your source
control system and so you will need to generate them on the Read the Docs
server before Sphinx starts processing your documentation.

One simple way of achieving this is to add the following code to your
``conf.py`` file:

.. code-block:: python

   import subprocess, os

   read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'

   if read_the_docs_build:

       subprocess.call('cd ../doxygen; doxygen', shell=True)

The first line uses the ``READTHEDOCS`` environment variable to determine
whether or not we are building on the Read the Docs servers. Read the Docs
set this environment variable `specifically for this purpose`_.

Then, if we are in a Read the Docs build, execute a simple shell command to
build the doxygen xml for your project. This is a very simple example; the
command will be determined by your project set up but something like this works
for the Breathe documentation.

As this is then executed right at the start of the ``sphinx-build`` process then
all your doxygen XML files will be in place for the build.

A More Involved Setup
---------------------

If you'd rather do something more involved then you can run ``doxygen`` as part
of a ``builder-inited`` event hook which you can install from your ``conf.py``
file by adding a ``setup`` function as shown below.

This is an approximation of the code that Breathe has in its ``conf.py`` in
order to run ``doxygen`` on the Read the Docs server.

.. code-block:: python

   import subprocess, sys

   def run_doxygen(folder):
       """Run the doxygen make command in the designated folder"""

       try:
           retcode = subprocess.call("cd %s; make" % folder, shell=True)
           if retcode < 0:
               sys.stderr.write("doxygen terminated by signal %s" % (-retcode))
       except OSError as e:
           sys.stderr.write("doxygen execution failed: %s" % e)


   def generate_doxygen_xml(app):
       """Run the doxygen make commands if we're on the ReadTheDocs server"""

       read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'

       if read_the_docs_build:

           run_doxygen("../../examples/doxygen")
           run_doxygen("../../examples/specific")
           run_doxygen("../../examples/tinyxml")


   def setup(app):

       # Add hook for building doxygen xml when needed
       app.connect("builder-inited", generate_doxygen_xml)

.. _Read the Docs: https://readthedocs.org/
.. _Github: https://github.com
.. _Bitbucket: https://bitbucket.org
.. _specifically for this purpose: https://docs.readthedocs.org/en/latest/faq.html#how-do-i-change-behavior-for-read-the-docs


