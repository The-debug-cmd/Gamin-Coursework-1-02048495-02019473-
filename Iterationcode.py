#Import itertools to iterate over all combinations of a list 
from itertools import combinations_with_replacement
#import numpy for imshow (display the matrix)
import numpy as np
# used for graphing
import matplotlib.pyplot as plt
# used for normal adjustment 
from scipy.stats import norm

#Initiate possibilties
Vals = range(1,10)
L = len(Vals)
itercount = 150

#A function which returns the payoff for player [value], takes a value and a List
def payoff(value, List):
    #find unique values
    Set = list(set(List))
    #Sort the vals in order (sometimes it wanted to go reverse)
    Set.sort()
    #Remember needed index
    Index = Set.index(List[value])
    adjust = norm.pdf(x = List[value],loc = 5.5,scale = 2)
    
    #if it is all the same
    if len(Set) == 1:
        return 10/List.count(List[value])
    # check if it is at the start
    elif value == 0 or Index == 0:
        # = score before, and score to next
        return  adjust * (List[value]/ List.count(List[value]) - (List[value] - Set[Index + 1 ] + 1)/(List.count(List[value]) + List.count(Set[Index + 1 ])))
    elif value == len(List) - 1 or Index == len(Set) - 1 :
        # = score to end, and score to before
        return adjust * ((L-List[value]+1)/List.count(List[value]) + (List[value] - Set[Index - 1 ] - 1)/(List.count(List[value]) + List.count(Set[Index - 1 ])))
    else:
        # score at value, score to before, score to next
        return adjust * ((List[value] - Set[max(Index - 1,0) ] - 1)/(List.count(List[value]) + 1) - (List[value] - Set[min(Index + 1, len(Set)-1) ] + 1)/(List.count(List[value]) + 1) + 1/ List.count(List[value]))

# A function that cheks if an input list is the best responce for player[value]
def Isbestresponce(value, List):
    #Make an immutable copy of the list (needed to ensure the payoff check goes well)
    copylist = tuple(List)
    #Make it a list
    copylist = list(List)
    #Make it without the element as will iterate over it
    copylist.pop(value)
    #Iterate over values the player can take
    for i in Vals:
        #Add the new value
        copylist.append(i)
        #Sort it to be used
        copylist.sort()
        #But remember the player's index
        j = copylist.index(i)
        #check if there are any cases where it is not the max
        if payoff(j,copylist) > payoff(value,List):
            #if so return the new list
            return copylist
        #Remove the Extra
        copylist.pop(j)
    # If nothing failed it must have worked ie it is true it is the best responce
    return List

def save(List):
    #count locations
    count = [List.count(j) for j in Vals]
    #convert to numpy array
    newcount = np.array(count)
    # expand dims
    newcount = np.expand_dims(newcount, axis=0)
    # set graph 
    plt.imshow(newcount, interpolation = "nearest", cmap = "BuGn")
    # save
    plt.savefig(f"output-{iter}.jpg")

#initiate iteration count
iter = 0
#initiate list
last  = [4,4,4]

for i in range(itercount):
    #increase count
    iter = iter + 1
    #iterate over players:
    for i in range(len(last)):
        #check if it is the best
        if last != Isbestresponce(i, last):
            #if it is not update + break
            last = Isbestresponce(i, last)
            break
    save(last)
