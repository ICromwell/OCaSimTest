# -*- coding: utf-8 -*-
"""
A screening process wherein a person returns for regular checkups at a dentist
"""

# Time interval between appointments
appInt = 6*30
    
# Create a counter for the number of dental appointments, if one doesn't already exist
if getattr(entity, "count_DentAppt", 0) == 0:
    entity.count_DentAppt = 0
    
def devOPL(entity, env):
    while True:
        t_OPL = random.normalvariate(500, 100)
        yield env.timeout(t_OPL)
        #entity.OPL.append(env.now)
        print(env.now, 'Developed OPL')
        entity.OPLStatus = 1
        entity.time_OPL = env.now
        env.exit()

def appointment_process(entity, env):
    while True:
        if entity.OPLStatus ==0:
            yield env.timeout(appInt)
            print(env.now, 'Everything looks fine, see you in %2.0f days'%appInt)
        elif entity.OPLStatus == 1:
            print(env.now, 'Found something at %2.0f'%env.now)
            entity.time_detectOPL = env.now                                 # The time at which an OPL is detected
            entity.allTime = entity.allTime + entity.time_detectOPL         # Update total simulation runtime
            entity.currentState = "Detected OPL, undergoing evaluation"     # Update state
            entity.stateNum = 1.1
            env.exit()
        entity.count_DentAppt = entity.count_DentAppt +1                    # Add running count to the number of dental appointments
    

# Run simulation

env = simpy.Environment()
env.process(devOPL(entity, env))
env.process(appointment_process(entity, env))
env.run()


# VARIABLES CREATED IN THIS STEP:
    # count_DentAppt - a counter for how many dentist's appointments an entity has had
    # time_OPL - the time that the entity develops an OPL
    # time_detectOPL - the time that an OPL is detected by a dentist
    # OPLStatus - a flag for whether or not an entity has an OPL 

