# This code is the interface between the python ant.py and the 
# c++ GOURGS codeset 
import numpy as np
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.map cimport map

cdef extern from "primitiveset.h":
    # Declare a c++ class interface for primitiveset
    cdef cppclass PrimitiveSet:
        PrimitiveSet() except +
        void add_operator(string, int)
        void add_variable(string)

        void set_operators_map(map[int, vector[string]])
        void set_fitting_parameters(vector[string])
        void set_variables(vector[string])
        void set_names(vector[string])

        vector[string] get_operators(int)
        vector[int] get_arities()

        map[int, vector[string]] get_operators_map()
        vector[string] get_fitting_parameters()
        vector[string] get_variables()
        vector[string] get_names()
        
def rebuild_primitiveset():
    p = CyPrimitiveSet
    return p        

cdef class CyPrimitiveSet:
    # Create Cython wrapper class for primitiveset
    # See the C++ implementation for details 
    cdef PrimitiveSet primitiveSet

    def __getstate__(self):
        return (self.primitiveSet.get_operators_map(),
                self.primitiveSet.get_fitting_parameters(),
                self.primitiveSet.get_variables(),
                self.primitiveSet.get_names())

    def __setstate__(self,x):
        (operators_map,
         fitting_parameters,
         variables,
         names) = x
        self.primitiveSet.set_operators_map(operators_map)
        self.primitiveSet.set_fitting_parameters(fitting_parameters)
        self.primitiveSet.set_variables(variables)
        self.primitiveSet.set_names(names)
        
    def add_operator(self, mystring, arity):
        mystring_ = mystring.encode('utf-8')
        self.primitiveSet.add_operator(mystring_, arity)

    def add_variable(self, mystring):
        mystring_ = mystring.encode('utf-8')
        self.primitiveSet.add_variable(mystring_)

    def get_arities(self):
        return self.primitiveSet.get_arities()

    def get_operators(self, arity):
        operators = self.primitiveSet.get_operators(arity)
        return operators
               
cdef extern from "enumerator.h":
    # Declare a c++ class interface for enumerator
    cdef cppclass Enumerator:
        Enumerator() except +
        void init(PrimitiveSet)
        int get_Q(int)
        vector[int] calculate_Q(int)
        vector[string] exhaustive_global_search(int,int)
        string uniform_random_global_search_once(int,long)
        vector[string] uniform_random_global_search(int,int,vector[long])
        string generate_specified_solution(int, int, int, int)
        PrimitiveSet m_primitiveSet


def rebuild_enumerator(pset):
    p = CyEnumerator(pset)
    return p


cdef class CyEnumerator:
    # Create Cython wrapper class for enumerator
    # See the C++ implementation for details 
    cdef CyPrimitiveSet primitiveSet
    cdef Enumerator enumerator
    
    def __init__(self, CyPrimitiveSet pset):
        self.primitiveSet = pset
        self.enumerator = Enumerator()
        self.enumerator.init(pset.primitiveSet)

    def __getstate__(self):
        return (self.primitiveSet,)

    def __setstate__(self, x):
        (self.primitiveSet,) = x
        pset = self.primitiveSet
        self.enumerator.init(pset.primitiveSet)
        
    def calculate_Q(self, n):
        weights = self.enumerator.calculate_Q(n)
        Q = self.enumerator.get_Q(n)
        return Q, weights
        
    def exhaustive_global_search(self, n, max_iters=None):
        if max_iters is not None:
            v = self.enumerator.exhaustive_global_search(n, max_iters)
        else:
            v = self.enumerator.exhaustive_global_search(n, 0)
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy
        
    def uniform_random_global_search_once(self, n, seed):
        # returns utf-8 decoded string
        cdef long local_seed = 0;
        if seed is not None:
            local_seed = seed
        else:
            local_seed = 0
        s = self.enumerator.uniform_random_global_search_once(n, local_seed)
        s = s.decode('utf-8')
        return s
        
    def uniform_random_global_search(self, n, iter, seeds):
        cdef vector[string] v;
        if type(seeds) == list():
            v = self.enumerator.uniform_random_global_search(n, iter, seeds)
        else:
            v = self.enumerator.uniform_random_global_search(n, iter,[])
        vcopy = vector[string](v.size())
        for i in range(0,v.size()):
            vcopy[i] = v[i].decode('utf-8')
        return vcopy
        
    def generate_specified_solution(self, i, r, s, n):
        return self.enumerator.generate_specified_solution(i, r, s, n)
