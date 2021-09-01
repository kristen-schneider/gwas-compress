import unittest
import numpy as np

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

class TestCodecs(unittest.TestCase):
    VAR1 = 0

    def test_function(self):
            self.assertEqual(function(), self.VAR1)

if __name__ == '__main__':
    unittest.main()
