# -*- coding: utf-8 -*-
"""
The progression of an OPL to stage I cancer, or spontaneously resolving

@author: icromwell
"""

import random
from Import_Varnames import Estimates
from Import_Varnames import Estimate
from Import_Varnames import diriSample


from openpyxl import load_workbook
workbook = load_workbook('ImportTest.xlsx')
sheet = workbook.active
estimates = Estimates()

for line in sheet.rows:
    if not line[0].value:
        # There's no estimate name in this row.
        continue
    setattr(estimates, line[0].value, Estimate(line[1].value, line[2].value, line[3].value))

del(estimates.Parameter)

import random
import simpy

def OPLProg(entity, env, estimates):
    
    "Randomly sample two competing TTE risks"
    
    if entity.OPLRisk == 1:
        t_OPL_StageOne = estimates.NatHist_timeOPL_stageone_low.sample()       # Time to developing stage I oral cancer given low-risk OPL status
    
    elif entity.OPLRisk == 2:
        t_OPL_StageOne = estimates.NatHist_timeOPL_stageone_med.sample()       # Time to developing stage I oral cancer given med-risk OPL status
        
    elif entity.OPLRisk == 3:
        t_OPL_StageOne = estimates.NatHist_timeOPL_stageone_hi.sample()        # Time to developing stage I oral cancer given hi-risk OPL status
    
    
    t_OPL_NED = estimates.NatHist_timeOPL_NED.sample()                     # Time to OPL spontaneously resolving


    if t_OPL_StageOne < t_OPL_NED:                              # Depending on which event happens first
        yield env.timeout(t_OPL_StageOne)                           # The person either develops stage I cancer
        print(env.now, ': Developed Stage One Cancer')
               
        entity.OPLStatus = 9                             # 9 signifies an OPL that has turned to cancer
        entity.hasCancer = 1                             # Set a person's cancer status to 1
        entity.cancerStage = 1                           # Cancer is stage 1
        entity.time_Cancer = entity.allTime + env.now    # The time that cancer first develops
        entity.cancerTime = 0                            # A clock of time with cancer starts running now
        entity.allTime += t_OPL_StageOne                 # Update the simulated time for subsequent steps
        entity.currentState = "Undetected Cancer"
        entity.stateNum = 1.9
        env.exit()
    
    else:                                                           # Or the OPL spontaneously resolves
        yield env.timeout(t_OPL_NED)
        print(env.now, ': OPL has resolved on its own')
        entity.OPLStatus = 0                             # Return person's OPL status to 0
        #entity.OPLcount += 1                            # A running count of the number of times someone has developed an OPL
        entity.time_resolve = env.now + entity.allTime   # Record the time of the latest resolution
        entity.allTime += t_OPL_NED                      # Update the simulated time for subsequent steps
        
        env.exit()
    

# Variables created in this step:
    # time_OPL - the time the most recent OPL was developed
    # time_resolve - the time that an OPL spontaneously reverted to healthy
    # time_Cancer - the time that the person develops cancer
    # hasCancer - a flag indicating that the person has cancer
    # cancerStage - the stage (1, 2, 3, or 4) of an incident cancer
    # cancerTime - the amount of time an incident cancer has been active