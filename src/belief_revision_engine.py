from convert2CNF import convert2CNF
from belief_base import BeliefBase,Belief

def cnf(s):
    '''Takes in a string of propositional logic and returns the same string in cnf

    Valid propositional logic operators:
    AND = ^
    OR = v
    NOT = ~
    IMPLIES = ->
    BICONDITIONAL = <->

    Returns a string of propositional logic in Conjunctive Normal Form (cnf)
    '''
    return convert2CNF.CNF(s)

def belief_base(s=''):
    '''Construct a belief base from a propositional logic sentence

    Optional: takes in a string of propositional logic in cnf
        if this is omitted, an empty belief base will be constructed
    Returns a BeliefBase object
    '''
    b = BeliefBase()
    if s != '':
        b.add_belief(Belief(s))
    return b

def entails(belief_base, s):
    '''Return true or false if s is entailed by the belief_base

    Takes in a string s of propositional logic in cnf form and a BeliefBase object
    Returns true or false if the BeliefBase object entails s
    '''
    return belief_base.entails(str(Belief(s)))

def expand(belief_base, s):
    '''Expand the belief base to contain s

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Expands the beleif base object, returns None

    Note: Does not revise the belief base, so there may be contradictions that result
    '''
    belief_base.add_belief(Belief(s))

def contract(belief_base, s, mode='partial-meet'):
    '''Contract the sentence s from belief_base using the specified mode

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Optional: define a mode (partial-meet, full-meet, maxichoice)
    Contracts the BeliefBase object with the appropriate contraction performed, returns None
    '''
    belief_base.contract(Belief(s), mode)

def revise(belief_base, s, mode='partial-meet'):
    '''Add the sentence s to belief_base after contracting contradictions

    Takes in a string s of propositional logic in cnf and a BeliefBase object
    Optional: define a mode for contraction (partial-meet, full-meet, maxichoice)
    Revises the BeliefBase object, returns None
    '''
    belief_base.revise(Belief(s), mode)
