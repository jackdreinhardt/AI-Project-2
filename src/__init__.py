import sys
from collections import deque

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\nusage: python __init__.py \"Propositional Logic Statement\"\n")
    else:
        statement = sys.argv[1]

    beliefs = deque()
    
