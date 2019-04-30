from __future__ import print_function
from collections import deque

class Belief:
    def __init__(self, cnf):
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

if __name__ == '__main__':
    b = BeliefBase()
    b1 = Belief("some stuff")
    b.add_belief(b1)
    b.show_belief_base()