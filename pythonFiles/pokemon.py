#!/usr/bin/python

import retro
import time
import random 


#This class will be called to make decisions in a battle, and will keep track of both your own pokemon and your opponent's 
class Pokemon:     
    
    #initialize an empty pokemon
    #Pokemon should have two types, all necessary stats, and 4 moves
    def __init__(self, type1 = 0, type2 = 0, health = 0, attack = 0, defense = 0,spDef = 0, spAtk = 0,
                 speed = 0, pv = 0, attack1 = None, attack2 = None, attack3 = None, attack4 = None):
            self.type1 = type1
            self.type2 = type2
            self.health = health
            self.attack = attack
            self.defense = defense
            self.spDef = spDef
            self.spAtk = spAtk
            self.speed = speed 
            self.attack1 = attack1
            self.attack2 = attack2
            self.attack3 = attack3
            self.attack4 = attack4
            self.pv = pv

    def printPokemon(self): 
        print("Type1: " + str(self.type1) + "\nType2: " + str(self.type2) + "\nHealth: " + str(self.health) +
                "\nAttack: " + str(self.attack) + "\nDefense: " + str(self.defense) + "\nSpecial Defense: " + 
                str(self.spDef) + "\nSpecial Attack: " + str(self.spAtk) + "\nSpeed: " + str(self.speed))


class Attack: 
        
    #initialize a move with type, base power, and accuracy
    def __init__(self, moveType, basePower, accuracy):
            self.moveType = moveType
            self.basePower = basePower
            self.accuracy = accuracy


    

    
