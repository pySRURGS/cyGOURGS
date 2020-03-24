import numpy as np
from libcpp.string cimport string
from libcpp.vector cimport vector
    
cdef extern from "primitiveset.h":
    cdef cppclass PrimitiveSet:
        PrimitiveSet() except +
        void add_operator(string, int)
        void add_variable(string)
      
cdef class CyPrimitiveSet:
    cdef PrimitiveSet primitiveSet
    def rebuild(prim):
        p = CyPrimitiveSet()
        p.primitiveSet = prim.primitiveSet
        return p
    def __reduce__(self):
        return (CyPrimitiveSet.rebuild, (self,))
    def add_operator(self, mystring, arity):
        mystring_ = mystring.encode('utf-8')
        self.primitiveSet.add_operator(mystring_, arity)
    def add_variable(self, mystring):
        mystring_ = mystring.encode('utf-8')
        self.primitiveSet.add_variable(mystring_)

cdef extern from "enumerator.h":
    cdef cppclass Enumerator:
        Enumerator() except +
        void init(PrimitiveSet)
        int get_Q(int)
        vector[int] calculate_Q(int)
        vector[string] exhaustive_global_search(int,int)
        string uniform_random_global_search_once(int)
        vector[string] uniform_random_global_search(int,int)
        
cdef class CyEnumerator:
    cdef CyPrimitiveSet primitiveSet
    cdef Enumerator enumerator
    def rebuild(primitiveSet):
        p = CyEnumerator()
        p.init(primitiveSet)
        return p
    def __reduce__(self):
        return (CyEnumerator.rebuild, (self.primitiveSet,))
    def init(self, prim):
        self.primitiveSet = prim
        self.enumerator.init(self.primitiveSet.primitiveSet)
    def calculate_Q(self,n):
        weights = self.enumerator.calculate_Q(n)
        Q = self.enumerator.get_Q(n)
        return Q, weights
    def exhaustive_global_search(self, n, max_iters=None):
        if max_iters is not None:
            v = self.enumerator.exhaustive_global_search(n,max_iters)
        else:
            v = self.enumerator.exhaustive_global_search(n,0)
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy
    def uniform_random_global_search_once(self,n):
        mystring_ = self.enumerator.uniform_random_global_search_once(n).decode('utf-8')
        return mystring_
    def uniform_random_global_search(self,n, iter, seed):
        v = self.enumerator.uniform_random_global_search(n,iter)
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy


