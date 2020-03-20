import numpy as np
from libcpp.string cimport string
from libcpp.vector cimport vector
    
cdef extern from "primitiveset.h":
    cdef cppclass PrimitiveSet:
        PrimitiveSet()
        void add_operator(string, int)
        void add_variable(string)
      
cdef class CyPrimitiveSet:
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
        int get_Q(int)
        vector[int] calculate_Q(int)
        vector[string] exhaustive_global_search(int,int)
        string uniform_random_global_search_once(int)
        vector[string] uniform_random_global_search(int,int)
        
cdef class CyEnumerator:
    cdef CyPrimitiveSet primitiveSet
    cdef Enumerator *thisptr
    def __init__(self, CyPrimitiveSet primitiveSet):
        self.primitiveSet = primitiveSet
        self.thisptr = new Enumerator(self.primitiveSet.thisptr)
    def __dealloc__(self):
        del self.thisptr
    def calculate_Q(self,n):
        weights = self.thisptr.calculate_Q(n)
        Q = self.thisptr.get_Q(n)
        return Q, weights
    def exhaustive_global_search(self, n, max_iters=None):
        if max_iters is not None:
            v = self.thisptr.exhaustive_global_search(n,max_iters)
        else:
            v = self.thisptr.exhaustive_global_search(n,0)
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy
    def uniform_random_global_search_once(self,n):
        mystring_ = self.thisptr.uniform_random_global_search_once(n).decode('utf-8')
        return mystring_
    def uniform_random_global_search(self,n, iter, seed):
        v = self.thisptr.uniform_random_global_search(n,iter)
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy

