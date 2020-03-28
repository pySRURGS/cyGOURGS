from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy
import sys
try:
    import sh
except ImportError: # on Windows
    # fallback: emulate the sh API with pbs
    import pbs

    class Sh(object):
        def __getattr__(self, attr):
            return pbs.Command(attr)
    sh = Sh()

boost_path = sh.echo('~').strip() + '/boost_1_72_0'

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
