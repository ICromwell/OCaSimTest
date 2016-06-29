# -*- coding: utf-8 -*-
"""
This file reads the location of the current entity in the model and determines the order in which the various programs should be run

@author: icromwell
"""

import ntpath
import random
myDir = 'E:\PhD Thesis\Python Scripts\Python Files\MultiProg Test'

execfile(ntpath.join(myDir, "00 - Create Entities.py"))

while True:

    # NTD PROCESS: Apply Demographic Characteristics to a newly-created entity

    if entity.stateNum == 0.0:
        execfile(ntpath.join(myDir, "01 - Apply Initial Characteristics.py"))
        
    # PROBABILITY NODE: Does this person regularly see a dentist?
        # If yes - develop OPL while undergoing regular observations (state 1.0)
        # If no - develop OPL and possibly cancer (state 1.8)
        
    if entity.stateNum == 0.1:
        makeDentist = random.random()
        if makeDentist < 0.5:
            entity.stateNum = 1.0
        else:
            entity.stateNum = 1.8

    # TTE PROCESSS: Dental Screening Appointments

    if entity.stateNum == 1.0:
        execfile(ntpath.join(myDir, "10 - Dentist Screening Appointment.py"))
        
    if entity.stateNum == 1.1:
        print("Simulation time:", entity.allTime, "; ", "Entity had OPL detected at:", entity.time_detectOPL)
        break
        
    # TTE PROCESS: Develop OPL and possibly cancer
    
    if entity.stateNum == 1.8:
        execfile(ntpath.join(myDir, "18 - No Screening.py"))
        
    if entity.stateNum == 1.9:
        print("Simulation time:", entity.allTime, "; ", "Entity developed cancer at:", entity.time_Cancer)
        break
    