# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:16:56 2016

@author: icromwell
"""

import random
import simpy
from openpyxl import load_workbook                  # Load the import function
import numpy

"Import values from the table"

from Import_Varnames import Estimates
from Import_Varnames import Estimate
from Import_Varnames import diriSample

workbook = load_workbook('ImportTest.xlsx')
sheet = workbook.active

estimates = Estimates()

for line in sheet.rows:
    if not line[0].value:
        # There's no estimate name in this row.
        continue
    setattr(estimates, line[0].value, Estimate(line[1].value, line[2].value, line[3].value))

del(estimates.Parameter)

from Glb_CreateEntity import Entity
entity = Entity()

from Glb_ApplyInit import addInitChars
addInitChars(entity)
entity.cancerDetected = 0

env = simpy.Environment(initial_time = entity.allTime)

def NatHistOCa(env,entity):
    
#    while True:
      
        "1 - Apparently healthy person develops OPL"
    
        if entity.OPLStatus == 0 and entity.hasCancer == 0:
            from NatHist_DevOPL import devOPL
            env.process(devOPL(entity, env, estimates))
            env.run()
            
        "2 - OPL may progress to stage I cancer or spontaneously resolve"
            
        if entity.OPLStatus == 1 and entity.hasCancer == 0:
            from NatHist_OPLProg import OPLProg
            env.process(OPLProg(entity, env, estimates))
            env.run()
            
#        if getattr(entity, "cancerStage", 0) != 0:    
        
        "3 - Stage I cancer may progress to stage II or be detected symptomatically"    
        
        if entity.cancerDetected == 0:        
        
            if entity.hasCancer == 1 and entity.cancerStage == 1:
                from NatHist_UnDet2 import UnDet
                env.process(UnDet(entity, env, estimates))
                env.run()
                
            "4 - Stage II cancer may progress to stage III or be detected symptomatically"
            
            if entity.hasCancer == 1 and entity.cancerStage == 2:
                from NatHist_UnDet2 import UnDet
                env.process(UnDet(entity, env, estimates))
                env.run()
                
            "5 - Stage III cancer may progress to stage IV or be detected symptomatically"
            
            if entity.hasCancer == 1 and entity.cancerStage == 3:
                from NatHist_UnDet2 import UnDet
                env.process(UnDet(entity, env, estimates))
                env.run()
            
            "6 - Stage IV cancer may be detected symptomatically, or the entity may die"
            
            if entity.hasCancer == 1 and entity.cancerStage == 4:
                from NatHist_UnDet2 import UnDet
                env.process(UnDet(entity, env, estimates))
                env.run()
            
#        if entity.cancerDetected == 1:
#            break
        
def GetAppt(env, entity, resources, events):

    if entity.stateNum == 1.0:
            
        from SysP_ScreenAppt import ScreenAppt                  # Bring in the dentist appointment function from the appropriate file
        env = simpy.Environment(initial_time=entity.allTime)
        env.process(ScreenAppt(entity, resources, events, env))
        env.run()
        
    if entity.stateNum == 1.1:
        from SysP_Biopsy import Biopsy                          # The detected lesion is biopsied
        Biopsy(entity, env, resources, events, estimates)
        
 
    "TTE PROCESS: No Dentist; Develop OPL and possibly cancer"
    
    if entity.stateNum == 1.8:
        print("Entity waits for disease event")
        
    if entity.stateNum == 1.9:
        print("Simulation time:", entity.allTime, "; ", "Entity developed cancer at:", entity.time_Cancer)
        env.exit()
        
    if entity.stateNum == 2.0:
        print("Simulation time:", entity.allTime, "; ", "Entity's OPL was detected at:", entity.allTime)
        
    if entity.stateNum == 3.0:
        print("Simulation time:", entity.allTime, "; ", "Entity's cancer was detected at:", entity.allTime)
        

resources = []
events = []
   
getAppt = env.process(GetAppt(env, entity, resources, events))    
env.process(NatHistOCa(env,entity,getAppt))
env.run()