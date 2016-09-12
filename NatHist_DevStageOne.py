# -*- coding: utf-8 -*-
"""
This simulates the development of a de novo OPL, cancer, or death from old age

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

def devStageOne(entity, env, estimates):
    #while entity.OPLStatus == 1:
    t_OPL_StageOne = random.normalvariate(800,100)      # Time to developing stage I oral cancer given OPL+ status
            
    yield env.timeout(t_OPL_StageOne)
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
    #break

# Variables created in this step:
    # time_OPL - the time the most recent OPL was developed
    # time_resolve - the time that an OPL spontaneously reverted to healthy
    # time_Cancer - the time that the person develops cancer
    # hasCancer - a flag indicating that the person has cancer
    # cancerStage - the stage (1, 2, 3, or 4) of an incident cancer
    # cancerTime - the amount of time an incident cancer has been active