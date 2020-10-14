'''
Test script for the symbolic regression routine in cyGOURGS

Sohrab Towfighi (C) 2020
'''

import os
import sys
import unittest
import numpy as np
sys.path.append(os.path.join('.', '..'))
import pdb
try:
    import sh
except ImportError:
    # fallback: emulate the sh API with pbs
    import pbs
    class Sh(object):
        def __getattr__(self, attr):
            return pbs.Command(attr)
    sh = Sh()

# TODO: Replicate test suite of pySRURGS
# TODO: Ensure both command line interface and python interface function 
    
class TestCommandLineInterface(unittest.TestCase):

    def setUp(self):
        self._output_db = './output_db.test'
        self._dataset_path = './weights_data.csv'
        self._weights_path = './weights.csv'
        self._funcs_arity_two = 'add,sub,div,mul'
        self._funcs_arity_one = 'cos,sin,tanh'
                
    def test_cli_single_processor_deterministic(self):            
        output = sh.python3('symbolic_regression.py', 
                            '-multiprocessing', False,
                            '-deterministic', True, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)
        
    def test_cli_zero_fit_params(self):
        output = sh.python3('symbolic_regression.py', 
                            '-deterministic', True,
                            '-max_num_fit_params', 0, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)
        
    def test_cli_five_fit_params(self):
        output = sh.python3('symbolic_regression.py', 
                            '-deterministic', True,
                            '-max_num_fit_params', 5,  
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)

    def test_cli_funcs_arity_two(self):
        output = sh.python3('symbolic_regression.py', 
                            '-deterministic', True,
                            '-funcs_arity_two', 'add,sub,div', 
                            '-max_num_fit_params', 1,
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)

    def test_cli_funcs_arity_one(self):
        output = sh.python3('symbolic_regression.py', 
                            '-deterministic', True,
                            '-funcs_arity_one', 
                            'tan,exp,sinh,cosh', '-funcs_arity_two', 'add',
                            '-max_num_fit_params', 1, 
                            '-path_to_db', working_db, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)

    def test_cli_max_permitted_trees(self):
        output = sh.python3('symbolic_regression.py', 
                            '-deterministic', True,
                            '-max_permitted_trees', 10, 
                            '-max_num_fit_params', 5, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)

    def test_cli_combo_params_exhaustive_1(self):        
        output = sh.python3('symbolic_regression.py', 
                            '-exhaustive', True, 
                            '-funcs_arity_two', 'add,sub', 
                            '-funcs_arity_one', 'sin', 
                            '-max_permitted_trees', 3, 
                            '-max_num_fit_params', 1, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)

    def test_cli_combo_params_exhaustive_2(self):
        output = sh.python3('symbolic_regression.py', 
                            '-exhaustive', True, 
                            '-funcs_arity_two', 'add,sub', 
                            '-max_permitted_trees', 3, 
                            '-max_num_fit_params', 1, 
                            self._dataset_path, 
                            self._output_db)
        output = output.strip()
        print(output)
        

class TestPythonInterface(unittest.TestCase):

    def setUp(self):
        self.pset = cy.CyPrimitiveSet()
        self.pset.add_operator('add', 2)
        self.pset.add_operator('sub', 1)
        self.pset.add_operator('truediv', 3)
        self.pset.add_operator('mul', 1)
        self.pset.add_variable('x')
        self.pset.add_variable('y')
        self.enum = cy.CyEnumerator(self.pset)

    def test_count_unique_trees(self):
        trees = list()
        N_trees = 20
        for i in range(0,N_trees):
            tree = self.enum.ith_n_ary_tree(i)
            trees.append(tree)
            print(tree)
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
        func = sr.compile(soln, self.pset)
        self.assertEqual(type(func), types.FunctionType)


if __name__ == '__main__':
    unittest.main(verbosity=2)