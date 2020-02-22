##Jeremy Vidaurri
##10/18/2019
##Project 2 - Maze Solver

##Algorithm/Pseudocode
##  Ask the user for input containing a maze
##      If file is blank, error
##      If file has invalid characters, error
##  Assign the maze to a list of lists containing each row
##      For every line, make every character an individual string and each line as a separate list within a list.
##  Set the starting position to the "S"
##      Find this by searching each row and seeing if any element within it equals "S"
##      If file has no S, error
##  Set the ending position to the "E"
##      Find this position by searching each row and seeing if any element within it equals "E"
##      If file has no E, error
##  Print the maze
##      Use join() to convert lists to strings
##      Use "/n" after printing the maze
##  As long as the position is not the final position, run a function to solve the maze
##      Make sure no where around the current position is out of bounds
##      Check in a counterclockwise fashion if there are any blank spots, if so, move there.
##      If there are no spots, work backwards.
##      If at anytime a new blank spot appears, go there.
##      If no where to go, might need to cross S again and check in a counterclockwise fashion
##      If still no where to go, check if there is another "S"
##          Remove the previous S and look for another "S"
##          If no more "S", return original "S" and no solution
##  After running the solve function, print the new iteration of the maze
##  Loop this until maze hits the "E"
##      If maze has no where to go, no solution
##  Remove any extra "S"

def main(userFile):
    ##Open the Maze file and append it into a list of list of strings
    #userFile = input("Enter the name of a file containing a maze: ").strip()
    myFile = open(userFile,"r")

    mazeList = []
    for i in myFile:
        i = i.strip("\n")
        newList = []
        for x in i:
            newList.append(x)
        mazeList.append(newList)    ##Make every line an individual string and add it to a list. Every line is a separate list
    myFile.close()
    
    mazeList[0] ##If this returns error, there is no maze
    isValidMaze(mazeList)   ##Check all characters are valid

    positionX, positionY = findStart(mazeList)  #Find the "S"
    endPositionX, endPositionY = findEnd(mazeList)  #Find the "E"
    
    S_count = 0
    for i in mazeList:
        S_count += i.count("S") ##Add up the amount of "S" in the maze
 
    while positionX != endPositionX or positionY != endPositionY:   #If the position doesn't match the position of the "E", continue
        prevX,prevY= positionX,positionY
        mazeList, positionX, positionY  = mazeSolver(mazeList,positionX,positionY)
        mazePrint(mazeList) #Print the maze after each step
        if prevX == positionX and prevY == positionY and S_count !=1:
            mazeList[positionY][positionX] = "."
            positionX,positionY = findStart(mazeList)   ##See if we can find a new "S"
            S_count -= 1    ##Every time a new "S" is attempted, remove 1 from S_count
        elif prevX == positionX and prevY == positionY:
            1/0     ##If not, no solution and raise a zerodiv error
    
    if S_count != 1:
        removeExtraS(mazeList)  ##Delete any unnecessary "S"
        mazePrint(mazeList)
        
            
def isValidMaze(mazeList):
    for i in mazeList:
        for x in i:
            if x != "#" and x != " " and x!="S" and x!="E":
                print("Error: Maze contains invalid characters. Line %s contains invalid character '%s'"%(mazeList.index(i),x))
                raise AssertionError    ##Invalid Character Error
        
def findStart(mazeList):
    positionY = 0
    for row in mazeList:
        for i in row:             
            if i == "S": #Check to see if any part of the list has the "S" and mark it
                return row.index("S"), positionY    ##If none, no start position
        positionY +=1

def findEnd(mazeList):
    positionY = 0
    for row in mazeList:
        for i in row:             
            if i == "E":   #Check to see if any part of the list has the "E" and mark it down
                return row.index("E"), positionY
        positionY +=1
    if row.index("E")==None:
        raise ValueError    ##No end position
    
def removeExtraS(mazeList):
    positionY = 0
    necStartX,necStartY = findStart(mazeList) ##Assign the current start as necessary position
    mazeList[necStartY][necStartX] = " "    ##Set it to blank so we don't index the same start
    for row in mazeList:
        for i in row:
            if i == "S":
                if necStartX != row.index("S") or necStartY != positionY:
                    mazeList[positionY][row.index("S")] = " "   ##Erase any new found "S"
        positionY +=1
    mazeList[necStartY][necStartX] = "S"    ##Put the necessary "S" back

def mazePrint(mazeList):
    printOutput = ""
    for line in mazeList:
        printOutput += "".join(line) + "\n"
    print(printOutput)

def mazeSolver(mazeList,positionX,positionY):
    ##Check if every spot around the current position is out of bounds _ is the negative direction
    outOfBoundsX,outOfBound_X,outOfBoundsY,outOfBound_Y = outOfBoundsRight(positionX,positionY,mazeList),outOfBoundsLeft(positionX,positionY,mazeList),outOfBoundsDown(positionX,positionY,mazeList),outOfBoundsUp(positionX,positionY,mazeList)

    ##Check what spot is blank after the start
    if mazeList[positionY][positionX] == "S":
        if outOfBound_X and mazeList[positionY][positionX-1] == " ":
            positionX -= 1
        elif outOfBoundsY and mazeList[positionY+1][positionX] == " ":
            positionY += 1
        elif outOfBoundsX and mazeList[positionY][positionX+1] == " ":
            positionX += 1
        elif outOfBound_Y and mazeList[positionY-1][positionX] == " ":
            positionY -= 1

    ##Check if we reached the end or if there are any blank spots in a counterclockwise fashion
    elif (outOfBound_X) and (mazeList[positionY][positionX-1] == " " or mazeList[positionY][positionX-1] == "E"):
        mazeList[positionY][positionX] = "<"
        positionX -= 1
    elif (outOfBoundsY) and (mazeList[positionY+1][positionX] == " " or mazeList[positionY+1][positionX] =="E"):
        mazeList[positionY][positionX] = "v"
        positionY += 1
    elif (outOfBoundsX) and (mazeList[positionY][positionX+1] == " " or mazeList[positionY][positionX+1] =="E"):
        mazeList[positionY][positionX] = ">"    
        positionX += 1
    elif (outOfBound_Y) and (mazeList[positionY-1][positionX] == " " or mazeList[positionY-1][positionX] =="E"):
        mazeList[positionY][positionX] = "^"
        positionY -= 1

    ##Check if we must go back in a counterclockwise fashion or  if we have to cross the start
    elif (outOfBoundsX) and (mazeList[positionY][positionX+1]=="<" or mazeList[positionY][positionX+1] =="S"):
        mazeList[positionY][positionX] = "."
        positionX += 1
    elif (outOfBound_Y) and (mazeList[positionY-1][positionX]=="v" or mazeList[positionY-1][positionX] =="S"):
        mazeList[positionY][positionX] = "."
        positionY -= 1
    elif (outOfBound_X) and (mazeList[positionY][positionX-1]==">" or mazeList[positionY][positionX-1] == "S"):
        mazeList[positionY][positionX] = "."
        positionX -= 1
    elif (outOfBoundsY) and (mazeList[positionY+1][positionX]=="^" or mazeList[positionY+1][positionX] =="S"):
        mazeList[positionY][positionX] = "."
        positionY += 1
    
    return mazeList,positionX,positionY

def outOfBoundsRight(positionX,positionY,mazeList):
    if len(mazeList[positionY]) > positionX +1:
        return True
    else:
        return False
def outOfBoundsLeft(positionX,positionY,mazeList):
    if 0 <= positionX -1:
        return True
    else:
        return False
    
def outOfBoundsDown(positionX,positionY,mazeList):
    try:
        mazeList[positionY + 1][positionX]
        return True
    except IndexError:
        return False
def outOfBoundsUp(positionX,positionY,mazeList):
    try:
        mazeList[positionY - 1][positionX]
        if positionY-1 != -1:   #Make sure that a spot upwards exists and that it isn't wrapping back to the bottom
            return True
        else:
            return False
    except IndexError:
        return False
try:
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec1-1.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec1-2.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec2-2.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec3-1.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec3-2.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec4-1.dat")
    main("C:/Users/jervi/Desktop/School Work/Fall 2019/Programming Principles/Programs/Projects/Project_2_Test_Mazes/ec4-2.dat")
except AssertionError:  ##In isValidMaze()
    pass
except ZeroDivisionError:   ##No solution
    print("Error: No route could be found from start to end. Maze unsolvable.")
except IndexError:  ##Can't index the first position so no maze
    print("Error: Specified file contains no maze.")
except TypeError:   ##No S returned
    print("Error: No start position found.")
except ValueError:  ##No E returned
    print("Error: No end position found.")
except FileNotFoundError:   ##File not found
    print("Error: Specified file does not exist.")





