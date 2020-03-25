# This script is used during development to figure out how to enable pickling 
# of Cython class instances

sample_eqn = 'prog3(prog3(ant.turn_right(),ant.move_forward(),ant.turn_left()),ant.if_food_ahead(ant.move_forward(),ant.move_forward()),prog3(ant.move_forward(),ant.move_forward(),prog2(ant.move_forward(),ant.move_forward())))'

import multiprocessing as mp
import parmap
import pdb
import argparse 
import sys,os
sys.path.append(os.path.join('..', 'pyGOURGS'))
import cython_call as cy
import pyGOURGS as pg
import pickle
from ant import str2bool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='minimal_working_pickle.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("cppimpl", help="should use cpp implementation of algorithms?(True - cpp False - python)", type=str2bool)
    arguments = parser.parse_args()
    cppimpl = arguments.cppimpl
    if cppimpl == True:
        print("Ran in c++ mode")
    else:
        print("Ran in python mode")

    if cppimpl != True:
        pset = pg.PrimitiveSet()
        pset.add_operator("ant.if_food_ahead", 2)
        pset.add_operator("prog2", 2)
        pset.add_operator("prog3", 3)
        pset.add_variable("ant.move_forward()")
        pset.add_variable("ant.turn_left()")
        pset.add_variable("ant.turn_right()")
        enum = pg.Enumerator(pset)
    elif cppimpl == True:
        pset = cy.CyPrimitiveSet()        
        pset.add_operator("ant.if_food_ahead", 2)
        pset.add_operator("prog2", 2)
        pset.add_operator("prog3", 3)
        pset.add_variable("ant.move_forward()")
        pset.add_variable("ant.turn_left()")
        pset.add_variable("ant.turn_right()")
        enum = cy.CyEnumerator(pset)
        
    # pickle PrimitiveSet
    d = pickle.dumps(pset)
    del(pset)

    # unpickle PrimitiveSet
    pset = pickle.loads(d)

    # run basic tests
    assert(pset.get_arities() == [2, 3])
    if cppimpl == False:
        assert(pset.get_operators() == [["ant.if_food_ahead", "prog2"], 
                                        ["prog3"]])
    else:
        assert(pset.get_operators(2) == [b'ant.if_food_ahead', b'prog2'])

    # pickle Enumerator
    d = pickle.dumps(enum)
    del(enum)

    # unpickle Enumerator   
    enum = pickle.loads(d)

    # run basic test
    if cppimpl == False:
        assert(type(enum._pset) == type(pset))
    else:
        assert(enum.__getstate__()[0].get_arities() == [2, 3])       
        assert(enum.generate_specified_solution(100,2,11,1100).decode('utf-8') 
               == sample_eqn)

    print("Passed all tests")