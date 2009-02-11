#!/bin/bash

directory=`pwd`

cd ../examples/doxygen

make 

cd $directory

ln -s ../examples/doxygen/class/xml/index.xsd .
ln -s ../examples/doxygen/class/xml/compound.xsd .

python generateDS.py --no-process-includes -o indexsuper.py -a "xsd:" index.xsd

python generateDS.py --no-process-includes -o compoundsuper.py -a "xsd:" compound.xsd

