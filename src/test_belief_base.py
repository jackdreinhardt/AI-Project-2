import unittest
from belief_base import BeliefBase,Belief
from globals import *

# Correct results of CNF conversion come from an online calculator
class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.b = BeliefBase()
        self.b_ = BeliefBase()

    # tests the __eq__ function
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

    # tests the entails function
    def test_entails(self):
        self.b.clear_beliefs()
        self.b.add_belief(Belief('p'))
        self.assertTrue(self.b.entails('p'))
        self.assertFalse(self.b.entails('q'))
        self.b.add_belief(Belief('q'))
        self.assertTrue(self.b.entails('p^q'))
        self.b.add_belief(Belief('r'))
        self.assertFalse(self.b.entails('(r^~p)'))
        self.assertTrue(self.b.entails('p^q^r^(~rvp)')) # raises error due to remove function

if __name__ == '__main__':
    unittest.main()