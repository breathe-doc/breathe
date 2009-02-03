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

all: class/xml/index.xml \
     define/xml/index.xml \
     enum/xml/index.xml \
     file/xml/index.xml \
     func/xml/index.xml \
     page/xml/index.xml \
     relates/xml/index.xml \
     author/xml/index.xml \
     par/xml/index.xml \
     overload/xml/index.xml \
     example/xml/index.xml \
     include/xml/index.xml \
     qtstyle/xml/index.xml \
     jdstyle/xml/index.xml \
     structcmd/xml/index.xml \
     autolink/xml/index.xml \
     restypedef/xml/index.xml \
     afterdoc/xml/index.xml \
     template/xml/index.xml \
     tag/xml/index.xml \
     group/xml/index.xml \
     diagrams/xml/index.xml \
     memgrp/xml/index.xml \
     docstring/xml/index.xml \
     pyexample/xml/index.xml \
     mux/xml/index.xml \
     manual/xml/index.xml

clean:
	rm -rf  class define enum file func page relates author \
                par overload example include qtstyle jdstyle structcmd \
		autolink tag restypedef afterdoc template tag group diagrams \
		memgrp docstring pyexample mux manual

class/xml/index.xml: class.h class.cfg
	$(DOXYGEN)/bin/doxygen class.cfg

define/xml/index.xml: define.h define.cfg
	$(DOXYGEN)/bin/doxygen define.cfg

enum/xml/index.xml: enum.h enum.cfg
	$(DOXYGEN)/bin/doxygen enum.cfg

file/xml/index.xml: file.h file.cfg
	$(DOXYGEN)/bin/doxygen file.cfg

func/xml/index.xml: func.h func.cfg
	$(DOXYGEN)/bin/doxygen func.cfg

page/xml/index.xml: page.doc page.cfg
	$(DOXYGEN)/bin/doxygen page.cfg

relates/xml/index.xml: relates.cpp relates.cfg
	$(DOXYGEN)/bin/doxygen relates.cfg

author/xml/index.xml: author.cpp author.cfg
	$(DOXYGEN)/bin/doxygen author.cfg

par/xml/index.xml: par.cpp par.cfg
	$(DOXYGEN)/bin/doxygen par.cfg

overload/xml/index.xml: overload.cpp overload.cfg
	$(DOXYGEN)/bin/doxygen overload.cfg

example/xml/index.xml: example.cpp example_test.cpp example.cfg 
	$(DOXYGEN)/bin/doxygen example.cfg

include/xml/index.xml: include.cpp example_test.cpp include.cfg 
	$(DOXYGEN)/bin/doxygen include.cfg

qtstyle/xml/index.xml: qtstyle.cpp qtstyle.cfg 
	$(DOXYGEN)/bin/doxygen qtstyle.cfg

jdstyle/xml/index.xml: jdstyle.cpp jdstyle.cfg 
	$(DOXYGEN)/bin/doxygen jdstyle.cfg

structcmd/xml/index.xml: structcmd.h structcmd.cfg 
	$(DOXYGEN)/bin/doxygen structcmd.cfg

autolink/xml/index.xml: autolink.cpp autolink.cfg 
	$(DOXYGEN)/bin/doxygen autolink.cfg

tag/xml/index.xml: tag.cpp tag.cfg example/xml/index.xml
	$(DOXYGEN)/bin/doxygen tag.cfg
#	sed -e "1,1s#perl#$(PERL)#g" tag/xml/installdox >tag/xml/installdox.perl
#	cd tag/xml ; $(PERL) installdox.perl -lexample.tag@../../example/xml

restypedef/xml/index.xml: restypedef.cpp restypedef.cfg 
	$(DOXYGEN)/bin/doxygen restypedef.cfg

afterdoc/xml/index.xml: afterdoc.h afterdoc.cfg
	$(DOXYGEN)/bin/doxygen afterdoc.cfg

template/xml/index.xml: templ.cpp templ.cfg
	$(DOXYGEN)/bin/doxygen templ.cfg

group/xml/index.xml: group.cpp group.cfg
	$(DOXYGEN)/bin/doxygen group.cfg

memgrp/xml/index.xml: memgrp.cpp memgrp.cfg
	$(DOXYGEN)/bin/doxygen memgrp.cfg

pyexample/xml/index.xml: pyexample.py pyexample.cfg
	$(DOXYGEN)/bin/doxygen pyexample.cfg

mux/xml/index.xml: mux.vhdl mux.cfg
	$(DOXYGEN)/bin/doxygen mux.cfg

manual/xml/index.xml: manual.c manual.cfg
	$(DOXYGEN)/bin/doxygen manual.cfg

docstring/xml/index.xml: docstring.py docstring.cfg
	$(DOXYGEN)/bin/doxygen docstring.cfg

diagrams/xml/index.xml: diagrams_a.h diagrams_b.h diagrams_c.h diagrams_d.h diagrams_e.h diagrams.cfg
ifneq ($(HAVE_DOT),)
	$(DOXYGEN)/bin/doxygen diagrams.cfg
endif

