import unittest
from src.convert2CNF import convert2CNF
from src.globals import *

class CNFConversionTests(unittest.TestCase):
    def setUp(self):
        self.c = convert2CNF()

    def test_and_cnf(self):
        self.assertEqual(self.c.CNF(f"p{AND}q{AND}r"), f"(p{AND}q{AND}r)")
        self.assertEqual(self.c.CNF(f"(p{AND}((q){AND}r)){AND}s"), f"((p{AND}((q){AND}r)){AND}s)")

    def test_or_cnf(self):
        self.assertEqual(self.c.CNF(f"p{OR}q{OR}r"), f"(p{OR}q{OR}r)")
        self.assertEqual(self.c.CNF(f"(p{OR}((q){OR}r)){OR}s"), f"(p{OR}q{OR}r{OR}s)")

    def test_implies_cnf(self):
        self.assertEqual(self.c.CNF(f"p{IMPLIES}q"), f"({NOT}p{OR}q)")
        self.assertEqual(self.c.CNF(f"(p{IMPLIES}q){IMPLIES}r"), f"({NOT}({NOT}p{OR}q){OR}r))")
        self.assertEqual(self.c.CNF(f"p{IMPLIES}q{IMPLIES}r"), f"({NOT}p{OR}({NOT}q{OR}r))")
        self.assertEqual(self.c.CNF(f"p{IMPLIES}q{IMPLIES}r{IMPLIES}s"), f"({NOT}({NOT}({NOT}p{OR}q){OR}r){OR}s)")

    def test_biconditional(self):
        self.assertEqual(self.c.CNF(f"p{BICONDITIONAL}q".format(BICONDITIONAL)), f"({NOT}p{OR}q){AND}({NOT}q{OR}p)")
        self.assertEqual(self.c.CNF(f"p{BICONDITIONAL}q{BICONDITIONAL}r"), f"({NOT}(({NOT}p{OR}q) {AND} ({NOT}q{OR}p)){OR}r){AND}({NOT}r{OR}(({NOT}p{OR}q) {AND} ({NOT}q{OR}p)))")


if __name__ == '__main__':
    unittest.main()