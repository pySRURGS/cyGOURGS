import numpy as np
from libcpp.string cimport string

cdef extern from "enumerator_container.h":
    void createEnumerator();
    void add_operator(string param, int arity);
    void add_variable(string param);
    string uniform_random_global_search_once(int n)    

cpdef py_createEnumerator():
    createEnumerator()
    
cpdef py_add_operator(mystring, arity):
    mystring_ = mystring.encode('utf-8')
    add_operator(mystring_, arity)
    
cpdef py_add_variable(mystring):
    mystring_ = mystring.encode('utf-8')
    add_variable(mystring_)

def py_uniform_random_global_search_once(n):
    
    mystring_ = uniform_random_global_search_once(n).decode('utf-8')
    return mystring_
