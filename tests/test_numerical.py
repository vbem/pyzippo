#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""https://docs.python.org/3/library/unittest.html
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import unittest
from pyzippo import numerical
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Test_numerical(unittest.TestCase):

    def test_approximate(self):
        
        self.assertTrue(numerical.approximate(1e-7,2e-7))
        self.assertFalse(numerical.approximate(1e-7,3e-7))

        self.assertTrue(numerical.approximate(1,2,10))
        self.assertFalse(numerical.approximate(1e-9,2e-9,1e-10))

        with self.assertRaises(TypeError):
            numerical.approximate(None,0)
        with self.assertRaises(TypeError):
            numerical.approximate(12.2,'12')
        with self.assertRaises(TypeError):
            numerical.approximate(1,1,'100')
        
    