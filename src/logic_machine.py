from convert2CNF import convert2CNF
from belief_base import BeliefBase,Belief

def cnf(s):
    '''Takes in a string of propositional logic using the following symbols.
    AND = ^
    OR = v
    NOT = ~
    IMPLIES = ->
    BICONDITIONAL = <->

    Returns a string of propositional logic in Conjunctive Normal Form (cnf).
    '''
    return convert2CNF.CNF(s)

def belief_base(s):
    '''Construct a belief base from a propositional logic sentence

    Takes in a string of propositional logic in cnf.
    Returns a BeliefBase object with s as the only belief
    '''
    b = BeliefBase()
    b.add_belief(Belief(s))
    return b

def entails(s, belief_base):
    '''Return true or false if s is entailed by the belief_base

    Takes in a string s of propositional logic in cnf form and a BeliefBase object
    Returns true or false if the BeliefBase object entails s
    '''
    return belief_base.entails(Belief(s).to_string())

def expand(s, belief_base):
    '''Expand the belief base to contain s

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Returns a BeliefBase object after expansion of s

    Note: Does not revise the belief base, so there may be contradictions
    '''
    belief_base.add_belief(Belief(s))

def contract(s, belief_base):
    '''Contract the sentence s from belief_base using partial meet contraction

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Returns a BeliefBase object containing the input sentence in cnf form
    '''
    belief_base.contract(Belief(s))

def revise(s, belief_base):
    '''Add the sentence s to belief_base after contracting contradictions

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Returns a BeliefBase object that has been revised by s
    '''
    belief_base.revise(Belief(s))



