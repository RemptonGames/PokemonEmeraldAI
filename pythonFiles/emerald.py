#!/usr/bin/python

import retro
import time
import random
import mapMaker
import structureProcessor
import sys 

#env = retro.make('PokemonEmeraldVersion-GbAdvance', 'Female.Ruby')
env = retro.make('PokemonEmeraldVersion-GbAdvance', 'state5')
env.reset()
done = False
state = "navigating"
action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ob, rew, done, info = env.step(action)
xPos = info["xPos"]
yPos = info["yPos"]
print("xPos = " + str(xPos) + ", yPos = " + str(yPos) + "\n")
maker = mapMaker.MapMaker(xPos, yPos)
sp = structureProcessor.StructureProcessor()
currentDirection = None
prevDirection = None

#Any time we move and either X or Y change by more than 2 at a time, we must have gone into a warp. Stop moving and return?
def takeStep(): 
    print("Taking Step")
    global currentDirection
    time1 = time.perf_counter()
    time2 = time1
    startingX = maker.xPos
    startingY = maker.yPos
    targetX = None
    targetY = None
    moved = False
    print("Current Direction = " + str(currentDirection))
    if (currentDirection == "LEFT"): 
        if(startingX == 0): 
            targetX = 242
        else: 
            targetX = startingX - 14;
        targetY = startingY
    elif (currentDirection == "RIGHT"): 
        if(startingX == 240): 
            targetX = 254
        else: 
            targetX = startingX + 14; 
        targetY = startingY
    elif (currentDirection == "UP"): 
        targetY = startingY + 14
        targetX = startingX
    elif(currentDirection == "DOWN"): 
        targetY = startingY - 14
        targetX = startingX
    print("Current X = " + str(startingX) + ", Current Y = " + str(startingY) + ". Target X = " + str(targetX) + ", Target Y = " + str(targetY))
    loopFinished = False
    while(not loopFinished): 
        ob, rew, done, info = env.step(action)
        env.render()
        maker.prevX = maker.xPos
        maker.prevY = maker.yPos
        maker.xPos = info["xPos"]
        maker.yPos = info["yPos"]
        if((abs(maker.xPos - maker.prevX) > 2 and abs(maker.xPos - maker.prevX) < 250) or (abs(maker.yPos - maker.prevY) > 2) and abs(maker.yPos - maker.prevY) < 250):
            print("X difference = " + str(abs(maker.xPos - maker.prevX)) + ", Y difference = " + str(abs(maker.yPos - maker.prevY)))
            #must have walked through a loop - return
            print("I MUST HAVE WALKED THROUGH A WARP!")
            return "WARP"
        time2 = time.perf_counter()
        #print("In Loop. Current X = " + str(maker.xPos) + ", Current Y = " + str(maker.yPos) + ". Target X = " + str(targetX) + ", Target Y = " + str(targetY) + ", Time difference = " + str(time2 - time1) + ", previous X = " + str(maker.prevX) + ", previous Y = " + str(maker.prevY))
        if(maker.xPos == targetX and maker.yPos == targetY): 
            loopFinished = True
            moved = True
            print("PLAYER MOVED CORRECTLY \n")
        if(maker.xPos == startingX and maker.yPos == startingY and (time2 - time1 > 0.1)): 
            loopFinished = True
            print("LOOP TIMED OUT")
        if((time2 - time1 > 1.0)): 
            loopFinished = True
            print("LOOP TIMED OUT")
    time1 = time.perf_counter()
    time2 = time1
    while(time2 - time1 < 0.05): 
      ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
      time2 = time.perf_counter()
    maker.prevX = maker.xPos
    maker.prevY = maker.yPos
    maker.xPos = info["xPos"]
    maker.yPos = info["yPos"]
    return moved




def checkDialogue(): 
    #Check prev direction and map to see if you walked into a wall. 
    hitWall = False
    pressedA = False
    checkMoved = False
    global prevDirection
    global currentDirection
    global action
    print("Previous direction = " + str(prevDirection))
    if(prevDirection == "LEFT" and maker.currentMap[maker.playerY][maker.playerX - 1] == "B"): 
        hitWall = True
    elif(prevDirection == "UP" and maker.currentMap[maker.playerY - 1][maker.playerX] == "B"): 
        hitWall = True
    elif(prevDirection == "RIGHT" and maker.currentMap[maker.playerY][maker.playerX + 1] == "B"):
        hitWall = True
    elif(prevDirection == "DOWN" and maker.currentMap[maker.playerY + 1][maker.playerX] == "B"): 
        hitWall = True
    if(hitWall == True): 
        print("I must have bumped into something")
        #If so, press A, and wait to see if the wall is interactive. 
        time1 = time.perf_counter()
        time2 = time1
        print("Pressing A to interact with wall")
        pressedA = True
        while(time2 - time1 < 1): 
            ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
            time2 = time.perf_counter()
            env.render()
        #Whether we warped or bumped into a wall, dialogue box should now be open. To check, start by trying to backtrack.  
        if(prevDirection == "LEFT"): 
            currentDirection = "RIGHT"
            action = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            print("Trying to move right")
            checkMoved = takeStep()
        elif(prevDirection == "UP"): 
            currentDirection = "DOWN"
            action = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            print("Trying to move down")
            checkMoved = takeStep()
        elif(prevDirection == "RIGHT"): 
            currentDirection = "LEFT"
            action = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            print("Trying to move left")
            checkMoved = takeStep()
        elif(prevDirection == "DOWN"): 
            currentDirection = "UP"
            action = [0, 0, 0, 0, 1 , 0, 0, 0, 0, 0, 0, 0]
            print("Trying to move up")
            checkMoved = takeStep()
    print("Tried to move - result was " + str(checkMoved))
    #If backtracking doesn't work, try pressing random directions and A until you can move again
    loopCount = 0
    while (checkMoved == False): 
        #Until you are able to move again - try pressing A and random directions
        print("Did not move - entering loop")
        print("Trying A again, then waiting for a second")
        ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
        time1 = time.perf_counter()
        time2 = time1
        while(time2 - time1 < 1): 
            ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            env.render()
            time2 = time.perf_counter()
        if(hitWall == False or loopCount > 10):
            prevDirection = currentDirection
            randNum = int(random.random() * 4)
            if (randNum == 0):
                currentDirection = "UP"  
                action = [0, 0, 0, 0, 1 , 0, 0, 0, 0, 0, 0, 0]                 
            elif (randNum == 1): 
                currentDirection = "DOWN"
                action = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]                        
            elif (randNum == 2): 
                currentDirection = "LEFT"  
                action = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]                     
            else:
                currentDirection = "RIGHT"
                action = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            print("TRYING TO MOVE AGAIN")
        checkMoved = takeStep()
        loopCount = loopCount + 1
        print(str(loopCount))
    if(checkMoved == True): 
        print("I moved - now I will move back into previous position")
        prevDirection = currentDirection
        if(prevDirection == "LEFT"): 
            currentDirection = "RIGHT"
            action = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            takeStep()
        elif(prevDirection == "UP"): 
            currentDirection = "DOWN"
            action = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            takeStep()
        elif(prevDirection == "RIGHT"): 
            currentDirection = "LEFT"
            action = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            takeStep()
        elif(prevDirection == "DOWN"): 
            currentDirection = "UP"
            action = [0, 0, 0, 0, 1 , 0, 0, 0, 0, 0, 0, 0]
            takeStep()
    
    
    

while not done:
    env.render() 
    #time.sleep(0.1)
    sp.getPokemonData()
    action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ob, rew, done, info = env.step(action) 
    sp.processSubstructures(info, env)
    #action = env.action_space.sample() #First entry is unknown
    #Second entry is unknown #Third entry is "select" button 
    #Fourth button is still unknown #Fifth button is "up"
    #sixth button is "down" #seventh button is "left"
    #eighth button is "right"  #ninth button appears to be "a"
    #tenth button is unknown (maybe "b"?) #eleventh button is unknown
    #twelfth button is unknown #action = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    #print(action)
    #action = maker.returnAction()
    #prevDirection = currentDirection
    #currentDirection = maker.direction
    #if((currentDirection == "LEFT") or currentDirection == "UP" or currentDirection == "RIGHT" or currentDirection == "DOWN"):
    #    takeStep()
    #elif(currentDirection == "CHECK"): 
    #    print("Checking for a dialogue box")
    #    checkDialogue()
    #else: 
    #    print("I am confoosle!")
    #maker.updateMap()
    #print("xPos = " + str(maker.xPos) + ", yPos = " + str(maker.yPos) + "\n")
    #maker.printMap()  
    done = True
sys.exit()              
        

    























