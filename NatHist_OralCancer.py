# -*- coding: utf-8 -*-
"""
The natural history of oral cancer progression

This file sequences the development of oral cancer from full health through to death of untreated metastatic disease

The sequence of events:

    1 - Aparently healthy person develops OPL
    
    2 - OPL may:
        a) progress to stage I cancer
        b) spontaneously resolve
        
    3 - Stage I cancer may:
        a) progress to stage II cancer
        b) be detected symptomatically
        
    4 - Stage II cancer may:
        a) progress to stage III cancer
        b) be detected symptomatically
        
    5 - Stage III cancer may:
        a) progress to stage IV cancer
        b) be detected symptomatically
        
    6 - Stage IV cancer may:
        a) kill the affected person
        b) be detected symptomatically
        
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

env = simpy.Environment(initial_time = entity.allTime)

def NatHistOCa(env,entity):
    
    entity.cancerDetected = 0
      
    "1 - Apparently healthy person develops OPL"

    from NatHist_DevOPL import devOPL
    env.process(devOPL(entity, env, estimates))
    env.run()
        
    "2 - OPL may progress to stage I cancer or spontaneously resolve"
        
    if entity.OPLStatus == 1 and entity.hasCancer == 0:
        from NatHist_OPLProg import OPLProg
        env.process(OPLProg(entity, env, estimates))
        env.run()
        
        "An error check, to make sure the program isn't doing things out of order"        
        
    elif entity.OPLStatus == 1 and entity.hasCancer == 1:
        print("OPLStatus should be 9, which means there's a problem somewhere")
        entity.currentState = "Error"
        entity.stateNum = 0.9
    
    if getattr(entity, "cancerStage", 0) != 0:    
    
        "3 - Stage I cancer may progress to stage II or be detected symptomatically"    
        
        if entity.hasCancer == 1 and entity.cancerStage == 1 and entity.cancerDetected == 0:
            from NatHist_UnDet import UnDet
            env.process(UnDet(entity, env, estimates))
            env.run()
            
        "4 - Stage II cancer may progress to stage III or be detected symptomatically"
        
        if entity.hasCancer == 1 and entity.cancerStage == 2 and entity.cancerDetected == 0:
            from NatHist_UnDet import UnDet
            env.process(UnDet(entity, env, estimates))
            env.run()
            
        "5 - Stage III cancer may progress to stage IV or be detected symptomatically"
        
        if entity.hasCancer == 1 and entity.cancerStage == 3 and entity.cancerDetected == 0:
            from NatHist_UnDet import UnDet
            env.process(UnDet(entity, env, estimates))
            env.run()
        
        "6 - Stage IV cancer may be detected symptomatically, or the entity may die"
        
        if entity.hasCancer == 1 and entity.cancerStage == 3 and entity.cancerDetected == 0:
            from NatHist_UnDet import UnDet
            env.process(UnDet(entity, env, estimates))
            env.run()
            
        elif entity.cancerDetected == 1:
            env.exit()
            

        