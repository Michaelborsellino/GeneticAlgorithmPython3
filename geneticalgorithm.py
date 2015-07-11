#!python3
import random
#Setting up some constants for easy comparison later on. These are all possible bitstrings
compare = {'0000':0,'0001':1,'0010':2,'0011':3,'0100':4,
           '0101':5,'0110':6,'0111':7,'1000':8,'1001':9,
           '1010':'+', '1011':'-', '1100':'*', '1101':'/'}
comparerev = {0:'0000',1:'0001',2:'0010',3:'0011',4:'0100',
           5:'0101',6:'0110',7:'0111',8:'1000',9:'1001',
           10:'1010', 11:'1011', 12:'1100', 13:'1101'}

#This Function converts the 36 character bit string into legal human readable function
#This step isn't explicitly nessecary and can simply be merged into the Evaluate step later on.
#I like it for testing purposes.
#What is considered a legal function:
# - Function must be a repeating sequence of single character operands and operators
#   e.g 1 + 5 - 3
# - In the case of multiple character operands or operators, the function is 'Fixed' by only taking
#   the first.
#   e.g 11 +- 23 becomes 1 + 2
# - In a case where the last character of a function after 'fixing' is an operator, the list simply pops it
def convert(instring):
    splitlist = list()
    even = True

    #This for loop increments by steps of 4 to prevent accidental overlap when splitting up the bitstring into its 4 character pieces
    for x in range(0,36,4):
        if instring[x:x+4] in compare:
            #On an even step (0, 2, etc) The function only adds the converted bitstring if it is an operand
            #it verifies by checking the dictionaries I set above. 
            #3 Cases
            # -The string slice is in the bitstring->Human Readable (BS->HR) and the HR is in the HR->BS, slice represents an operand
            # -The string slice is in the bitstring->Human Readable (BS->HR) and the HR is NOT in the HR->BS, slice represents an operator
            # -The string slice is NOT in the bitstring->Human Readable(BS->HR) Therefore it is an invalid sequence and is simply ignored
            if even == True:
                if compare[instring[x:x+4]] in comparerev:
                    splitlist.append(compare[instring[x:x+4]])
                    even = False
            else:
                if compare[instring[x:x+4]] not in comparerev:
                    splitlist.append(compare[instring[x:x+4]])
                    even = True
    #This checks for an operator at the end of a function(to pop, and also, checks for functions that are altogether invalid.
    #If the function is altogether invalid e.g. started off as -+++--*/+ or something, and now the list is empty, the fitness
    #automatically becomes -9999 to give it as little a chance as possible to reproduce
    try:
        if splitlist[len(splitlist)-1] not in comparerev:
            splitlist.pop()
    except IndexError:
        return -9999
    
    print(splitlist)
    #This is where the result of the function is evaluated
    total = evaluate(splitlist)
    print(total)
    #If the evaluate function shows the string to have a divide by zero error it is also considered something undesirable and
    #is given an extremely low fitness
    if total == 10000:
        return -9999
    #This is a super simple fitness function
    try:
        fitness = float(1 / (total - 23))
    #If this triggers, you have your answer! returns 1000 as a marker
    except ZeroDivisionError: 
        return 1000
    #Otherwise the function just returns the fitness of the string
    else:
        return abs(fitness)
    
#creating a simple calculator evaluator
def evaluate(formula):
    total = formula[0]
    if len(formula) == 1:
        return formula[0]
    else:
        for x in range(1,len(formula),2):
            if formula[x] == '+':
                total += formula[x+1]
            elif formula[x] == '-':
                total -= formula[x+1]
            elif formula[x] == '*':
                total *= formula[x+1]
            elif formula[x] == '/':
                try:
                    total /= formula[x+1]
                except ZeroDivisionError:
                    print(formula)
                    return 10000
    return total
#And here is what makes this program genetic!
def breed(inList):
    #print(inList)
    breedList = list(list())
    mutationFactor = 0.6
    crossoverRate = 6
    for x in range(0,len(inList)):
        swaplist = list(list())
        #fortestingswaplist = list()
        #Here we select which two bitstrings get to breed on each run
        for p in range(2):
            while True:
                #First, we randomly select a bitstring from the population
                current = list()
                current = inList[random.randint(0,len(inList)-1)]
                print(current)
                #Now we use Stochastic Acceptance to decide if the bitstring gets to reproduce. 
                #The higher the fitness, the better the chance.
                if random.random() <= current[1]:
                    #Strings in Python are immutable, so for easy breeding I convert the string to a list and push that
                    swaplist.append(list(current[0]))
                    #fortestingswaplist.append(current[0])
                    break
        #print(fortestingswaplist)
        #Now we randomly breed bits from the point dictated in the crossover rate based on the mutation factor
        for p in range(crossoverRate,len(swaplist[0])):
            if random.random() >= mutationFactor:
                swaplist[0][p],swaplist[1][p] = swaplist[1][p],swaplist[0][p]
        #Then we package everything nicely for the next round
        tempList = list()
        tempList.append(''.join(swaplist[0]))
        breedList.append(tempList)
        tempList2 = list()
        tempList2.append(''.join(swaplist[1]))
        breedList.append(tempList2)
        
    #print(breedList)
    return breedList
    
    
            
            

genpop = list(list())
'''
#Creating initial population
for p in range(20):
    internal = list()
    temp = ''
    for x in range(36):
        temp += str(random.randint(0,1))
    internal.append(temp)
    #print(temp)
    result = convert(temp)
    if result == 1000:
        print('Success!')
        break
    internal.append(result)
    genpop.append(internal)
breed(genpop)
#print(genpop)
'''
#And here is the main function area. Basically separated into the initial population creation and the main driver
#create initial list
for p in range(200):
    initial = list()
    temp = ''
    for x in range(36):
        temp += str(random.randint(0,1))
    initial.append(temp)
    genpop.append(initial)
#print(genpop)
unSolved = True
#continue until solved

#start up the cycle
while unSolved:
    result = 0
    for d in range(0,len(genpop)):
        result = convert(genpop[d][0])
        #print(result)
        if result == 1000:
            print('Success!')
            print(genpop[d])
            unSolved = False
            break
        genpop[d].append(result)
    if unSolved == False:
        break
    #print(genpop)
    
    #print(genpop)
    genpop= breed(genpop)
    
    #print(temp)

