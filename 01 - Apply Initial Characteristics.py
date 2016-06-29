# -*- coding: utf-8 -*-
"""
Apply initial demographic characteristics to a newly-created entity
"""

import random

def addInitChars(entity):
    "A function to apply the initial characteristics to each person"
    
    "Starting age is applied randomly between 20 and 60 years"    
    entity.age = random.randrange(20,60)
    
    "Sex: 1 = female, 0 = male"
    makeSex = random.random()
    if makeSex < 0.5:
        entity.sex = 1
    else:
        entity.sex = 0
    
    "Smoking status: 1 = ever smoker, 0 = never smoker"    
    makeSmoker = random.random()
    if makeSmoker < 0.15:
        entity.smokeStatus = 1
    else:
        entity.smokeStatus = 0
    
    "Alcohol use: 1 = heavy user, 0 = not heavy user"   
    makeAlc = random.random()
    if makeAlc < 0.02:
        entity.alcStatus = 1
    else:
        entity.alcStatus = 0
        
    "Entities start without OPL"
    entity.OPLStatus = 0
        
    "Update state"
    entity.currentState = "Initial Characteristics Applied"
    entity.stateNum = 0.1
    
addInitChars(entity)

# VARIABLES CREATED IN THIS STEP:
    # age - the entity's age within the model
    # sex - the entity's binary sex (1: female; 0: male)
    # smokeStatus - whether the entity is a never or ever smoker (1: ever; 0: never)
    # alcStatus - whether or not the entity is a heavy alcohol user (1: yes; 0: no)
    # OPLStatus - whether or not the entity has an active OPL (1: yes; 0: no)