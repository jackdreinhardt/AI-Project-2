from src.convert2CNF import convert2CNF
from src.belief_base import BeliefBase,Belief


def cnf(s):
    '''
    Takes in a string of propositional logic using the following symbols.
    AND = ^
    OR = v
    NOT = ~
    IMPLIES = ->
    BICONDITIONAL = <->

    Returns a string of propositional logic in Conjunctive Normal Form.
    '''
    return convert2CNF.CNF(s)

def belief_base(s):
    '''
    Takes in a string of propositional logic using the following symbols.
    AND = ^
    OR = v
    NOT = ~
    IMPLIES = ->
    BICONDITIONAL = <->

    Returns a BeliefBase object containing the input sentence in cnf form
    '''
    return BeliefBase(Belief(cnf(s)))

def contract(s, belief_base):
    '''
    Takes in a string s of propositional logic using the following symbols.
    AND = ^
    OR = v
    NOT = ~
    IMPLIES = ->
    BICONDITIONAL = <->

    Returns a BeliefBase object containing the input sentence in cnf form
    '''
