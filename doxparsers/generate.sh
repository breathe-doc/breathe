#!/bin/bash

directory=`pwd`

cd ../examples/doxygen

make 

cd $directory

ln -s ../examples/doxygen/class/xml/index.xsd .
ln -s ../examples/doxygen/class/xml/compound.xsd .

python generateDS.py --no-process-includes -o indexsuper.py -s index.py -a "xsd:" index.xsd

sed -i 's/???/indexsuper/g' index.py

python generateDS.py --no-process-includes -o compoundsuper.py -s compound.py -a "xsd:" compound.xsd

sed -i 's/???/compoundsuper/g' compound.py

