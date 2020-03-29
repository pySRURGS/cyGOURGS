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
import pdb

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
        self.enum_pg = pg.Enumerator(self.pset_pg)
        
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
        for i in range(0, 10):
            soln = self.enum.uniform_random_global_search_once(10000, i)
            soln_pg = self.enum_pg.uniform_random_global_search_once(10000, i)
            func = pg.compile(soln, self.pset_pg)
            self.assertEqual(type(func), types.FunctionType)
            func_pg = pg.compile(soln_pg, self.pset_pg)
            self.assertEqual(type(func_pg), types.FunctionType)

    def test_timing_and_uniqueness_random_search(self):
        iters = 100
        init = time.time()
        solns = list()
        solns_pg = list()
        for i in range(0, iters):
            soln = self.enum.uniform_random_global_search_once(10000, i)
            solns.append(soln)
        delta = time.time() - init
        for i in range(0, iters):    
            soln_pg = self.enum_pg.uniform_random_global_search_once(10000, i)
            solns_pg.append(soln_pg)
        delta_pg = time.time() - delta - init
        self.assertGreater(delta_pg, 50*delta)
        n_unique = len(list(set(solns)))
        n_unique_pg = len(list(set(solns_pg)))
        self.assertGreater(n_unique, 0.98*iters)
        self.assertGreater(n_unique_pg, 0.98*iters)
        
    def test_compare_exhaustive_search_pg_vs_cy(self):        
        for num_trees in range(1, 6):
            cy_solns = self.enum.exhaustive_global_search(num_trees)
            py_solns = self.enum_pg.exhaustive_global_search(num_trees)
            for cy_soln, py_soln in zip(cy_solns, py_solns):          
                self.assertEqual(cy_soln, py_soln)

    def test_compare_generate_specified_solution(self):
        for i in [1, 10, 1000, 10000]:
            N = i + 1            
            R_i = self.enum.calculate_R_i(i)
            S_i = self.enum.calculate_S_i(i)
            R_i_pg = self.enum_pg.calculate_R_i(i)
            S_i_pg = self.enum_pg.calculate_S_i(i)
            r = int(R_i/2)
            s = int(S_i/2)
            self.assertEqual(R_i, R_i_pg)
            self.assertEqual(S_i, S_i_pg)
            cy_soln = self.enum.generate_specified_solution(i, r, s, N)
            py_soln = self.enum_pg.generate_specified_solution(i, r, s, N)
            self.assertEqual(cy_soln.decode('utf-8'), py_soln)
            
            
if __name__ == '__main__':
    unittest.main(verbosity=2)
