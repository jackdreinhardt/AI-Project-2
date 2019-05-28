import unittest
from belief_revision_engine import cnf,belief_base,entails,expand,contract,revise

# to run the tests:
# python -m unittest test_logic_machine.py -v

class TestLogicMachine(unittest.TestCase):
    def test_cnf(self):
        self.assertEqual(cnf('p^q'),'(p^q)')

    # tests the entails function
    def test_entails(self):
        b = belief_base('p')
        self.assertTrue(entails(b, 'p'))
        self.assertFalse(entails(b, 'q'))
        expand(b, 'q')
        self.assertTrue(entails(b, 'p^q'))
        expand(b,'r')
        self.assertFalse(entails(b, '(r^~p)'))
        self.assertTrue(entails(b, 'p^q^r^(~rvp)')) # raises error due to remove function

    def test_contraction(self):
        b = belief_base()
        for i in ['p', 'q', 'r']:
            expand(b, i)
        r = belief_base()
        expand(r, 'r')
        contract(b, 'p^q','full-meet')
        self.assertEqual(b, r)

        b = belief_base()
        for i in ['p', 'q', '~pvr','r']:
            expand(b, i)
        r = belief_base()
        for i in ['q', 'rv~p']:
            expand(r, i)
        contract(b, 'r','maxichoice')
        self.assertEqual(b, r)

        b = belief_base()
        for i in ['p', 'q', '~pvr','r']:
            expand(b, i)
        r = belief_base()
        for i in ['q', 'rv~p']:
            expand(r, i)
        contract(b, 'r','partial-meet')

    def test_revision(self):
        b = belief_base()
        for i in ['p', 'q', 'r']:
            expand(b, i)
        r = belief_base()
        for i in ['p', 'q', 'r','p^q']:
            expand(r, i)
        revise(b, 'p^q', 'maxichoice')
        self.assertEqual(b, r)

        b = belief_base()
        for i in ['p^q', 'r']:
            expand(b, i)
        r = belief_base()
        for i in ['~p','r']:
            expand(r, i)
        revise(b, '~p','full-meet')
        self.assertEqual(b, r)

if __name__ == '__main__':
    unittest.main()