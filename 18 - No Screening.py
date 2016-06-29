# -*- coding: utf-8 -*-
"""
This simulates the development of a de novo OPL, cancer, or death from old age

@author: icromwell
"""

import random

t_OPL_StageOne = random.normalvariate(800,100)      # Time to developing stage I oral cancer given OPL+ status
t_OPL_NED = random.normalvariate(800,100)           # Time to OPL spontaneously resolving
t_OPL = random.normalvariate(500, 100)  # Time to developing de novo OPL


def devOPL(entity, env):                             # A process to develop new OPLs
    #while (entity.OPLStatus == 0):
        yield env.timeout(t_OPL)
        print(env.now, 'Developed OPL')
        entity.OPLStatus = 1                         # Set person's OPL status to 1
        #entity.OPLcount += 1                        # Increase the counter tracking number of OPL's developed by 1
        entity.time_OPL = env.now + entity.allTime   # Track the simulated time that the last OPL was developed
        entity.allTime += t_OPL                      # Update the simulated time for subsequent steps
        env.exit()
        #break
    
def OPL_NED(entity, env):                                # A process to return existing OPLs to healthy tissue
    #while entity.OPLStatus == 1:
        yield env.timeout(t_OPL_NED)
        print(env.now, ': OPL has resolved on its own')
        entity.OPLStatus = 0                             # Return person's OPL status to 0
        #entity.OPLcount += 1                            # A running count of the number of times someone has developed an OPL
        entity.time_resolve = env.now + entity.allTime   # Record the time of the latest resolution
        entity.allTime += t_OPL_NED                      # Update the simulated time for subsequent steps
        env.exit()
        #break
        
def devStageOne(entity, env):
    #while entity.OPLStatus == 1:
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

env = simpy.Environment()

if entity.OPLStatus == 0:
    env.process(devOPL(entity, env))
if entity.OPLStatus == 1:
    if t_OPL_StageOne < t_OPL_NED:
        env.process(devStageOne(entity, env))
    else:
        env.process(OPL_NED(entity, env))

env.run()
entity.__dict__


# Variables created in this step:
    # time_OPL - the time the most recent OPL was developed
    # time_resolve - the time that an OPL spontaneously reverted to healthy
    # time_Cancer - the time that the person develops cancer
    # hasCancer - a flag indicating that the person has cancer
    # cancerStage - the stage (1, 2, 3, or 4) of an incident cancer
    # cancerTime - the amount of time an incident cancer has been active