from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy
import sys
import pdb
import os
import platform

path_to_boost = None 
from boost_path import * # We define path_to_boost inside this file

if platform.system() == 'Darwin':
    msg = "We do not support Mac. You can remove this error and try your luck"
    raise Exception(msg)

if os.path.isdir(path_to_boost) == False and platform.system() == 'Windows':
    msg = 'path_to_boost must be defined on Windows'
    raise Exception(msg)

if platform.system() == 'Linux':
    path_to_boost = '.'

os.environ["CC"] = "g++" # Use G++ as compiler

extensions = [
    Extension('cython_call', ['cython_call.pyx', 
                              'enumerator.cpp', 
                              'primitiveset.cpp'],
              include_dirs=[numpy.get_include(), 
                            path_to_boost, 
                            '.'],
              language='c++',
              extra_compile_args=["-std=c++11"],
              extra_link_args=["-std=c++11"]
              ),
]

setup(ext_modules=cythonize(extensions, 
                            compiler_directives={'language_level' : "3"}))
