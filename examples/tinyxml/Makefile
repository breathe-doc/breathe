#
# This file was generated from Makefile.in on Sat Dec 13 12:17:28 GMT 2008
#

DOXYGEN   ?= `which doxygen`
TMAKEPATH = 
ENV       = env TMAKEPATH=$(TMAKEPATH)
TMAKE     = 
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
	rm -rf tinyxml

tinyxml/xml/index.xml: tinyxml.h tinyxml.cfg
	$(DOXYGEN) tinyxml.cfg

