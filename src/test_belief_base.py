import unittest
from belief_base import BeliefBase,Belief

# to run the tests:
# python -m unittest test_belief_base.py -v

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
        self.b_.add_belief(Belief('q'))
        self.b_.add_belief(Belief('p'))
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
        self.assertEqual(self.b,BeliefBase.intersect([self.b]))
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
        self.assertTrue(self.b.entails('p^q^r^(~rvp)')) # raises error due to remove function

    # test the remainder function
    def test_remainders(self):
        self.b.add_belief(Belief('p'))
        self.b.add_belief(Belief('q'))
        r1 = BeliefBase()
        r1.add_belief(Belief('p'))
        r2 = BeliefBase()
        r2.add_belief(Belief('q'))
        self.assertCountEqual(self.b.remainders(Belief('p^q')), [r1,r2])

        self.b.add_belief(Belief('~pvr'))
        r1.clear_beliefs()
        for i in ['p', 'q', '~pvr']:
            r1.add_belief(Belief(i))
        self.assertCountEqual(self.b.remainders(Belief('~r')), [r1])

        self.b.add_belief(Belief('r'))
        r1.clear_beliefs()
        for i in ['q', '~pvr']:
            r1.add_belief(Belief(i))
        r2.clear_beliefs()
        for i in ['p', 'q']:
            r2.add_belief(Belief(i))
        self.assertCountEqual(self.b.remainders(Belief('r')), [r1,r2])

    def test_full_meet_contraction(self):
        for i in ['p', 'q', 'r']:
            self.b.add_belief(Belief(i))
        r = BeliefBase()
        r.add_belief(Belief('r'))
        self.b.contract(Belief('p^q'),'full-meet')
        self.assertEqual(self.b, r)

        self.b.clear_beliefs()
        for i in ['p', 'q', '~pvr','r']:
            self.b.add_belief(Belief(i))
        r.clear_beliefs()
        r.add_belief(Belief('q'))
        self.b.contract(Belief('r'),'full-meet')
        self.assertEqual(self.b, r)

        self.b.clear_beliefs()
        for i in ['~pvr','r']:
            self.b.add_belief(Belief(i))
        r.clear_beliefs()
        r.add_belief(Belief('rv~p'))
        self.b.contract(Belief('r'),'full-meet')
        self.assertEqual(self.b, r)

    def test_maxichoice_contraction(self):
        for i in ['p', 'q', 'r']:
            self.b.add_belief(Belief(i))
        r = BeliefBase()
        for i in ['q', 'r']:
            r.add_belief(Belief(i))
        self.b.contract(Belief('p^q'),'maxichoice')
        self.assertEqual(self.b, r)

        self.b.clear_beliefs()
        for i in ['p', 'q', '~pvr','r']:
            self.b.add_belief(Belief(i))
        r = BeliefBase()
        for i in ['q', 'rv~p']:
            r.add_belief(Belief(i))
        self.b.contract(Belief('r'),'maxichoice')
        self.assertEqual(self.b, r)

    def test_partial_meet_contraction(self):
        for i in ['p', 'q', 'r']:
            self.b.add_belief(Belief(i))
        r = BeliefBase()
        for i in ['q', 'r']:
            r.add_belief(Belief(i))
        self.b.contract(Belief('p^q'),'partial-meet')
        # print(self.b)

    def test_revision(self):
        for i in ['p', 'q', 'r']:
            self.b.add_belief(Belief(i))
        r = BeliefBase()
        for i in ['p', 'q', 'r','p^q']:
            r.add_belief(Belief(i))
        self.b.revise(Belief('p^q'),'maxichoice')
        self.assertEqual(self.b, r)

        self.b.clear_beliefs()
        for i in ['p^q', 'r']:
            self.b.add_belief(Belief(i))
        r.clear_beliefs()
        for i in ['~p','r']:
            r.add_belief(Belief(i))
        self.b.revise(Belief('~p'),'full-meet')
        self.assertEqual(self.b, r)

if __name__ == '__main__':
    unittest.main()