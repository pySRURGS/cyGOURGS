import numpy as np
from libcpp.string cimport string
    
cdef extern from "primitiveset.h":
    cdef cppclass PrimitiveSet:
        PrimitiveSet()
        void add_operator(string, int)
        void add_variable(string)
      
cdef class PyPrimitiveSet:
    cdef PrimitiveSet *thisptr
    def __cinit__(self):
        self.thisptr = new PrimitiveSet()
    def __dealloc__(self):
        del self.thisptr
    def add_operator(self, mystring, arity):
        mystring_ = mystring.encode('utf-8')
        self.thisptr.add_operator(mystring_, arity)
    def add_variable(self, mystring):
        mystring_ = mystring.encode('utf-8')
        self.thisptr.add_variable(mystring_)         

cdef extern from "enumerator.h":
    cdef cppclass Enumerator:
        Enumerator(PrimitiveSet*)
        string uniform_random_global_search_once(int)  
        
cdef class PyEnumerator:
    cdef PyPrimitiveSet primitiveSet
    cdef Enumerator *thisptr
    def __init__(self, PyPrimitiveSet primitiveSet):
        self.primitiveSet = primitiveSet
        self.thisptr = new Enumerator(self.primitiveSet.thisptr)
    def __dealloc__(self):
        del self.thisptr
    def uniform_random_global_search_once(self,n):
        mystring_ = self.thisptr.uniform_random_global_search_once(n).decode('utf-8')
        return mystring_