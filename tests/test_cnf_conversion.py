import unittest
from src.convert2CNF import convert2CNF
from src.globals import *

class CNFConversionTests(unittest.TestCase):
    def setUp(self):
        self.c = convert2CNF()

    def test_and_cnf(self):
        self.assertEqual(self.c.CNF("p{0}q{1}r".format(AND,AND)), "(p{0}q{1}r)".format(AND,AND))
        self.assertEqual(self.c.CNF("(p{0}((q){1}r)){2}s".format(AND,AND,AND)), "((p{0}((q){1}r)){2}s)".format(AND,AND,AND))

    def test_or_cnf(self):
        self.assertEqual(self.c.CNF("p{0}q{1}r".format(OR,OR)), "(p{0}q{1}r)".format(OR,OR))
        self.assertEqual(self.c.CNF("(p{0}((q){1}r)){2}s".format(OR,OR,OR)), "(p{0}q{1}r{2}s)".format(OR,OR,OR))

    def test_implies_cnf(self):
        self.assertEqual(self.c.CNF("p{0}q".format(IMPLIES)), "({0}p{1}q)".format(NOT, OR))
        self.assertEqual(self.c.CNF("(p{0}q){1}r".format(IMPLIES,IMPLIES)), "({0}({1}p{2}q){3}r))".format(NOT,NOT,OR,OR))
        self.assertEqual(self.c.CNF("p{0}q{1}r".format(IMPLIES,IMPLIES)), "({0}p{1}({2}q{3}r))".format(NOT,OR,NOT,OR))
        self.assertEqual(self.c.CNF("p{0}q{1}r{2}s".format(IMPLIES,IMPLIES)), "({0}({1}({2}p{3}q){4}r){5}s)".format(NOT,NOT,NOT,OR,OR,OR))


    def test_biconditional(self):
         self.assertEqual(self.c.CNF("p{0}q".format(BICONDITIONAL)), "({0}p{1}q){2}({3}q{4}p)".format(NOT, OR, AND, NOT, OR))

if __name__ == '__main__':
    unittest.main()