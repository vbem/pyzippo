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
# import testing_module
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def setUpModule():
    # raise unittest.SkipTest('in setUpModule')
    pass

def tearDownModule():
    pass
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @unittest.skip('before class')
class Test_all(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # raise unittest.SkipTest('in setUpClass')
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # self.skipTest('in setUp')
        pass

    def tearDown(self):
        pass

    # @unittest.skip("before method")
    # @unittest.expectedFailure
    def test_asserts(self):
        # print(self.id())
        # self.skipTest('in method')
        
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)

        self.assertTrue(1<2)
        self.assertFalse(1>2)

        self.assertIs(1, 1)
        self.assertIsNot(1, 2)

        self.assertIsNone(None)
        self.assertIsNotNone(False)

        self.assertIn(1, [1,2])
        self.assertNotIn(3, [1,2])

        self.assertIsInstance('', str)
        self.assertNotIsInstance(b'', str)

        self.assertAlmostEqual(0.00000001,0.000000002)
        self.assertNotAlmostEqual(0.0001,0.0002)

        self.assertGreater(2,1)
        self.assertGreaterEqual(2,2)

        self.assertLess(1,2)
        self.assertLessEqual(2,2)

        self.assertRegex('1bc123xyz', r'[a-zA-Z]+\d{3,}[a-zA-Z]+')
        self.assertNotRegex('1bc123xyz', r'[a-zA-Z]+\d{1,2}[a-zA-Z]+')

        self.assertCountEqual((1,2,3,2), (3,2,2,1))

        with self.assertRaises(TypeError) as context:
            ''.split(123)
        self.assertIsInstance(context.exception, Exception)
        with self.assertRaisesRegex(TypeError, 'str'):
            ''.split(123)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    unittest.main(verbosity=2)