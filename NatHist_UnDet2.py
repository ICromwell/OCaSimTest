# -*- coding: utf-8 -*-
"""
Progression of undetected oral cancer. Cancers can either present symptomatically (i.e., person has pain or other symptoms that lead them to consult
a doctor who refers them to an oncologist), or can progress to a more advanced stage. Stage 4 cancers can be fatal.

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

def UnDet(entity, env, estimates):
    
    t_StageOne_Sympt = estimates.NatHist_timeStageone_sympt.sample()
    t_StageOne_StageTwo = estimates.NatHist_timeStageone_stagetwo.sample()
    
    t_StageTwo_Sympt = estimates.NatHist_timeStageone_sympt.sample()
    t_StageTwo_StageThree = estimates.NatHist_timeStagetwo_stagethree.sample()
    
    t_StageThree_Sympt = estimates.NatHist_timeStagethree_sympt.sample()
    t_StageThree_StageFour = estimates.NatHist_timeStagethree_stagefour.sample()
    
    t_StageFour_Sympt = estimates.NatHist_timeStagefour_sympt.sample()
    t_StageFour_Death = estimates.NatHist_timeStagefour_death.sample()


    "Stage One Cancers"
    
    if entity.cancerStage == 1:
        if t_StageOne_Sympt < t_StageOne_StageTwo:
            yield env.timeout(t_StageOne_Sympt)
            entity.allTime = entity.allTime + t_StageOne_Sympt
            entity.cancerTime = entity.cancerTime + t_StageOne_Sympt
            entity.currentState = "3.0 - Detected Cancer"
            entity.stateNum = 3.0
            print("Stage One cancer presents symptomatically")
            entity.cancerDetected = 1
            #yield entity.allTime
            env.exit()
        else:
            yield env.timeout(t_StageOne_StageTwo)
            entity.allTime = entity.allTime + t_StageOne_StageTwo
            entity.cancerTime = entity.cancerTime + t_StageOne_StageTwo
            entity.cancerStage = 2
            print("Stage One cancer progresses to stage Two")
            env.exit()
            
    
    "Stage Two Cancers"
    
    if entity.cancerStage == 2:
        if t_StageTwo_Sympt < t_StageTwo_StageThree:
            yield env.timeout(t_StageTwo_Sympt)
            entity.allTime = entity.allTime + t_StageTwo_Sympt
            entity.cancerTime = entity.cancerTime + t_StageTwo_Sympt
            entity.currentState = "3.0 - Detected Cancer"
            entity.stateNum = 3.0
            print("Stage Two cancer presents symptomatically")
            entity.cancerDetected = 1
            #yield entity.allTime
            env.exit()
        else:
            yield env.timeout(t_StageTwo_StageThree)
            entity.allTime = entity.allTime + t_StageTwo_StageThree
            entity.cancerTime = entity.cancerTime + t_StageTwo_StageThree
            entity.cancerStage = 3
            print("Stage Two cancer progresses to stage Three")
            env.exit()
    
    
    "Stage Three Cancers"
 
    if entity.cancerStage == 3:   
        if t_StageThree_Sympt < t_StageThree_StageFour:
            yield env.timeout(t_StageThree_Sympt)
            entity.allTime = entity.allTime + t_StageThree_Sympt
            entity.cancerTime = entity.cancerTime + t_StageThree_Sympt
            entity.currentState = "3.0 - Detected Cancer"
            entity.stateNum = 3.0
            print("Stage Three cancer presents symptomatically")
            entity.cancerDetected = 1
            #yield entity.allTime
            env.exit()
        else:
            yield env.timeout(t_StageThree_StageFour)
            entity.allTime = entity.allTime + t_StageThree_StageFour
            entity.cancerTime = entity.cancerTime + t_StageThree_StageFour
            entity.cancerStage = 4
            print("Stage Three cancer progresses to stage Four")
            env.exit()
            
            
    "Stage Four Cancers"
    
    if entity.cancerStage == 4:
        if t_StageFour_Sympt < t_StageFour_Death:
            yield env.timeout(t_StageFour_Sympt)
            entity.allTime = entity.allTime + t_StageFour_Sympt
            entity.cancerTime = entity.cancerTime + t_StageFour_Sympt
            entity.currentState = "3.0 - Detected Cancer"
            entity.stateNum = 3.0
            print("Stage Four cancer presents symptomatically")
            entity.cancerDetected = 1
            env.exit()
        else:
            yield env.timeout(t_StageFour_Death)
            entity.allTime = entity.allTime + t_StageFour_Death
            entity.cancerTime = entity.cancerTime + t_StageFour_Death
            entity.dead = 1
            entity.deathcause = "Death from undetected cancer"
            entity.deathtime = entity.allTime
            print("The entity has died from undetected oral cancer")
            entity.cancerDetected = 1
            #yield entity.allTime
            env.exit()
            
    if entity.cancerDetected == 1:
        yield env.exit()