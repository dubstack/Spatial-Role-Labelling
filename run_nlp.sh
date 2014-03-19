#!/bin/bash
g++ convert_xml.cpp
./a.out input.txt input.xml
python tokenize.py
python postagger.py
jython parser.py
python prepositionfeatures.py
python spatialindicators.py
echo "DONE!"
exit


