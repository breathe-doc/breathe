#!/bin/bash

directory=`pwd`

# Make all the examples in the doxygen directory
cd ../examples/doxygen
make 

# Create links to examples of the .xsd files 
# (It doesn't matter which ones they are all the same)
cd $directory

if [ ! -e index.xsd ]
then
	ln -s ../examples/doxygen/class/xml/index.xsd .
fi

if [ ! -e compound.xsd ]
then
	ln -s ../examples/doxygen/class/xml/compound.xsd .
fi

if [ ! -e generateDS.py ]
then
	echo "Error - Cannot find generateDS.py in this directory."
	echo "        Please get it from:"
	echo "        http://www.rexx.com/~dkuhlman/generateDS.html#download"
	exit
fi

python generateDS.py --no-process-includes -o indexsuper.py -a "xsd:" index.xsd

python generateDS.py --no-process-includes -o compoundsuper.py -a "xsd:" compound.xsd

