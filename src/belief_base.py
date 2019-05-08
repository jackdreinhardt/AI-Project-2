from __future__ import print_function
from collections import deque
import copy

AND = '^'
OR = 'v'
NOT = '~'
IMPLIES = '->'
BICONDITIONAL = '<->'

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

    def del_positive_symbol(self, s):
        self.positives.remove(s)

    def del_negative_symbol(self, s):
        self.negatives.remove(s)

    @staticmethod
    def combine_clauses(c1, c2):
        result = Clause()
        result.positives.extend(c1.positives)
        result.positives.extend(c2.positives)
        result.negatives.extend(c1.negatives)
        result.negatives.extend(c2.negatives)
        return result

class Belief:
    def __init__(self, cnf):
        cnf = cnf.replace(" ", "")
        self.cnf = cnf
        self.clauses = []

        idx = cnf.find(AND)
        while idx > -1:
            c = cnf[:idx]
            cnf = cnf[idx+2:]
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

    def show(self):
        print(self.cnf, end='')

class BeliefBase:
    def __init__(self):
        self.d = deque()

    def add_belief(self, b):
        self.d.append(b)

    def del_belief(self, b):
        self.d.remove(b)

    def show_belief_base(self):
        print('| ', end='')
        for ele in self.d:
            ele.show()
        print(' |')

    def resolve(self, c1, c2):
        c1_copy = copy.copy(c1)
        c2_copy = copy.copy(c2)

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

    def entails(self, b):
        # method that checks if the belief base entails b using resolution

        return

    def contract(self, b):
        # uses partial meet contraction to remove belief b from the belief base
        return

if __name__ == '__main__':
    b = BeliefBase()
    b1 = Belief("(avbv~cvd)^(av~bvcvd)")
    b.add_belief(b1)
    #b.show_belief_base()

    c1 = b1.clauses[0]
    c2 = b1.clauses[1]

    print("Clauses: ")
    c1.show()
    c2.show()

    print("\nResolvent: ")
    result = b.resolve(c1,c2)
    result.show()
