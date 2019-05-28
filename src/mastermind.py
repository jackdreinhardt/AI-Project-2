from belief_revision_engine import cnf,belief_base

red = ["a","b","c","d"]
green = ["e","f","g","h"]
yellow = ["i","j","k","l"]
blue = ["m","n","o","p"]


def build_belief_base():
    # There must be one color in each position
    belief_base(red[0] + "v" + green[0] + "v" + yellow[0] + "v" + blue[0])
    belief_base(red[1] + "v" + green[1] + "v" + yellow[1] + "v" + blue[1])
    belief_base(red[2] + "v" + green[2] + "v" + yellow[2] + "v" + blue[2])
    belief_base(red[3] + "v" + green[3] + "v" + yellow[3] + "v" + blue[3])
    
    # There can only be one color in each position
    belief_base()

def input2coding(userInput):
    code = [0,0,0,0]
    for element in range(len(userInput)):
        if userInput[element] == "r":
            code[element] = red[element]
    for element in range(len(userInput)):
        if userInput[element] == "g":
            code[element] = green[element]
    for element in range(len(userInput)):
        if userInput[element] == "y":
            code[element] = yellow[element]
    for element in range(len(userInput)):
        if userInput[element] == "b":
            code[element] = blue[element]
    #solution = str(solution[0] + "^" + solution[1] + "^" + solution[2] + "^" + solution[3])
    return code

def compareGuess(guess, solution):
    correctColor = 0
    correct = 0
    for index in range(len(guess)):
        if guess[index] in solution:
            correctColor += 1
        if guess[index] == solution[index]:
            correctColor -= 1
            correct += 1
    return correctColor, correct

def createBelief(correctColor, correct, guess):
    beliefs = []
    

print("Choose from these colors: \nred (r), green (g), yellow (y), blue (b)")

solution = list(input("Enter your secrect four digit code with unique colors (e.g.: gbyr): "))

#build_belief_base()
solutionCode = input2coding(solution)

guess = ["y","b","r","g"]
guessCode = input2coding(guess)
correctColor, correct = compareGuess(guess, solution)
print(correctColor, correct)


