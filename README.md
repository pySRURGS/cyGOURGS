![Binoculars](cyGOURGS.svg)

[![Build Status](https://travis-ci.org/pySRURGS/cyGOURGS.svg?branch=master)](https://travis-ci.org/pySRURGS/cyGOURGS)
[![License: GPL v3](images/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![python versions](images/python-3_6_3_7-blue.svg)](https://www.python.org)

# Global Optimization by Uniform Random Global Search

Users who are unfamiliar with this software or with C++ should refer to the 
python version of this same software [pyGOURGS](https://github.com/pySRURGS/pyGOURGS). 
This is a C++ port of pyGOURGS, produced to increase the performance of the 
software.

This software package solves problems whose solutions can be represented as 
n-ary trees. These problems are typically solved using genetic programming. 
For these problems, there is often little to no relationship between the data
structure representation of a candidate solution and the ultimate performance of 
the candidate solution, once the data structure representation has been 
evaluated to its human readable form. This makes pure random search an 
attractive algorithm with which to solve these kinds of problems. This software 
is aimed at engineers, researchers and data scientists working in data analysis 
and computational optimization.

## Features 

1. Developed and tested on C++11
2. Can be run in deterministic mode for reproducibility
3. Can also run an exhaustive/brute-force search
4. API is similar to that of the popular DEAP genetic programming software

## Installing

Prerequisite software includes: Python3.6, terminal, and gcc.

### On Linux 
This is the preferred platform as it is very easy to install on Ubuntu Linux.
On Ubuntu 18.04 Linux, everything but the Boost C++ codes are preinstalled by your distribution.
You can install boost using "sudo apt-get install libboost-dev"

### On Windows
Users would need to install Python3.6 if they do not have it installed [download](https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe). They will need to download [git](https://git-scm.com/download/win) to use git bash. They will also need to install MinGW64 [download](https://sourceforge.net/projects/mingw/) in order to use gcc.  Windows users will also need to install boost [download](https://dl.bintray.com/boostorg/release/1.72.0/source/) and then edit the `boost_path = '.'` variable in `setup.py` and the `path_to_boost` variable in `install.sh` to point to the directory where the `boost` subdirectory is housed. 

### On Both Linux and Windows

Copy the repository to your computer using git bash using the following commands.

```
git clone https://github.com/pySRURGS/cyGOURGS.git
cd cyGOURGS
```

Then, you can compile the code using

```
bash install.sh
```

## Usage

Users of pyGOURGS are referred to the similarly named `ant.py` in `./cyGOURGS/examples/ant.py` which has an identical interface with the addition of the `cppimpl` flag, which uses the C++ cyGOURGS when `True` and which uses the python3 pyGOURGS when `False`.

## Authorship

Port from Python to Cython/C++ performed by Razvan Tarnovan in collaboration with Sohrab Towfighi.

Copyright belongs to Sohrab Towfighi.

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE.txt) file for details

## How to Cite

If you use this software in your research, then please cite us.

Towfighi, S., (2020). pyGOURGS - global optimization of n-ary tree representable problems using uniform random global search. Journal of Open Source Software, 5(47), 2074, https://doi.org/10.21105/joss.02074

## Community

If you would like to contribute to the project or you need help, then please create an issue.

With regards to community suggested changes, I would comment as to whether it would be within the scope of the project to include the suggested changes. If both parties are in agreement, whomever is interested in developing the changes can make a pull request, or I will implement the suggested changes.

## Acknowledgments

* The example scripts are derived from the DEAP project: [link](https://github.com/DEAP/deap)
* Luther Tychonievich created the algorithm mapping integers to full binary trees: [link](https://www.cs.virginia.edu/luther/blog/posts/434.html), [web archived link](http://web.archive.org/web/20190908010319/https://www.cs.virginia.edu/luther/blog/posts/434.html).
* The icon is derived from the GNOME project and the respective artists. Taken from [link](https://commons.wikimedia.org/wiki/File:Gnome-system-run.svg), [web archived link](https://web.archive.org/web/20161010072611/https://commons.wikimedia.org/wiki/File:Gnome-system-run.svg). License: LGPL version 3.0. 

## References

- Koza JR, Koza JR. Genetic programming: on the programming of computers by means of natural selection. MIT press; 1992.
- Towfighi S. Symbolic regression by uniform random global search. SN Applied Sciences. 2020 Jan 1;2(1):34. [https://doi.org/10.1007/s42452-019-1734-3](https://doi.org/10.1007/s42452-019-1734-3)
