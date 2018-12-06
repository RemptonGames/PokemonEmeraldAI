#!/usr/bin/python

import retro
import time
import random
import mapMaker
import sys

class StructureProcessor: 

    #def __init__(self):
        

    def getPokemonData(self): 
        data = open("../backupData.json", "r")
        lines = data.readlines()
        data.close()
        data = open("../data.json", "w")
        data.writelines(lines)
        data.close()
        data = open("../data.json", "r")
        lines = data.readlines()
        #for line in lines: 
        #    print(line)  
        data.close()         
    
    def decryptAttackStructure(self, attackStructureIndex, env): 
        #Once the correct substructure has been determined, player will have to extract data from that substructure 2 bytes at a time.
        data = open("../data.json", "r")
        lines = data.readlines()
        index = 0
        baseAddress = None
        #search through the data to find the beginning address of that substructure
        for line in lines:
            index = index + 1 
            if (line.find(attackStructureIndex) > 0): 
                break
        baseAddress = int(lines[index][lines[index].find("3"): lines[index].find(",")])
        print("Whole line - " + lines[index] + ", extracted address - " + str(baseAddress))
        #Using that base address, add new addresses for the 4 parts of the substructure that we need
        lines = lines[:-3]
        for index in range(1, 5): 
            subIndex = attackStructureIndex + str(index)
            lines.append("    },\n    " + subIndex + " {\n")
            lines.append('      "address": ' + str(baseAddress + ((index - 1) * 2)) + '\n')
            lines.append('      "type": "<u2" \n')
        lines.append("    }\n  }\n}")
        data.close()
        data = open("../data.json", "w")
        data.writelines(lines)
        data.close()
        #Have the agent perform an empty action so that the newly added information can be modified 
        #These two byte pieces will need to be decrypted. There are two decryption keys. 
        #The first decryption key is the public ID xor'ed with the first half of the personality value
        #The second key is the secret ID xor'ed with the second half of the personality value
        #Parts 1, 3, and 5 will be xor'ed with the first key
        #parts 2, 4, and 6 will be xor'ed with the second key. 
        #Only the first four parts are necessary - they each contain a pointer to one of the pokemon's 4 moves
        #Send each of these four parts to the "proccessAttacks()" function and get the attack data
        

    def processSubstructures(self, info, env): 
        #Should be a loop that can go through all six pokemon data structures
        for index in range(1, 7): 
            attackStructureIndex = None
            dictionaryIndex = "pv" + str(index)
            #These two portions need to be combined into a single large integer
            pv1 = info[dictionaryIndex + "A"]
            pv2 = info[dictionaryIndex + "B"]
            print("PV1 = " + hex(pv1) + ", PV2 = " + hex(pv2))
            pv1 = pv1 * (2 ** 16)
            print("PV1 has been multiplied - now pv1 = " + hex(pv1)) 
            personalityValue = pv1 + pv2
            print("PV2 has been added to PV1 - result is " + hex(pv1))
        #Should check the pokemon's personality value. If it is 0, don't process. 
            if(personalityValue == 0): 
                print("Don't process " + dictionaryIndex)
                order = personalityValue % 24
        #If it is not 0, should use the personality value to determine the order of the substructures
            else: 
                print("Processing " + dictionaryIndex)
                order = personalityValue % 24
                decryptKey = info["IDNo"] ^ personalityValue
                #This determines which substructure is the attacks substructure, and prepares it to be decrypted
                if(order >= 6 and order <= 11): 
                    attackStructureIndex = "substructure" + str(index) + "A"
                    attackStructure = hex(info[attackStructureIndex])
                    print("Order is " + str(order) + ", attacks is first substructure - " + str(attackStructureIndex) + " - " + str(attackStructure))
                elif (order == 0 or order == 1 or order == 14 or order == 15 or order == 20 or order == 21):
                    attackStructureIndex = "substructure" + str(index) + "B" 
                    attackStructure = hex(info[attackStructureIndex])
                    print("Order is " + str(order) + ", attacks is second substructure - " + str(attackStructureIndex) + " - " + str(attackStructure))
                elif (order == 2 or order == 4 or order == 12 or order == 17 or order == 18 or order == 23): 
                    attackStructureIndex = "substructure" + str(index) + "C"
                    attackStructure = hex(info[attackStructureIndex])
                    print("Order is " + str(order) + ", attacks is third substructure - " + str(attackStructureIndex) + " - " + str(attackStructure))
                else:   
                    attackStructureIndex = "substructure" + str(index) + "D"
                    attackStructure = hex(info[attackStructureIndex])
                    print("Order is " + str(order) + ", attacks is fourth substructure - " + str(attackStructureIndex) + " - " + str(attackStructure))
        #After determining which substructure is the "attacks" substructure, decrypt that substructure and extract the attack data
            if(attackStructureIndex is not None): 
                self.decryptAttackStructure(attackStructureIndex, env)
        data = open("../data.json", "r")
        lines = data.readlines()
        for line in lines: 
            print(line)
        data.close()
            
        






















