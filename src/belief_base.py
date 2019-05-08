from __future__ import print_function
from collections import deque

AND = '^'
OR = 'v'
NOT = '~'
IMPLIES = '->'
BICONDITIONAL = '<->'

class Belief:
    def __init__(self, cnf):
        cnf = cnf.replace(" ", "")
        self.cnf = cnf

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
        # assume c1 and c2 only are each a single clause from a sentence in CNF
        c1_copy = c1
        c2_copy = c2
        c1 = c1.replace(OR, "")
        c2 = c2.replace(OR, "")

        c1_positives = []
        c1_negatives = []
        c2_positives = []
        c2_negatives = []

        while c1 != "":
            if c1[0] == NOT: # find all negations
                # add symbol corresponding to the negation to negatives
                c1_negatives.append(c1[1])
                # remove negations and corresponding symbol from b
                c1 = c1.replace(c1[0:2], "", 1)
            else:
                # add first symbol to positives
                c1_positives.append(c1[0])
                # remove first symbol from
                c1 = c1.replace(c1[0], "", 1)

        while c2 != "":
            if c2[0] == NOT: # find all negations
                # add symbol corresponding to the negation to negatives
                c2_negatives.append(c2[1])
                # remove negations and corresponding symbol from b
                c2 = c2.replace(c2[0:2], "", 1)
            else:
                # add first symbol to positives
                c2_positives.append(c2[0])
                # remove first symbol from
                c2 = c2.replace(c2[0], "", 1)

        # find all complements
        complements = []
        for c1_symbol in c1_positives:
            for c2_symbol in c2_negatives:
                # if the symbols match, remove the symbols from c1 and c2
                if c1_symbol == c2_symbol:
                    c1_copy = c1_copy.replace(c1_symbol, "", 1)
                    c2_copy = c2_copy.replace(NOT+c2_symbol, "", 1)
        for c2_symbol in c2_positives:
            for c1_symbol in c1_negatives:
                # if the symbols match, remove the symbols from c1 and c2
                if c2_symbol == c1_symbol:
                    c2_copy = c2_copy.replace(c2_symbol, "", 1)
                    c1_copy = c1_copy.replace(NOT+c1_symbol, "", 1)

        # remove redundant symbols
        for c1_symbol in c1_positives:
            for c2_symbol in c2_positives:
                # if the symbols match, remove the symbol from c2
                if c1_symbol == c2_symbol:
                    c2_copy = c2_copy.replace(c2_symbol, "", 1)
        for c1_symbol in c1_negatives:
            for c2_symbol in c2_negatives:
                # if the symbols match, remove the symbol from c2
                if c1_symbol == c2_symbol:
                    c2_copy = c2_copy.replace(NOT+c2_symbol, "", 1)

        resolvent = ""
        if c1_copy == "" or c2_copy == "":
            resolvent = c1_copy + c2_copy
        else:
            resolvent = c1_copy + OR + c2_copy

        idx = resolvent.find(OR+OR)
        while idx > -1:
            resolvent = resolvent.replace(OR+OR, OR)
            idx = resolvent.find(OR+OR)

        if resolvent[len(resolvent)-1] == OR:
            resolvent = resolvent[:len(resolvent)-1]

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
    b1 = Belief("c^a^b")
    b.add_belief(b1)
    #b.show_belief_base()

    c1 = "avbv~cvd"
    c2 = "av~bvcvd"
    result = b.resolve(c1,c2)
    print(result)
