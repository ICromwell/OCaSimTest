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

def resolveOPL(entity, env):                                # A process to return existing OPLs to healthy tissue
    t_OPL_NED = random.normalvariate(800,100)           # Time to OPL spontaneously resolving
    #while entity.OPLStatus == 1:
    yield env.timeout(t_OPL_NED)
    print(env.now, ': OPL has resolved on its own')
    entity.OPLStatus = 0                             # Return person's OPL status to 0
    #entity.OPLcount += 1                            # A running count of the number of times someone has developed an OPL
    entity.time_resolve = env.now + entity.allTime   # Record the time of the latest resolution
    entity.allTime += t_OPL_NED                      # Update the simulated time for subsequent steps
    
    env.exit()
        #break
        



# Variables created in this step:
    # time_OPL - the time the most recent OPL was developed
    # time_resolve - the time that an OPL spontaneously reverted to healthy
    # time_Cancer - the time that the person develops cancer
    # hasCancer - a flag indicating that the person has cancer
    # cancerStage - the stage (1, 2, 3, or 4) of an incident cancer
    # cancerTime - the amount of time an incident cancer has been active