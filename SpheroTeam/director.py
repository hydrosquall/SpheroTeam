# Director.py
# Prototyped in notebooks 7, 8

import time
import math
import logging

from navigation import get_bot_position
from core import roll_sphero


def bot_go_to_point(bot, offset,
                     targetX, targetY,
                     trace_object, trace_color,
                     MAX_X, MAX_Y, tracker,
                     TIMEOUT=250, MAX_SECONDS=10, 
                     stopRadius=30, Kp=0.23, DEBUG=False):
    """
    Constrast to "RUSH TO POINT IN STRAIGHT LINE"

    Really would work better with a bigger field

    # TIMEOUT should be longer than  get_position's runtime

    Or boost speed when within range: pause and then burst
    # With thanks to Rabia Aslam for ideas about the PID controller
    http://rabiaaslam.com/designing-the-sphero-control-system/
    """

    if (targetX > MAX_X) or (targetY > MAX_Y):
        logging.warning("Can't roll off the screen! %d %d", MAX_X, MAX_Y)
        return -1
    sleepTime = TIMEOUT/1000.0

    currentX, currentY = get_bot_position(bot, trace_object, tracker, samples=1)

    # Basic closed loop controller
    startTime = time.time()

    # Angle to distance
    angle, distance = vector_to_target(currentX, currentY, targetX, targetY)
    print("Get from {},{} to {},{}| Distance {} / {}").format(currentX, currentY, 
                                                         targetX, targetY, distance, angle)
    bot.set_motion_timeout(TIMEOUT)
    # REPLACE SOMEDAY WITH TRUE PID CONTROLLER
    while distance > stopRadius and (((time.time() - startTime ) < MAX_SECONDS)):
        outSpeed = distance * Kp # Constant of proportional control

        if outSpeed < 30:
            outSpeed = 35

        # roll the sphero, make use of the request object
        if DEBUG:
            print("Dist {} outSpeed {} at {} degrees: {},{}"\
                  .format(distance, outSpeed, angle, currentX, currentY))

        roll_sphero(bot, outSpeed, -angle, offset)

        # use this for recovery when lost

        bot.prev_angle = -angle   
        time.sleep(sleepTime)

        currentX , currentY = get_bot_position(bot, trace_object, tracker, samples=1)

        if currentX:
            # Repeat waypointing calculation
            angle, distance = vector_to_target(currentX, currentY, targetX, targetY)
        else:
            # bring robot back onto screen
            angle = bot.prev_angle
            distance = 100 # aim to go back to middle
            
    print("Stopped at {},{}, with dist {}").format(currentX, currentY, distance)

def vector_to_target(currentX, currentY, targetX, targetY):
    '''
        Returns distance and angle between two points
    '''
    deltaX = targetX - currentX
    deltaY = targetY - currentY
    angle = math.degrees(math.atan2(deltaY, deltaX))
    distance = math.sqrt(deltaX * deltaX + deltaY * deltaY)

    return angle, distance

# Team driving functions
def team_go_to_points(bots, targets, offsets, traceable_object, traceable_color,
                      MAX_X=imageX, MAX_Y=imageY, TIMEOUT=200, stopRadius=25):
    '''
        Send each bot in the team to its designated point. 
        Bots drive in a straight line to
        each point.

        Alternate function would send each robot along paths (sequences of points)
        Perhaps each point might have its own Kp or timeout or speed.
    '''

    for bot in bots:
        bot.set_rgb(0,0,0)

    for i, bot in enumerate(bots):
        print("Bot {}".format(bot.bt_name))
        bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
        time.sleep(1.5)

        targetX, targetY = targets[i]
        bot_go_to_point(bot, offsets[i], targetX, targetY,
                        traceable_object, traceable_color, MAX_X, MAX_Y, 
                        tracker, TIMEOUT=200, stopRadius=stopRadius)

        bot.set_rgb(0,0,0)



def team_go_to_paths(bots, paths, offsets, traceable_object, traceable_color,
                      MAX_X, MAX_Y, TIMEOUT=200, stopRadius=25):
    '''
        Send each bot in the team a list of points
    '''
    
    for bot in bots:
        bot.set_rgb(0,0,0)
    
    for i, bot in enumerate(bots):
        print("Bot {}".format(bot.bt_name))
        bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
        time.sleep(1.5)
        

        for target in paths[i]:
            targetX, targetY = target
            bot_go_to_point(bot, offsets[i], targetX, targetY,          
                traceable_object, traceable_color, MAX_X, MAX_Y, tracker, TIMEOUT=250,
                           stopRadius=stopRadius)  
        
        # Turn robot off when done
        bot.set_rgb(0,0,0) 
