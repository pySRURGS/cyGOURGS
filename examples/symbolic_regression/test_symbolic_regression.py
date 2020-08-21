import os
import sh
import sys
import unittest
import numpy as np
sys.path.append(os.path.join('.', '..'))
import pdb

class TestSuite(unittest.TestCase):

    def setUp(self):
        dataset_path = './weights_data.csv'
        weights_path = './weights.csv'
        funcs_arity_two = 'add,sub,div,mul'
        funcs_arity_one = 'cos,sin,tanh'
        
        
        
    def test_base_one(self):
        self.assertEqual(self.enum.decimal_to_base_m(5,1), [1,1,1,1,1])
        self.assertEqual(self.enum.base_m_to_decimal(11111,1), 5)
   
            
if __name__ == '__main__':
    unittest.main(verbosity=2)
