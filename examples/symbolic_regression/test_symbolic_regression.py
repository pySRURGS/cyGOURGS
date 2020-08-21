'''
Test script for the symbolic regression routine in cyGOURGS
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

class TestSuite(unittest.TestCase):

    def setUp(self):
        self._output_db = './output_db.test'
        self._dataset_path = './weights_data.csv'
        self._weights_path = './weights.csv'
        self._funcs_arity_two = 'add,sub,div,mul'
        self._funcs_arity_one = 'cos,sin,tanh'
               
        
    def test_base_one(self):
        sh.python('symbolic_regression.py', self._dataset_path, self._output_db)
        self.assertEqual(os.path.isfile(self._output_db), True)
        sh.rm(self._output_db)


if __name__ == '__main__':
    unittest.main(verbosity=2)