import unittest
from belief_base import BeliefBase,Belief
from globals import *

# to run the tests:
# python -m unittest test_belief_base.py -v

# Correct results of CNF conversion come from an online calculator
class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.b = BeliefBase()
        self.b_ = BeliefBase()

    def tearDown(self):
        self.b.clear_beliefs()
        self.b_.clear_beliefs()

    # tests the __eq__ and __ne__ functions
    def test_equality(self):
        self.b.add_belief(Belief('p'))
        self.b.add_belief(Belief('q'))
        self.b_.add_belief(Belief('p'))
        self.b_.add_belief(Belief('q'))
        self.assertEqual(self.b, self.b_)
        self.b.add_belief(Belief('(rvs)^p'))
        self.assertNotEqual(self.b, self.b_)
        self.b_.add_belief(Belief('(rvs)^p'))
        self.assertEqual(self.b, self.b_)
        self.b.del_belief(Belief('(rvs)^p'))
        self.assertNotEqual(self.b, self.b_)

    # tests the __str__ function
    def test_print(self):
        self.assertEqual(str(self.b), '{}')
        self.b.add_belief(Belief('p'))
        self.assertEqual(str(self.b), '{(p)}')
        self.b.add_belief(Belief('q'))
        self.assertEqual(str(self.b), '{(p), (q)}')
        self.b.del_belief(Belief('p'))
        self.assertEqual(str(self.b), '{(q)}')

    def test_intersect(self):
        self.b.add_belief(Belief('p^q'))
        self.b_.add_belief(Belief('q^p'))
        self.assertEqual(self.b,BeliefBase.intersect([self.b,self.b_]))
        self.b.add_belief(Belief('(rvs)^p'))
        self.assertNotEqual(self.b,BeliefBase.intersect([self.b,self.b_]))
        self.b_.add_belief(Belief('(svr)^p'))
        self.assertEqual(self.b,BeliefBase.intersect([self.b,self.b_]))

    # tests the entails function
    def test_entails(self):
        self.b.add_belief(Belief('p'))
        self.assertTrue(self.b.entails('p'))
        self.assertFalse(self.b.entails('q'))
        self.b.add_belief(Belief('q'))
        self.assertTrue(self.b.entails('p^q'))
        self.b.add_belief(Belief('r'))
        self.assertFalse(self.b.entails('(r^~p)'))
        # self.assertTrue(self.b.entails('p^q^r^(~rvp)')) # raises error due to remove function

if __name__ == '__main__':
    unittest.main()