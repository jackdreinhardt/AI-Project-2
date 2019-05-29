# import unittest
# from convert2CNF import convert2CNF
# from globals import *

# # to run the tests:
# # python -m unittest test_cnf_conversion.py -v

# # Correct results of CNF conversion come from an online calculator
# class TestCNFConversion(unittest.TestCase):
#     def setUp(self):
#         self.c = convert2CNF()

#     def test_and_cnf(self):
#         self.assertEqual(self.c.CNF(f"p{AND}q{AND}r"), f"(p{AND}q{AND}r)")
#         self.assertEqual(self.c.CNF(f"(p{AND}((q){AND}r)){AND}s"), f"((p{AND}((q){AND}r)){AND}s)")

#     def test_or_cnf(self):
#         self.assertEqual(self.c.CNF(f"p{OR}q{OR}r"), f"(p{OR}q{OR}r)")
#         self.assertEqual(self.c.CNF(f"(p{OR}((q){OR}r)){OR}s"), f"(p{OR}q{OR}r{OR}s)")

#     def test_implies_cnf(self):
#         self.assertEqual(self.c.CNF(f"p{IMPLIES}q"), f"({NOT}p{OR}q)")
#         self.assertEqual(self.c.CNF(f"p{IMPLIES}(q{AND}r)"), f"({NOT}p{OR}q){AND}({NOT}p{OR}r)")
#         self.assertEqual(self.c.CNF(f"(p{IMPLIES}q){IMPLIES}r"), f"(p{OR}r){AND}({NOT}q{OR}r)")
#         self.assertEqual(self.c.CNF(f"p{IMPLIES}(q{IMPLIES}r)"), f"({NOT}p{OR}{NOT}q{OR}r)")
#         # self.assertEqual(self.c.CNF(f"(p{IMPLIES}q){IMPLIES}(r{IMPLIES}s)"), f"(p{OR}{NOT}r{OR}s){AND}({NOT}q{OR}{NOT}r{OR}s)")

#     def test_biconditional_cnf(self):
#         self.assertEqual(self.c.CNF(f"p{BICONDITIONAL}q"), f"({NOT}p{OR}q){AND}({NOT}q{OR}p)")
#         self.assertEqual(self.c.CNF(f"(p{BICONDITIONAL}q){BICONDITIONAL}r"), f"(({NOT}p{OR}q){AND}(p{OR}{NOT}q){AND}({NOT}q{OR}r){AND}(q{OR}{NOT}r))")

#     def test_combinations_cnf(self):
#         self.assertEqual(self.c.CNF(f"(p{IMPLIES}q){BICONDITIONAL}(r{IMPLIES}s)"), f"(p{OR}{NOT}r{OR}s){AND}({NOT}q{OR}{NOT}r{OR}s)")
#         self.assertEqual(self.c.CNF(f"(({NOT}p){IMPLIES}(q{AND}r)){BICONDITIONAL}(r{IMPLIES}{NOT}(s{OR}(t{BICONDITIONAL}u)))"), f"({NOT}p{OR}{NOT}r{OR}{NOT}s){AND}({NOT}p{OR}{NOT}r{OR}t){AND}({NOT}p{OR}{NOT}r{OR}{NOT}u){AND}({NOT}q{OR}{NOT}r{OR}{NOT}s){AND}({NOT}q{OR}{NOT}r{OR}t){AND}({NOT}q{OR}{NOT}r{OR}{NOT}u)")

#     def test_or_over_and_distribution(self):
#         self.assertEqual(self.c.CNF(f"(p{AND}q){OR}r"), f"(p{OR}r){AND}(q{OR}r)")
#         self.assertEqual(self.c.CNF(f"r{OR}(p{AND}q)"), f"(r{OR}p){AND}(r{OR}q)")

#     def test_de_morgan(self):
#         self.assertEqual(self.c.CNF(f"{NOT}(({NOT}p{OR}q){AND}({NOT}q{OR}p))"),f"({NOT}p{OR}{NOT}q){AND}(p{OR}q)")

# if __name__ == '__main__':
#     unittest.main()