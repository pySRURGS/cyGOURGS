from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy


extensions = [
    Extension('function_call', ['enumerator_call.pyx', 'enumerator_container.cpp', '../enumerator.cpp', '../primitiveset.cpp'],
              include_dirs=[numpy.get_include(), 'c:/boost/boost_1_72_0', '..'],
              #extra_compile_args=['-I '],
              language='c++'
              ),
]

setup(
    ext_modules=cythonize(extensions),
    #extra_compile_args=["-w", '-g'],
)