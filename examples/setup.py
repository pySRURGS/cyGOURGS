from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy

extensions = [
    Extension('cython_call', ['cython_call.pyx', '../enumerator.cpp', '../primitiveset.cpp'],
              include_dirs=[numpy.get_include(), 'c:/boost/boost_1_72_0', '..'],
              language='c++',
              extra_compile_args=["-std=c++11"],
              extra_link_args=["-std=c++11"]
              ),
]

setup(
    ext_modules=cythonize(extensions, compiler_directives={'language_level' : "3"})
    #extra_compile_args=["-w", '-g'],
)
