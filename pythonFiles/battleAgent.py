#!/usr/bin/python

import retro
import time
import random 
import pokemon


#This class will be called to make decisions in a battle, and will keep track of both your own pokemon and your opponent's 
class BattleAgent:     

    #initializes all instance variables for the battle agent
    def __init__(self):
        #This typechart will be used to calculate damage when making decisions.
        #The row represents the attacking type, the column represents the defending type
        self.typechart =     [[1, 1, 1, 1, 1, 0.5, 1, 0, 0.5, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.typechart.append([2, 1, 0.5, 0.5, 1, 2, 0.5, 0, 2, 1, 1, 1, 1, 0.5, 2, 1, 2])
        self.typechart.append([1, 2, 1, 1, 1, 0.5, 2, 1, 0.5, 1, 1, 2, 0.5, 1, 1, 1, 1 ])    
        self.typechart.append([1, 1, 1, 0.5, 0.5, 0.5, 1, 0.5, 0, 1, 1, 2, 1, 1, 1, 1, 1])    
        self.typechart.append([1, 1, 0, 2, 1, 2, 0.5, 1, 2, 2, 1, 0.5, 2, 1, 1, 1, 1])       
        self.typechart.append([1, 0.5, 2, 1, 0.5, 1, 2, 1, 0.5, 2, 1, 1, 1, 1, 2, 1, 1])    
        self.typechart.append([1, 0.5, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 0.5, 1, 2, 1, 2, 1, 1, 2])        
        self.typechart.append([0, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 2, 1, 1, 0.5])
        self.typechart.append([1, 1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 0.5, 1, 0.5, 1, 2, 1, 1])        
        self.typechart.append([1, 1, 1, 1, 1, 0.5, 2, 1, 2, 0.5, 0.5, 2, 1, 1, 2, 0.5, 1])
        self.typechart.append([1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 0.5, 1])
        self.typechart.append([1, 1, 0.5, 0.5, 2, 2, 0.5, 1, 0.5, 0.5, 2, 0.5, 1, 1, 1, 0.5, 1])       
        self.typechart.append([1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 0.5, 1])
        self.typechart.append([1, 2, 1, 2, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 1, 0])
        self.typechart.append([1, 1, 2, 1, 2, 1, 1, 1, 0.5, 0.5, 0.5, 2, 1, 1, 0.5, 2, 1])
        self.typechart.append([1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 2, 1])
        self.typechart.append([1, 0.5, 1, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 2, 1, 1, 0.5])
        self.party = []
        pokemon1 = pokemon.Pokemon()
        pokemon2 = pokemon.Pokemon()
        pokemon3 = pokemon.Pokemon()
        self.party.append(pokemon1)
        self.party.append(pokemon2)
        self.party.append(pokemon3)




    #This function will be called after data about the pokemon and moves have been loaded by the structure processor. 
    #hardcode the three pokemon, order them based on their personality numbers. 
    def getPartyData(self, env): 
        action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ob, rew, done, info = env.step(action)
        for index in range(1, 4): 
            current = self.party[index - 1]
            current.health = info["health" + str(index)]
            current.attack = info["attack" + str(index)]
            current.defense = info["defense" +str(index)]
            current.spDef = info["spDef" + str(index)]
            current.spAtk = info["spAtk" + str(index)]
            current.speed = info["speed" + str(index)]
            #print("PID = " + str(info["pv" + str(index)]))
            current.pv = info["pv" + str(index)]
            #current pokemon is lotad - load lotad's stats
            if(current.pv == 3233569461): 
                #print("Lotad")
                current.type1 = 10
                current.type2 = 11
                current.attack1 = pokemon.Attack(7, 30, 10)
                current.attack2 = pokemon.Attack(0, 0, 1)
                current.attack3 = pokemon.Attack(11, 20, 1)
            #This is poochyena
            elif(current.pv == 2287974448): 
                #print("Poochyena")
                current.type1 = 16
                current.type2 = 16
                current.attack1 = pokemon.Attack(0, 35, 0.95)
                current.attack2 = pokemon.Attack(0, 0, 1)
            elif(current.pv == 2591126865): 
                #print("Mudkip")
                current.type1 = 10
                current.type2 = 10
                current.attack1 = pokemon.Attack(0, 35, 0.95)
                current.attack2 = pokemon.Attack(0, 0, 1)
                current.attack3 = pokemon.Attack(4, 20, 1)
            else: 
                print("Something went wrong")
        
        
        

    #This function will be called everytime the enemy Pokemon ID changes, which includes when enterring / leaving a battle
    def getEnemyData(self): 
        print("Getting enemy data")

    #This calculates how much damage the player's pokemon will do to the opponent
    def getPlayerDamage(self): 
        print("Getting player damage")
    
    #This calculates how much damage the enemy's pokemon will do to the player
    def getEnemyDamage(self): 
        print("Getting enemy damage")

    #The primary function of this class - uses information from the previous functions to 
    def returnAction(self, env): 
        print("Trying A again, then waiting for a second")
        ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
        time1 = time.perf_counter()
        time2 = time1
        while(time2 - time1 < 1): 
            ob, rew, done, info = env.step([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            env.render()
            time2 = time.perf_counter()
        
   
