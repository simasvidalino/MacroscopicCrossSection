#!/bin/bash
sudo dnf upgrade
sudo dnf install gfortran
sudo dnf install python3
sudo dnf install gcc
sudo dnf install cmake
git clone --branch v1.3.0 https://github.com/njoy/NJOY21.git
cd NJOY21
mkdir bin
cd bin
cmake -D CMAKE_BUILD_TYPE=Release ..
make
make test
