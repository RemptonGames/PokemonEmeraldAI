#!/usr/bin/python

import retro
import time
import random 

class MapMaker:     

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        #char in map entry keeps track of type of square
        # '?' is an unknown square, 'P' is the player's current position, 'W' is a warp 
        # 'B' is a 'block' - impassible square, "D" means sign or sprite (opens dialogue box when clicked)
        # 'S' is a 'safe' square - player can move on it freely
        self.map1 = [["?","?","?"],["?","P", "?"],["?","?","?"]]
        self.mapList = [self.map1]
        self.currentMap = self.map1
        self.portals = []
        self.direction = "NONE"
        self.prevX = 0
        self.prevY = 0
        self.pathStack = []
        self.prevStack = []
        self.playerX = 1
        self.playerY = 1
        self.searchStack = []


    #TODO: Add checking for warps, wraparound, and interacting with walls 
    def updateMap(self): 
        print("Updating Map - direction is " + str(self.direction) + "\n")
        #if a warp occurred, both X and Y will change. Check for this
        if((self.xPos == self.prevX or self.yPos == self.prevY) and (abs(self.xPos - self.prevX) <= 2 or abs(self.xPos - self.prevX) > 250) and abs(self.yPos - self.prevY) <= 2 or abs(self.yPos - self.prevY) > 250): 
            if(self.direction == "LEFT"):
                #print("Direction is left \n")
                #print("Current xPos = " + str(self.xPos) + ", previous xPos = " + str(self.prevX))
                if (self.xPos != self.prevX) :
                    self.currentMap[self.playerY][self.playerX] = "S"
                    self.playerX = self.playerX - 1
                    self.currentMap[self.playerY][self.playerX] = "P"
                    if(self.playerX == 0):
                        self.playerX = 1
                        for row in self.currentMap: 
                            row.insert(0, "?")
                    print("Player moved left")
                else: 
                    self.currentMap[self.playerY][self.playerX - 1] = "B"
                    print("Player encountered an obstacle while moving left")
                    self.pathStack.append("CHECK")
            elif(self.direction == "UP"):
                print("Direction is up \n")
                print("Current yPos = " + str(self.yPos) + ", previous yPos = " + str(self.prevY))
                if (self.yPos != self.prevY):
                    self.currentMap[self.playerY][self.playerX] = "S"
                    self.playerY = self.playerY - 1
                    self.currentMap[self.playerY][self.playerX] = "P"
                    if(self.playerY == 0):
                        self.playerY = 1
                        self.currentMap.insert(0, ["?"] * len(self.currentMap[0]))
                    print("Player moved up")                
                else: 
                    self.currentMap[self.playerY - 1][self.playerX] = "B"
                    print("Player encountered an obstacle while moving up")
                    self.pathStack.append("CHECK")
            elif(self.direction == "RIGHT"):
                print("Direction is right \n")
                print("Current xPos = " + str(self.xPos) + ", previous xPos = " + str(self.prevX))
                if (self.xPos != self.prevX) :
                    self.currentMap[self.playerY][self.playerX] = "S"
                    self.playerX = self.playerX + 1
                    self.currentMap[self.playerY][self.playerX] = "P"
                    if(self.playerX == len(self.currentMap[0]) - 1):
                        for row in self.currentMap: 
                            row.append("?")
                    print("Player moved right")
                else: 
                    self.currentMap[self.playerY][self.playerX + 1] = "B"
                    print("Player encountered an obstacle while moving right")
                    self.pathStack.append("CHECK")
            elif(self.direction == "DOWN"):
                print("Direction is down \n")
                print("Current yPos = " + str(self.yPos) + ", previous yPos = " + str(self.prevY))
                if (self.yPos != self.prevY) :
                    self.currentMap[self.playerY][self.playerX] = "S"
                    self.playerY = self.playerY + 1
                    self.currentMap[self.playerY][self.playerX] = "P"
                    if(self.playerY == len(self.currentMap) - 1):
                        self.currentMap.append(["?"] * len(self.currentMap[0]))
                    print("Player moved down")
                else: 
                    self.currentMap[self.playerY + 1][self.playerX] = "B"
                    print("Player encountered an obstacle while moving down")
                    self.pathStack.append("CHECK")
        else: 
            #Warp must have occurred!
            #Step 1. Mark warp on current map + print new map
            print("Player walked through a warp!")
            self.pathStack.append("CHECK")
            if(self.direction == "LEFT"): 
                self.currentMap[self.playerY][self.playerX - 1] = "W"
            elif(self.direction == "UP"): 
                self.currentMap[self.playerY - 1][self.playerX] = "W"
            elif(self.direction == "RIGHT"): 
                self.currentMap[self.playerY][self.playerX + 1] = "W"
            elif(self.direction == "DOWN"): 
                self.currentMap[self.playerY + 1][self.playerX] = "W"
            self.printMap()
            #Step 2. create new blank map, add it to mapList and assign it as current map
            newMap = [["?","?","?"],["?","P", "?"],["?","?","?"]]
            self.prevX = 0
            self.prevY = 0
            self.xPos = 0
            self.yPos = 0
            self.playerX = 1 
            self.playerY = 1
            self.mapList.append(newMap)
            self.currentMap = newMap
        print("Player Coordinates: Player X = " + str(self.playerX) + ", Player Y = " + str(self.playerY))            
            
                
                
                 
                   
        





    def printMap(self): 
        for row in self.currentMap: 
            print("\n", end =" "),
            for entry in row: 
                print(entry, end = " "),
        print("\n")


    def getPath(self): 
        #when called, perhaps empty stack? (for recalculating path if wall found)
        self.pathStack.clear()
        self.searchStack.clear()
        self.prevStack.clear()
        #A* search - basically depth first search in this case 
        #Starting node is the player's current location (represented by playerX and playerY)
        #start by pushing the starting node to the stack, then begin loop. 
        rowIndex = -1
        entryIndex = -1
        for row in self.currentMap:
            rowIndex = rowIndex + 1
            entryIndex = -1 
            for entry in row:
                entryIndex = entryIndex + 1
                if (entry == "P"): 
                    #print("Found player at index (" + str(rowIndex) + " , " + str(entryIndex) + ") \n"),
                    #first entry in the tuple is the type of square, next two entries are the row and column indices, fourth entry is the path length, final entry is the directional instructions to reach that space
                    self.searchStack.append(("P", rowIndex, entryIndex, 0.0, "NONE"))
                    #print("Adding starting space to the search stack. Search stack = " + str(self.searchStack) + "\n")
        #loop - search stack for shortest path, pop that node 
        currentEntry = None
        #print("Entering While loop \n")
        while (len(self.searchStack) > 0):
            lowestPathLength = float("Inf")  
            currentEntry = None
            #print("About to begin searching the stack \n") 
            for entry in self.searchStack:
                    #print("searchStack entry is " + str(entry) + "\n")
                    if (entry[3] < lowestPathLength): 
                        #print("New shortest path found - old path was " + str(lowestPathLength) + ", new path is " + str(entry[3]) + "\n")
                        currentEntry = entry
                        lowestPathLength = currentEntry[3]
            #print("Current shortest path is through the entry " + str(currentEntry) + "\n")
        #check if node is a destination - if so, break out of loop and start backtracking
            self.searchStack.remove(currentEntry)
            #print("Removing current entry from search stack. Search stack is now " + str(self.searchStack) + "\n")
            self.prevStack.append(currentEntry)
            #print("Adding current entry to previous stack. Previous stack is now " + str(self.prevStack) + "\n")             
            if(currentEntry[0] == "?"):
                #print("Found an unknown space at " + str(currentEntry) + "\n") 
                break
        #if not, expand node by creating left, up, right, and down children (identified by array position) else: 
                #expand to the left (x - 1) 
            #print("About to expand the current entry") 
            currentRow = currentEntry[1]
            currentColumn = currentEntry[2]
            currentCost = currentEntry[3]
            if (currentColumn != 0):
                leftEntry = self.currentMap[currentRow][currentColumn - 1]
                stepCost = self.getStepCost(leftEntry)
                #print("Current cost = " + str(currentCost) + ", step cost = " + str(stepCost) + ", left entry = " + leftEntry + "\n")
                self.searchStack.append((leftEntry, currentRow, currentColumn - 1, currentCost + stepCost, "LEFT"))
                #print("Adding left entry. Search stack is now " + str(self.searchStack) + "\n")
            if (currentRow != 0): 
                upEntry = self.currentMap[currentRow -1][currentColumn]
                stepCost = self.getStepCost(upEntry)
                self.searchStack.append((upEntry, currentRow - 1, currentColumn, currentCost + stepCost, "UP"))
               # print("Adding up entry. Search stack is now " + str(self.searchStack) + "\n")
            if(currentColumn < len(self.currentMap[currentRow]) - 1): 
                rightEntry = self.currentMap[currentRow][currentColumn + 1]
                stepCost = self.getStepCost(rightEntry)
                self.searchStack.append((rightEntry, currentRow, currentColumn + 1, currentCost + stepCost, "RIGHT"))
                #print("Adding right entry. Search stack is now " + str(self.searchStack) + "\n")
            if(currentRow < len(self.currentMap) - 1): 
                downEntry = self.currentMap[currentRow + 1][currentColumn]
                stepCost = self.getStepCost(downEntry)
                self.searchStack.append((downEntry, currentRow + 1, currentColumn, currentCost + stepCost, "DOWN"))
               # print("Adding down entry. Search stack is now " + str(self.searchStack) + "\n") 
    #backtracking - once a destination node is found, add its direction to the pathStack and loop until you make your way back to the start node
        if (currentEntry[0] == "?"): 
            #print("Beginning backtracking with " + str(currentEntry) + "\n")
            while (currentEntry[0] != "P"): 
                direction = currentEntry[4]
                self.pathStack.append(direction)
                #print("Adding direction to pathstack - pathStack is now " + str(self.pathStack) + "\n")
                targetRow = None
                targetColumn = None
                #print("Locating previous step \n")
                if(direction == "LEFT"): 
                    targetRow = currentEntry[1]
                    targetColumn = currentEntry[2] + 1
                if(direction == "UP"): 
                    targetRow = currentEntry[1] + 1
                    targetColumn = currentEntry[2]
                if(direction == "RIGHT"):
                    targetRow = currentEntry[1]
                    targetColumn = currentEntry[2] - 1
                if(direction == "DOWN"): 
                    targetRow = currentEntry[1] - 1
                    targetColumn = currentEntry[2]
                for prev in self.prevStack: 
                    #print("Checking prev = " + str(prev) + "\n")
                    if(prev[1] == targetRow and prev[2] == targetColumn):
                        #print("Previous step found - " + str(prev) + "\n") 
                        currentEntry = prev
                        break
                self.prevStack.remove(currentEntry) 

    def getStepCost(self, currentEntry): 
        if (currentEntry == "B" or currentEntry == "D" or currentEntry == "P"): 
            stepCost = float("Inf")
        elif (currentEntry == "S" or currentEntry == "?"): 
            stepCost = 1.0
        elif (currentEntry == "W"): 
            stepCost = 1000.0
        return stepCost



    def returnAction(self): 
        if (self.xPos % 16 == 0 and self.yPos % 16 == 0):
            #TODO check if player actually moved or warped, adjust map accordingly, then take next action (this could be a separate called function
            #If player moved, update map to show current position (previous position goes from "player" to "safe"
            #also add new row / column of unknowns to the map in the direction of movement
            #if player did not move, update space they should have moved to as impassible (wall) 
            #if player hits wall, press A to see if dialogue box appears. To check for dialogue box, try moving in all directions. If cannot move any direction, dialogue box is open. If dialogue discovered, hammer A while occasionally checking for movement 
            #also check for warp / wraparound. Check wraparound values 
            #to check for warp - check if both x and y changed (should not be possible in other circumstances)
            #If either x and y were already 0 then warp could be confused for movement - check if the non-zero value changed by more than one. In rare occasions this may be confused for a wraparound, but its the best I can do right now
            if (len(self.pathStack) == 0):  
                self.getPath()
            nextStep = self.pathStack.pop()
            print("Popping next step - next step = " + nextStep + "\n")
            if nextStep == "LEFT":
                self.direction = "LEFT"
                return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]                
            elif nextStep == "RIGHT":
                self.direction = "RIGHT"
                return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]                     
            elif nextStep == "UP":
                self.direction = "UP"
                return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]                    
            elif nextStep == "DOWN":
                self.direction = "DOWN"
                return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] 
            elif nextStep == "CHECK":
                self.direction = "CHECK"
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                   
            elif nextStep == "RANDOM": 
                randNum = int(random.random() * 4)
                if (randNum == 0):
                    self.direction = "UP"
                    return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]                        
                elif (randNum == 1): 
                    self.direction = "DOWN"
                    return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]                        
                elif (randNum == 2): 
                    self.direction = "LEFT"
                    return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]                        
                else:
                    self.direction = "RIGHT"
                    return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]  
            else: 
                self.direction == "NONE"
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                        
