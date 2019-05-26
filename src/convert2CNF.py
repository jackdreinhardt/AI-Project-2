from globals import *

class convert2CNF:
    @staticmethod
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
        
      
        print("Solve DISTRIBUTIONS:")
        prop = convert2CNF.or_over_and(prop)
        print("Transformed: " + prop)
            
# =============================================================================
#         p1= convert2CNF.convert_to_cnf("(p<->(q^r))")
#         p2= convert2CNF.convert_to_cnf("(p->r)")
#         p3= convert2CNF.convert_to_cnf("(p<->q)")
#         p4= convert2CNF.convert_to_cnf("rv(p->q)")
#         p5 = convert2CNF.convert_to_cnf(prop)
# =============================================================================
    
    @staticmethod
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
    
    @staticmethod
    def solveBiconditional(prop):
        idx = prop.find(BICONDITIONAL)
        left, middlePart, right = convert2CNF.divideSentence(prop, idx)
        middlePart = middlePart.split("<->")
        cnf = str("(" + middlePart[0] + IMPLIES + middlePart[1] + ")" + AND + "(" + middlePart[1] + IMPLIES + middlePart[0] + ")")
        prop = str(left + cnf + right)
        return prop
        
    @staticmethod
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
    
    @staticmethod
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
    
    
    @staticmethod
    def or_over_and(prop):
        while(convert2CNF.detect_distribution(prop,OR)!=-1):
            idx = convert2CNF.detect_distribution(prop,OR)
            strings = convert2CNF.divide(prop,idx,OR)
            prop = convert2CNF.distribution(strings[0],strings[1],strings[2],OR,AND)
        return prop
   
    @staticmethod
    def detect_distribution(prop, operator):
        in_clause=0
        int_operator=[]
        #add all distributions to array
        for s in range(len(prop)):
            if(in_clause <= 1 and prop[s] == operator and (prop[s-1]==')' or prop[s+1]=='(') ):
                int_operator.append(s)
        idx=-1
        last=0
        #find the distribution sign
        for op in int_operator:
            m=op-1
            openPar=0
            while(m>-1):#All characters up to thenext and sign are important
                    if(prop[m]=='('):
                        openPar+=1
                    elif(prop[m]==')'):
                        openPar-=1
                    if openPar>last:
                        idx=op
                    m-=1
            last=openPar
        return idx
    
    @staticmethod
    def divide(prop,index,operator):
        i_start =0
        i_end = len(prop)
        m=index-1
        openPar=0
        while(m>-1):#All characters up to thenext and sign are important
            if (prop[m]==(AND) or prop[m]=='(') and openPar <=0:
                i_start=m
                break
            elif(prop[m]=='('):
                openPar-=1
            elif(prop[m]==')'):
                openPar+=1
            m-=1
        m=index+1
        openPar=0
        while(m<len(prop)):#All characters up to thenext and sign are important
            if (prop[m]==(AND) or prop[m] ==')') and openPar <=0:
                i_end=m
                break
            elif(prop[m]=='('):
                openPar+=1
            elif(prop[m]==')'):
                openPar-=1
            m+=1
        #set substrubgs
        if prop[i_start]=='(':
            i_start+=1
        left= prop[:i_start]
        right= prop[i_end:]
        middlePart = prop[i_start:i_end]
        return left,middlePart,right
    
    @staticmethod
    def distribution(left,middlePart,right, op1 , op2):
        output=''
        middlePart = middlePart.replace("(","")
        middlePart = middlePart.replace(")","")
        #print(middlePart)
        if(middlePart.find(op2)==-1):
            return left+'('+middlePart+')'+right
        arguments = middlePart.split(op1,1)
        leftPart = arguments[0].split(op2)
        rightPart = arguments[1].split(op2)
        new_middle_part = ["" for x in range(len(leftPart*len(rightPart)))]
        i=0
        for p_left in leftPart:
            for p_right in rightPart:
                new_middle_part[i]='('+p_left+op1+p_right+')'
                i+=1
   #put together
        for s in range(len(new_middle_part)):
           output+=new_middle_part[s]
           if s!=len(new_middle_part)-1:
               output+=op2
        return left + output+right
            
        
        
    
    @staticmethod        
    def isCnf(prop):
        #This method checks wether the input string is already in CNF format or not
        in_clause=0 # number of parenthesis
        prop = prop[1:len(prop)-1]
        if(prop.find(BICONDITIONAL)!=-1 or prop.find(IMPLIES)!=-1):
            return False
        for s in prop :
            if(in_clause ==0 and s==OR ):
                return False
            if s=='(':
                in_clause+=1
            elif (s==')'):
                in_clause-=1
        else:
            return True
        
    @staticmethod
    def convert_to_cnf(prop):
        while prop.find(BICONDITIONAL) != -1:
            prop = convert2CNF.solveBiconditional(prop)
        while prop.find(IMPLIES) != -1:
            prop = convert2CNF.solveImplication(prop)
        for c in range(len(prop)-1):
            if prop[c] == NOT and prop[c+1] == "(":
                prop = convert2CNF.deMorgan(prop, c)
        while(convert2CNF.detect_distribution(prop,OR)):
            prop = convert2CNF.or_over_and(prop)
        return prop
