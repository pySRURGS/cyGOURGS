import os
import sys
import types
import unittest
import time
import numpy as np
from operator import add, sub, truediv, mul
sys.path.append(os.path.join('.', 'pyGOURGS'))
sys.path.append(os.path.join('.', 'examples'))
import pyGOURGS.pyGOURGS as pg
import cython_call as cy

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.pset = cy.CyPrimitiveSet()
        self.pset.add_operator('add', 2)
        self.pset.add_operator('sub', 1)
        self.pset.add_operator('truediv', 3)
        self.pset.add_operator('mul', 1)
        self.pset.add_variable('x')
        self.pset.add_variable('y')
        self.enum = cy.CyEnumerator(self.pset)
        
        # to allow for use of pyGOURGS' compile function
        self.pset_pg = pg.PrimitiveSet()
        self.pset_pg.add_operator('add', 2)
        self.pset_pg.add_operator('sub', 1)
        self.pset_pg.add_operator('truediv', 3)
        self.pset_pg.add_operator('mul', 1)
        self.pset_pg.add_variable('x')
        self.pset_pg.add_variable('y')
        
    def test_base_one(self):
        self.assertEqual(self.enum.decimal_to_base_m(5,1), [1,1,1,1,1])
        self.assertEqual(self.enum.base_m_to_decimal(11111,1), 5)

    def test_base_two(self):
        self.assertEqual(self.enum.decimal_to_base_m(5,2), [1,0,1])
        self.assertEqual(self.enum.base_m_to_decimal(101,2), 5)
           
    def test_base_three(self):
        self.assertEqual(self.enum.decimal_to_base_m(125,3), [1,1,1,2,2])
        self.assertEqual(self.enum.base_m_to_decimal(11122,3), 125)
       
    def test_base_nine(self):
        self.assertEqual(self.enum.decimal_to_base_m(125,9), [1,4,8])
        self.assertEqual(self.enum.base_m_to_decimal(148,9), 125)

    def test_count_unique_trees(self):
        trees = list()
        N_trees = 20
        for i in range(0,N_trees):
            tree = self.enum.ith_n_ary_tree(i)
            trees.append(tree)
        self.assertEqual(len(list(set(trees))), N_trees)
    
    def test_terminal(self):
        self.assertEqual(self.enum.ith_n_ary_tree(0), '..')

    def test_operator_1(self):
        self.assertEqual(self.enum.ith_n_ary_tree(1), '[..]')

    def test_operator_2(self):
        self.assertEqual(self.enum.ith_n_ary_tree(2), '[..,..]')

    def test_operator_3(self):
        self.assertEqual(self.enum.ith_n_ary_tree(3), '[..,..,..]')

    def test_count_operators_0(self):
        self.assertEqual(self.enum.calculate_l_i_b(0, 0), 0)

    def test_count_operators_0(self):
        self.assertEqual(self.enum.calculate_l_i_b(1, 0), 1)

    def test_count_operators_0(self):
        self.assertEqual(self.enum.calculate_l_i_b(2, 1), 1)
        self.assertEqual(self.enum.calculate_l_i_b(2, 0), 0)
        self.assertEqual(self.enum.calculate_l_i_b(1, 0), 1)
        self.assertEqual(self.enum.calculate_l_i_b(4, 0), 2)

    def test_count_total_configurations_operators_0(self):
        self.assertEqual(self.enum.calculate_G_i_b(4,0), 4)
        self.assertEqual(self.enum.calculate_G_i_b(11,0), 4)

    def test_count_total_configurations_all_arities_0(self):
        self.assertEqual(self.enum.calculate_R_i(0),1)
        self.assertEqual(self.enum.calculate_R_i(1),2)
        self.assertEqual(self.enum.calculate_R_i(2),1)
        self.assertEqual(self.enum.calculate_R_i(3),1)
        self.assertEqual(self.enum.calculate_R_i(11),4)

    def test_count_total_configurations_terminals_0(self):
        self.assertEqual(self.enum.calculate_a_i(0),1)
        self.assertEqual(self.enum.calculate_a_i(1),1)
        self.assertEqual(self.enum.calculate_a_i(2),2)
        self.assertEqual(self.enum.calculate_a_i(3),3)
        self.assertEqual(self.enum.calculate_a_i(4),1)
        self.assertEqual(self.enum.calculate_a_i(5),2)
        
    def test_count_total_configurations_terminals_0(self):
        self.assertEqual(self.enum.calculate_S_i(0),2)
        self.assertEqual(self.enum.calculate_S_i(1),2)
        self.assertEqual(self.enum.calculate_S_i(2),4)
        self.assertEqual(self.enum.calculate_S_i(3),8)
        self.assertEqual(self.enum.calculate_S_i(4),2)
        self.assertEqual(self.enum.calculate_S_i(5),4)
         
    def test_uniform_random_global_search(self):
        solns = []
        for soln in self.enum.uniform_random_global_search(10000, 10):
            solns.append(soln)
        self.assertEqual(len(solns), len(list(set(solns))), 10)
        soln = self.enum.uniform_random_global_search_once(10000)
        self.assertEqual(type(soln), str)
        solns = []
        for soln in self.enum.exhaustive_global_search(2,5):
            solns.append(soln)
        self.assertEqual(len(solns), 5)
        func = pg.compile(soln, self.pset_pg)
        self.assertEqual(type(func), types.FunctionType)
        
if __name__ == '__main__':
    unittest.main()