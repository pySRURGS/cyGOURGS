import multiprocessing as mp
import parmap
import pdb
import sys,os
sys.path.append(os.path.join('..', 'pyGOURGS'))
import cython_call as cy
import pyGOURGS as pg
import pickle

# IN ORDER TO RUN AGAINST PYTHON, SET TO FALSE
# IN ORDER TO RUN AGAINST C++, SET TO TRUE
cppimpl = True
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
assert(pset.get_operators() == [["ant.if_food_ahead", "prog2"], ["prog3"]])

# pickle Enumerator
d = pickle.dumps(enum)
del(enum)

# unpickle Enumerator
enum = pickle.loads(d)
assert(enum)

# run basic test
if cppimpl == False:
    assert(type(enum._pset) == type(pset))
else:
    assert(type(enum.primitiveSet) == type(pset))

print("Passed all tests")