from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy
import sys
import pdb

# On Windows, the user needs to specify the path where they installed boost
# Edit the following variable to reflect the correct path.
boost_path = '.'

extensions = [
    Extension('cython_call', ['cython_call.pyx', 
                              'enumerator.cpp', 
                              'primitiveset.cpp'],
              include_dirs=[numpy.get_include(), 
                            boost_path, 
                            '.'],
              language='c++',
              extra_compile_args=["-std=c++11"],
              extra_link_args=["-std=c++11"]
              ),
]

setup(ext_modules=cythonize(extensions, 
                            compiler_directives={'language_level' : "3"}))
