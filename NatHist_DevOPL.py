# -*- coding: utf-8 -*-
"""
A screening process wherein a person returns for regular checkups at a dentist
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

screenInt = random.randint(1,10)                # The dentist screens for cancer at a random constant frequency

 
def devOPL(entity, env, estimates):
    
    t_OPL = estimates.NatHist_timeOPL.sample()
    yield env.timeout(t_OPL)
    #entity.OPL.append(env.now)
    print(env.now, 'Developed OPL')
    entity.OPLStatus = 1
    entity.allTime = entity.allTime + env.now
    entity.time_OPL = entity.allTime
    
    "Assign risk category of OPL progression"    
    
    OPLRiskGroup_names = ["OPLRisk_Low", "OPLRisk_Med", "OPLRisk_Hi"]                           # A 'names' vector for the dirichlet sampling process
    OPLRiskGroup_probs = [estimates.NatHist_OPLrisk_low.mean, estimates.NatHist_OPLrisk_med.mean, estimates.NatHist_OPLrisk_hi.mean]   # A 'values' vector for the dirichlet sampling process
    
    diriSample(estimates, OPLRiskGroup_names, OPLRiskGroup_probs)      # Generate random value for OPL risk group
    entity.OPLRisk = random.random()                   
        
    if entity.OPLRisk <= estimates.OPLRisk_Low:                              # Low risk group
        entity.OPLRisk = 1
        
    elif estimates.OPLRisk_Low < entity.OPLRisk <= estimates.OPLRisk_Hi:     # Medium risk group
        entity.OPLRisk = 2
            
    elif entity.OPLRisk > estimates.OPLRisk_Hi:                              # High risk group
        entity.OPLRisk = 3

    else:
        print("Something has gone wrong in the OPL risk assignment process")
        entity.currentstate = "Error"
        entity.stateNum = 0.9        
    
    env.exit()
    
    

# VARIABLES CREATED IN THIS STEP:
    # time_OPL - the time that the entity develops an OPL
    