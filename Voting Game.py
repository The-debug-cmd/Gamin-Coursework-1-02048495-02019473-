#Import itertools to iterate over all combinations of a list 
from itertools import combinations_with_replacement
#import numpy for imshow (display the matrix)
import numpy as np
import matplotlib.pyplot as plt

#Max number of players EDIT
Maxplayer = 13

#Initiate possibilties
Vals = [1,2,3,4,5,6,7,8,9,10]

#A function which returns the payoff for player [value], takes a value and a List
def payoff(value, List):
    #find unique values
    Set = list(set(List))
    #Sort the vals in order (sometimes it wanted to go reverse)
    Set.sort()
    #Remember needed index
    Index = Set.index(List[value])
    
    #if it is all the same
    if len(Set) == 1:
        return 10/List.count(List[value])
    # check if it is at the start
    elif value == 0 or Index == 0:
        # = score before, and score to next
        return (List[value] - (List[value] - Set[Index + 1 ] + 1)/2)/List.count(List[value])
    elif value == len(List) - 1 or Index == len(Set) - 1 :
        # = score to end, and score to before
        return ((10-List[value]+1) + (List[value] - Set[Index - 1 ] - 1)/2)/List.count(List[value])
    else:
        # score at value, score to before, score to next
        return ((List[value] - Set[max(Index - 1,0) ] - 1)/(2) - (List[value] - Set[min(Index + 1, len(Set)-1) ] + 1)/(2) + 1)/List.count(List[value])

# A function that checks if an input list is the best responce for player[value]
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
            #if so return false
            return False
        #Remove the Extra
        copylist.pop(j)
    # If nothing failed it must have worked ie it is true it is the best responce
    return True


#takes in a List, turns a correct list length and then turns it to colour
def display(List, See = True):
    equibcount = []
    symmtros = 0
    if not(equilibriums):
        return "No Equilibriums"
    #list of counts of locations
    for i in List:
        #count
        count = [i.count(j) for j in Vals]
        #backup count
        backupcount = [i.count(j) for j in Vals]
        # reverse the count
        count.reverse()
        #check if symmetric
        if backupcount == count:
            symmtros = symmtros + 1

        #if it is not already inside
        if not(count in equibcount):
             #flip back
             count.reverse()
             equibcount.append(count)
       

    newcount = np.array(equibcount)
    a = newcount.shape
    Shape = list(a)

    if See == False:
        return newcount
    else:
        plt.imshow(newcount, interpolation = "nearest", cmap = "BuGn", extent=(0.5,Shape[1]+0.5,Shape[0]-0.5,-0.5))
        plt.xlim(0.5, 10.5)
        plt.xticks([1,2,3,4,5,6,7,8,9,10])
        plt.xlabel("Player Position")
        plt.ylabel("Equilibriums")
        plt.title(f"N = {N}", fontdict={"fontsize":20})
        plt.savefig(f"N = {N}.png")
        print(f"The number of symmetric equilibria for n = {N} is {symmtros}.")


#iterate over N 
for N in range(2, Maxplayer+1):
    #Initialise the equilibriums
    equilibriums = []
    #Iterate over suspects
    for i in combinations_with_replacement(Vals, N):
        i = list(i)
        #Assume true unless proven otherwise
        val = True
        #iterate over players
        for j in range(len(i)):
            #if player j is not a best responce:
            if not(Isbestresponce(j,i)):
                #Make it False
                val = False
                #End loop to avoid further calculations
                break
        # If still true:
        if val:
            #It is an equilibrium
            equilibriums.append(i)
    display(equilibriums)


