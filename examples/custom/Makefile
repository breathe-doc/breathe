#
# This file was generated from Makefile.in on Sat Dec 13 12:17:28 GMT 2008
#

DOXYGEN   = /user_data/RND/git/vendor/doxygen/doxygen-1.5.8
TMAKEPATH = /user_data/RND/git/vendor/doxygen/doxygen/doxygen/tmake/lib/linux-g++
ENV       = env TMAKEPATH=$(TMAKEPATH)
TMAKE     = /user_data/RND/git/vendor/doxygen/doxygen-1.5.8/tmake/bin/tmake
MAKE      = /usr/bin/make
PERL      = /usr/bin/perl
RM        = rm -f
CP        = cp
VERSION   = 1.5.7.1
INSTALL   = /tmp
INSTTOOL  = /usr/bin/install
DOXYDOCS  = ..
DOCDIR    = $(INSTALL)/share/doc/packages/doxygen
QTDIR     = 
HAVE_DOT  = /usr/bin/dot

all: tinyxml/xml/index.xml

clean:
	rm -rf  class define enum file func page relates author \
                par overload example include qtstyle jdstyle structcmd \
		autolink tag restypedef afterdoc template tag group diagrams \
		memgrp docstring pyexample mux manual

tinyxml/xml/index.xml: tinyxml.h tinyxml.cfg
	$(DOXYGEN)/bin/doxygen tinyxml.cfg

