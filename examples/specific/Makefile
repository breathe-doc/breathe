#
# This file was generated from Makefile.in on Sat Dec 13 12:17:28 GMT 2008
#

DOXYGEN   = `which doxygen`
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

all: typedef/xml/index.xml \
	class/xml/index.xml \
	nutshell/xml/index.xml \
	alias/xml/index.xml \
	rst/xml/index.xml \
	inline/xml/index.xml \
	members/xml/index.xml \
	c_file/xml/index.xml \
	namespacefile/xml/index.xml \
	multifilexml/xml/index.xml \
	template_class/xml/index.xml \
	template_class_non_type/xml/index.xml \
	template_function/xml/index.xml \
	userdefined/xml/index.xml \
	fixedwidthfont/xml/index.xml \
	latexmath/xml/index.xml \
	functionOverload/xml/index.xml \
	programlisting/xml/index.xml \
	image/xml/index.xml
	

clean:
	rm -rf typedef class nutshell alias rst inline namespacefile c_file \
		members multifilexml userdefined fixedwidthfont latexmath functionOverload \
		programlisting image
           
typedef/xml/index.xml: typedef.h typedef.cfg
	$(DOXYGEN) typedef.cfg

class/xml/index.xml: class.h class.cfg
	$(DOXYGEN) class.cfg

nutshell/xml/index.xml: nutshell.h nutshell.cfg
	$(DOXYGEN) nutshell.cfg

alias/xml/index.xml: alias.h alias.cfg
	$(DOXYGEN) alias.cfg

rst/xml/index.xml: rst.h rst.cfg
	$(DOXYGEN) rst.cfg

inline/xml/index.xml: inline.h inline.cfg
	$(DOXYGEN) inline.cfg

members/xml/index.xml: members.h members.cfg
	$(DOXYGEN) members.cfg

c_file/xml/index.xml: c_file.h c_file.cfg
	$(DOXYGEN) c_file.cfg

namespacefile/xml/index.xml: namespacefile.h namespacefile.cfg
	$(DOXYGEN) namespacefile.cfg
	
multifilexml/xml/index.xml: multifile/one/Util.h multifile/two/Util.h multifile.cfg
	$(DOXYGEN) multifile.cfg

template_class/xml/index.xml: template_class.h template_class.cfg
	$(DOXYGEN) template_class.cfg

template_class_non_type/xml/index.xml: template_class_non_type.h template_class_non_type.cfg
	$(DOXYGEN) template_class_non_type.cfg

template_function/xml/index.xml: template_function.h template_function.cfg
	$(DOXYGEN) template_function.cfg

userdefined/xml/index.xml: userdefined.h userdefined.cfg
	$(DOXYGEN) userdefined.cfg

fixedwidthfont/xml/index.xml: fixedwidthfont.h fixedwidthfont.cfg
	$(DOXYGEN) fixedwidthfont.cfg

latexmath/xml/index.xml: latexmath.h latexmath.cfg
	$(DOXYGEN) latexmath.cfg

functionOverload/xml/index.xml: functionOverload.h functionOverload.cfg
	$(DOXYGEN) functionOverload.cfg

programlisting/xml/index.xml: programlisting.h programlisting.cfg programlistinginclude.txt
	$(DOXYGEN) programlisting.cfg

image/xml/index.xml: image.h image.cfg
	$(DOXYGEN) image.cfg
