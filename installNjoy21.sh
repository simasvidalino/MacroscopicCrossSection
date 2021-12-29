#!/bin/bash
sudo apt-get install gfortran
sudo apt-get install python3
sudo apt-get install gcc
sudo apt-get install cmake
git clone https://github.com/njoy/NJOY21.git
wget https://raw.githubusercontent.com/njoy/signatures/master/NJOY21/1.1.0-NJOY21.json
cd NJOY21
./metaconfigure/fetch_subprojects.py ../1.1.0-NJOY21.json
mkdir bin
cd bin
cmake -D fetched_subprojects=true ../
make
make test