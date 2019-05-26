from __future__ import print_function
from collections import deque
import copy
import time
from checkable_queue import CheckableQueue
from globals import *
from convert2CNF import convert2CNF
from functools import total_ordering



class Clause:
    def __init__(self, c=""):
        c1 = c.replace(OR, "")
        self.positives = []
        self.negatives = []

        while c1 != "":
            if c1[0] == NOT: # find all negations
                # add symbol corresponding to the negation to negatives
                self.negatives.append(c1[1])
                # remove negations and corresponding symbol from b
                c1 = c1.replace(c1[0:2], "", 1)
            else:
                # add first symbol to positives
                self.positives.append(c1[0])
                # remove first symbol from
                c1 = c1.replace(c1[0], "", 1)

    def show(self):
        str = ""
        for symbol in self.positives:
            str += symbol + OR
        for symbol in self.negatives:
            str += NOT + symbol + OR
        str = str[:len(str)-1]
        print(str)

    def to_string(self):
        str = ""
        for symbol in self.positives:
            str += symbol + OR
        for symbol in self.negatives:
            str += NOT + symbol + OR
        str = str[:len(str)-1]
        return str

    def del_positive_symbol(self, s):
        self.positives.remove(s)

    def del_negative_symbol(self, s):
        self.negatives.remove(s)

    def isEmpty(self):
        if len(self.positives) == 0 and len(self.negatives) == 0:
            return True
        return False

    @staticmethod
    def combine_clauses(c1, c2):
        result = Clause()
        result.positives.extend(c1.positives)
        result.positives.extend(c2.positives)
        result.negatives.extend(c1.negatives)
        result.negatives.extend(c2.negatives)
        return result

    @staticmethod
    def copy(c):
        result = Clause()
        for symbol in c.positives:
            result.positives.append(symbol)
        for symbol in c.negatives:
            result.negatives.append(symbol)
        return result

    @staticmethod
    def equals(c1, c2):
        if len(c1.positives) != len(c2.positives) or len(c1.negatives) != len(c2.negatives):
            return False
        for symbol1 in c1.positives: # ensure each positive symbol has a match
            match = False
            for symbol2 in c2.positives:
                if symbol1 == symbol2:
                    match = True
                    break
            if match == False:
                return False
        for symbol1 in c1.negatives: # ensure each negative symbol has a match
            match = False
            for symbol2 in c2.negatives:
                if symbol1 == symbol2:
                    match = True
                    break
            if match == False:
                return False
        return True

    @staticmethod
    def negate_clause(c):
        new_clauses = []
        for symbol in c.positives:
            new_c = Clause('~'+symbol)
            new_clauses.append(new_c)
        for symbol in c.negatives:
            new_c = Clause(symbol)
            new_clauses.append(new_c)
        return new_clauses

    @staticmethod
    def resolve(c1, c2):
        c1_copy = Clause.copy(c1)
        c2_copy = Clause.copy(c2)

        # find and remove all complements
        for c1_symbol in c1.positives:
            for c2_symbol in c2.negatives:
                # if the symbols match, remove the symbols from c1 and c2
                if c1_symbol == c2_symbol:
                    c1_copy.del_positive_symbol(c1_symbol)
                    c2_copy.del_negative_symbol(c2_symbol)
        for c2_symbol in c2.positives:
            for c1_symbol in c1.negatives:
                # if the symbols match, remove the symbols from c1 and c2
                if c2_symbol == c1_symbol:
                    c1_copy.del_negative_symbol(c1_symbol)
                    c2_copy.del_positive_symbol(c2_symbol)

        # remove redundant symbols
        for c1_symbol in c1.positives:
            for c2_symbol in c2.positives:
                # if the symbols match, remove the symbol from c2
                if c1_symbol == c2_symbol:
                    c2_copy.del_positive_symbol(c2_symbol)
        for c1_symbol in c1.negatives:
            for c2_symbol in c2.negatives:
                # if the symbols match, remove the symbol from c2
                if c1_symbol == c2_symbol:
                    c2_copy.del_negative_symbol(c2_symbol)

        resolvent = Clause.combine_clauses(c1_copy, c2_copy)

        # return the resolvent
        return resolvent

class Belief:
    def __init__(self, cnf, negate=False):
        cnf = cnf.replace(" ", "")
        cnf = cnf.replace("~~", "") # eliminate any double negations
        self.clauses = []

        if negate == False:
            idx = cnf.find(AND)
            while idx > -1:
                c = cnf[:idx]
                cnf = cnf[idx+1:]
                c = c.replace("(", "")
                c = c.replace(")", "")
                clause = Clause(c)
                self.clauses.append(clause)
                idx = cnf.find(AND)
            c = cnf
            c = c.replace("(", "")
            c = c.replace(")", "")
            clause = Clause(c)
            self.clauses.append(clause)

        else:
            temp_clauses = []
            idx = cnf.find(AND)
            while idx > -1:
                c = cnf[:idx]
                cnf = cnf[idx+1:]
                c = c.replace("(", "")
                c = c.replace(")", "")
                clause = Clause(c)
                temp_clauses.append(clause)
                idx = cnf.find(AND)
            c = cnf
            c = c.replace("(", "")
            c = c.replace(")", "")
            clause = Clause(c)
            temp_clauses.append(clause)

            # negate each clause
            negated_clauses = []
            for c in temp_clauses:
                result = Clause.negate_clause(c)
                negated_clauses.append(result)

            # distribute to return to cnf
            while(len(negated_clauses) > 1):
                clause_set1 = negated_clauses[0]
                clause_set2 = negated_clauses[1]
                new_clauses = []
                for c1 in clause_set1:
                    for c2 in clause_set2:
                        new_c = Clause.combine_clauses(c1, c2)
                        new_clauses.append(new_c)
                negated_clauses[0] = new_clauses
                del(negated_clauses[1])

            for c in negated_clauses[0]:
                self.clauses.append(c)

    # not a legitimate ordering, working on a nontrivial implementation
    def __lt__(self, item):
        slen = 0; ilen = 0;
        for s,i in zip(self.clauses,item.clauses):
            slen += len(s.positives) + len(s.negatives)
            ilen += len(i.positives) + len(i.negatives)
        return slen < ilen

    # not a legitimate ordering, working on a nontrivial implementation
    def __eq__(self, item):
        slen = 0; ilen = 0;
        for s,i in zip(self.clauses,item.clauses):
            slen += len(s.positives) + len(s.negatives)
            ilen += len(i.positives) + len(i.negatives)
        return slen == ilen


    def show(self):
        total_str = ''
        for c in self.clauses:
            str = '(' + c.to_string() + ")^"
            total_str += str
        total_str = total_str[:len(total_str)-1]
        print(total_str)

    def to_string(self):
        total_str = ''
        for c in self.clauses:
            str = '(' + c.to_string() + ")^"
            total_str += str
        total_str = total_str[:len(total_str)-1]
        return total_str

class BeliefBase:
    def __init__(self):
        self.beliefs = []
        self.entrenchment = 0

    def __eq__(self, item):
        for sb,ib in zip(self.beliefs, item.beliefs):
            for sbc,ibc in zip(sb.clauses,ib.clauses):
                if not Clause.equals(sbc, ibc):
                    return False
        return True

    def add_belief(self, b):
        self.beliefs.append(b)

    def del_belief(self, b):
        for belief in self.beliefs:
            same_belief = True
            for c1,c2 in zip(belief.clauses,b.clauses):
                if not Clause.equals(c1,c2):
                    same_belief = False
            if same_belief:
                self.beliefs.remove(belief)

            

    def show_belief_base(self):
        for ele in self.beliefs:
            ele.show()

    def entails(self, belief):
        # belief is a string
        # method that checks if the belief base entails b using resolution
        new_b = Belief(belief, True) # create negation of the belief

        # create a list containing all clauses in KB ^ ~belief
        all_clauses = []
        resolved_clauses = []
        all_clauses.extend(new_b.clauses)
        for b in self.beliefs:
            all_clauses.extend(b.clauses)

        clause_added = True
        while(clause_added): # loop until a clause can no longer be added
            clause_added = False
            for c1 in all_clauses:
                for c2 in all_clauses:
                    if not Clause.equals(c1, c2) and (c1,c2) not in resolved_clauses:
                    # if c1 and c2 are not equal and have not already been resolved
                        result = Clause.resolve(c1, c2) # resolve c1 and c2
                        if result.isEmpty(): # if the resolvent is empty
                            return True # then the KB entails the belief

                        # add resolvent if it is unique
                        add_clause = True
                        for c3 in all_clauses:
                            if Clause.equals(result, c3):
                                add_clause = False
                        if add_clause:
                            clause_added = True
                            all_clauses.append(result)
                            resolved_clauses.append((c1,c2))
        return False        


    def contract(self, b):
        '''
        Implements partial meet contraction using the ordering defined in the belief class
        This ordering satisfies the postulates for epistemic entrenchment.
        
        1. the belief base is flattened, so each belief contains one clause
        2. the beliefs in the belief base are sorted and given a entrenchment rank
            2.a. entrenchment rank increases with the square (cubed?) root,
                 therefore, more entrenched beliefs are valued higher
        3. maximize the entrenchment value (search problem?) of the intersected solutions
        '''
        self.flatten()
        self.beliefs = self.remainders(b)[0].beliefs
        # self.show_belief_base()
        self.beliefs.sort()
        # self.show_belief_base()

    def remainders(self, b):
        '''
        Returns all remainders when introducing belief b into the belief base.
        Flattens the clauses so that each belief contains one clause

        "Backward Clause Selection" - Jacob
        frontier = initial belief base
        loop do
            if frontier empty then return the empty set
            choose belief base n from frontier
            remove belief base n from frontier
            add belief base n to expanded
            if n does not entail b, then return solution
            for each belief m in belief base n
                n' = copy of belief base n with m removed
                if n' not in frontier and n' not in expanded
                    add n' to frontier
        '''
        self.flatten()
        frontier = CheckableQueue()
        frontier.put(self)
        expanded = CheckableQueue()
        remainders = []
        while True:
            if frontier.empty():
                remainders.append(BeliefBase()) # failure case
                return remainders
            n = frontier.get()
            expanded.put(n)
            if not n.entails(b.to_string()):
                remainders.append(n)
            for belief_one_clause in n.beliefs:
                n_copy = copy.deepcopy(n)
                n_copy.del_belief(belief_one_clause)
                if n_copy not in frontier and n_copy not in expanded:
                    frontier.put(n_copy)

    def flatten(self):
        belief = []
        for b in self.beliefs:
            for c in b.clauses:
                belief.append(Belief(c.to_string()))
        self.beliefs = belief

    def revision(self, b):
        b_not = Belief(b.to_string(),negate=True)
        self.contract(b_not)
        self.add_belief(b)


if __name__ == '__main__':
    b = BeliefBase()
    b1 = Belief("(avbv~cvd)^g")
    b2 = Belief("(av~bvcvd)")
    b.add_belief(b1)
    b.add_belief(b2)

    print("Belief Base:")
    b.show_belief_base()

    c1 = b1.clauses[0]
    c2 = b1.clauses[1]

    print("\nClauses: ")
    for belief in b.beliefs:
        for c in belief.clauses:
            c.show()

    eq = Clause.equals(c1, c2)
    print("Are the clauses equal? " + str(eq))

    print("\nResolvent of clause 1 and clause 2: ")
    result = Clause.resolve(c1,c2)
    result.show()

    empty = result.isEmpty()
    print("Is the resolvent empty? " + str(empty))

    belief = "a^b"
    entails = b.entails(belief)
    print("\nDoes the KB ential " + belief + "? " + str(entails))

    b_c = BeliefBase()
    b1 = Belief("p")
    b2 = Belief("~qvp")
    b3 = Belief("r")
    b4 = Belief("p^q")
    b_c.add_belief(b1)
    b_c.add_belief(b2)
    b_c.add_belief(b3)
    b_c.contract(b4)
    b_c.show_belief_base()
    
    
    prop = str(input("Please enter a sentence in propositional logic: "))
    #prop = "(" + prop + ")"
    cnf = convert2CNF.CNF(prop)

    #### Tests ####
    #a^((p^q)<->r)
    #~(p^q)
    #a^(~((p^q)vb)vc
    #(a^b)v(c^d)v(e->f)
