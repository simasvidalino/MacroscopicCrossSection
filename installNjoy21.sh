#!/bin/bash
sudo apt install gfortran
sudo apt install python3
sudo apt install gcc
sudo apt install cmake
git clone --branch v1.2.1 https://github.com/njoy/NJOY21.git
cd NJOY21
mkdir bin
cd bin
cmake -D CMAKE_BUILD_TYPE=Release ..
make
make test