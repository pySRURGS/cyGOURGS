from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy


extensions = [
    Extension('cython_calls', ['cython_call.pyx', '../enumerator.cpp', '../primitiveset.cpp'],
              include_dirs=[numpy.get_include(), 'c:/boost/boost_1_72_0', '..'],
              language='c++'
              ),
]

setup(
    ext_modules=cythonize(extensions),
    #extra_compile_args=["-w", '-g'],
)