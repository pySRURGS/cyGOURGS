![Binoculars](cyGOURGS.svg)

WORK-IN-PROGRESS (NOT FINISHED)

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
4. Memoization of methods for speed
5. API is similar to that of the popular DEAP genetic programming software

## Getting Started

The software is run using C++11. It is run using the terminal.

## Installing

You can install directly from github via the repository.

```
git clone https://github.com/pySRURGS/cyGOURGS.git
cd cyGOURGS
```

You need to have the `boost` library installed/downloaded.

On Linux, you can download [boost_1_72_0](https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.gz) and unzip the `boost_1_72_0` folder to `~/boost/boost_1_72_0`.

The bash commands to do this are:
```
curl https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.gz --output ~/boost_1_72_0.tar.gz
tar -xvf ~/boost_1_72_0.tar.gz -C ~/boost/boost_1_72_0
```

On Windows, you can download [boost_1_72_0](https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.zip) and unzip the `boost_1_72_0` folder to `C:/boost/boost_1_72_0`.

After downloading `boost`, run the following commands using the terminal (git bash terminal on Windows),
```
bash make.sh
cd examples
bash cybuild.sh
```

## Authorship

Port from Python to Cython/C++ performed by Razvan Tarnovan in collaboration with Sohrab Towfighi.

Copyright belongs to Sohrab Towfighi.

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE.txt) file for details

## How to Cite

If you use this software in your research, then please cite our papers.

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
