from globals import *

class convert2CNF:
    
    def CNF(prop):
        while prop.find(BICONDITIONAL) != -1:
            print("Solve BICONDITIONAL:")
            prop = convert2CNF.solveBiconditional(prop)
            print("Transformed: " + prop)
        while prop.find(IMPLIES) != -1:
            print("Solve IMPLICATION:")
            prop = convert2CNF.solveImplication(prop)
            print("Transformed: " + prop)
# =============================================================================
#     for c in range(len(prop)-1):
#         if prop[c] == NOT and prop[c+1] == "(":
#             print("Solve DEMORGAN")
#             prop = convert2CNF.deMorgan(prop, c)
#             print("Transformed: " + prop)
# =============================================================================
        for c in range(len(prop)-1):
            if prop[c] == NOT and prop[c+1] == "(":
                print("Solve DEMORGAN:")
                prop = convert2CNF.deMorgan(prop, c)
                print("Transformed: " + prop)
    
    
    def divideSentence(prop, idx):
        op_position = idx
        openPar = 1
        if idx != -1:
            while idx >= 0:
                idx -= 1
                if prop[idx] == "(":
                    openPar -= 1
                    if openPar == 0:
                        left = prop[0:idx]
                        middleStart = idx
                        break
                if prop[idx] == ")":
                    openPar += 1
                    
            idx = op_position
            openPar = 1
            while idx < len(prop)-1:
                idx += 1
                if prop[idx] == ")":
                    openPar -= 1
                    if openPar == 0:
                        right = prop[idx+1:len(prop)]
                        middleEnd = idx
                        break
                if prop[idx] == "(":
                    openPar += 1
                    
            middlePart = prop[middleStart+1:middleEnd]
        return left, middlePart, right
    
    
    def solveBiconditional(prop):
        idx = prop.find(BICONDITIONAL)
        left, middlePart, right = convert2CNF.divideSentence(prop, idx)
        middlePart = middlePart.split("<->")
        cnf = str("(" + middlePart[0] + IMPLIES + middlePart[1] + ")" + AND + "(" + middlePart[1] + IMPLIES + middlePart[0] + ")")
        prop = str(left + cnf + right)
        return prop
        
          
    def solveImplication(prop):
        idx = prop.find(IMPLIES)
        left, middlePart, right = convert2CNF.divideSentence(prop, idx)
        middlePart = middlePart.split("->")
        cnf = str("(" + NOT + middlePart[0] + OR + middlePart[1] + ")")
        prop = left + cnf + right
        return prop
            
# =============================================================================
#     def deMorgan(prop, c):
#         left, middlePart, right = convert2CNF.divideSentence(prop, c+1)
#         print("left = " + left)
#         print("middlePart = " + middlePart)
#         print("right = " + right)
#         idx = 2
#         openPar = 0
#         while idx <= len(middlePart):
#             if middlePart[idx] == "(":
#                 openPar += 1
#             elif middlePart[idx] == ")":
#                 openPar -= 1
#             if openPar == 0:
#                 if middlePart[idx] == AND:
#                     leftString = middlePart[2:idx]
#                     print("leftString: " + leftString)
#                     rightString = middlePart[idx+1:len(middlePart)]
#                     print("rightString: " + rightString)
#                     middlePart = NOT + leftString + OR + NOT + rightString
#                     break
#                 elif middlePart[idx] == OR:
#                     leftString = middlePart[2:idx]
#                     print("leftString: " + leftString)
#                     rightString = middlePart[idx+1:len(middlePart)]
#                     print("rightString: " + rightString)
#                     middlePart = NOT + leftString + AND + NOT + rightString
#                     break
#             idx += 1
#         prop = left + "((" + middlePart + ")" + right
#         return prop
# =============================================================================
    
    def deMorgan(prop, idx):
        prop = list(prop)
        del prop[idx]
        openPar = -1
        while idx <= len(prop):
            if prop[idx] == "(":
                openPar += 1
            elif prop[idx] == ")":
                openPar -= 1
            elif openPar == 0:
                if prop[idx] == AND:
                    prop[idx] = OR
                elif prop[idx] == OR:
                    prop[idx] = AND
                else:
                    prop.insert(idx, NOT)
                    idx += 1
            if openPar == -1:
                break
            idx += 1
        prop = "".join(prop)
        return prop
