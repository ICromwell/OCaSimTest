# -*- coding: utf-8 -*-
"""
This code creates an entity with an expandable list of characteristics.

The entity is the main simulation unit.
"""

import sys
sys.path.append('C:\Anaconda\Lib\site-packages')

import random
import simpy


class Entity(object):
   def __init__(self, **kwargs):
       #This step allows the class to adopt any characteristic defined within the model       
       self.__dict__.update(kwargs)
       # These variables allow you to track where the entity is within the model
           # "currentState" is a text description of the state
           # "stateNum" is used by the sequencer to determine what action to take
       self.currentState = "Newly created entity"
       self.stateNum = 0.0
       # "allTime" is a running counter of the amount of time elapsed within the simulation (i.e., survival time)
       self.allTime = 0

entity = Entity()