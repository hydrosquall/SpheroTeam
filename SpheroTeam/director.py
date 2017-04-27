# Director.py
# Prototyped in notebooks 7, 8, 9
import time
import math
import logging

from navigation import get_bot_position
from core import roll_sphero
from pidController import pidController


def bot_go_to_point(bot, offset,
                    targetX, targetY,
                    trace_object, trace_color,
                    MAX_X, MAX_Y, tracker,
                    TIMEOUT=250, MAX_SECONDS=10,
                    stopRadius=30, Kp=0.25, DEBUG=False, PID=False):
    """ Sends robot to a desired point

    :param bot: robot being controlled
    :param targetX: x coordinate
    :param targetY: y coordinate
    :param MAX_X: maximum x dimension
    :param TIMEOUT: How many milliseconds pass before issuing new command
    :param MAX_SECONDS: How many seconds to navigate before quitting
    :param stopRadius: Pixel distance threshhold before stopping
    :param Kp: Proportional control constant
    :param DEBUG: Boolean toggling print statements
    :param PID: Boolean toggling whether to use PID control

    :type trace_object: traceable object
    :type trace_color: RGB list of values

    # With thanks to Rabia Aslam for ideas about the PID controller
    http://rabiaaslam.com/designing-the-sphero-control-system/
    """

    if (targetX > MAX_X) or (targetY > MAX_Y):
        logging.warning("Can't roll off the screen! %d %d", MAX_X, MAX_Y)
        return -1
    sleepTime = TIMEOUT / 1000.0

    currentX, currentY = get_bot_position(bot, trace_object,
                                          tracker, samples=2)

    # Basic closed loop controller
    startTime = time.time()

    # Angle to distance
    angle, distance = vector_to_target(currentX, currentY, targetX, targetY)
    print("Go {},{} to {},{}| Distance {} / {}").format(currentX, currentY,
                                                        targetX, targetY,
                                                        distance, angle)
    bot.set_motion_timeout(TIMEOUT)  # how long bot rolls bfore stopping

    if PID:
        outSpeed = 0
        controller = pidController()

    while (distance > stopRadius) \
            and \
            (((time.time() - startTime) < MAX_SECONDS)):

        # Constant of proportional
        if PID:  # PID Controller
            outSpeed = controller.getPIDSpeed(distance, outSpeed)
        else:    # Proportional controller
            outSpeed = distance * Kp
            if outSpeed < 30:
                outSpeed = 33

        # roll the sphero, make use of the request object
        if DEBUG:
            print("Dist {} outSpeed {} at {} degrees: {},{}"
                  .format(distance, outSpeed, angle, currentX, currentY))

        roll_sphero(bot, outSpeed, -angle, offset)

        # use this for recovery when at boundary
        bot.prev_angle = -angle
        time.sleep(sleepTime)

        currentX, currentY = get_bot_position(bot, trace_object,
                                              tracker, samples=2)

        if currentX:
            # Repeat waypointing calculation
            angle, distance = vector_to_target(currentX, currentY,
                                               targetX, targetY)
        else:
            # bring robot back onto screen
            angle = bot.prev_angle
            distance = 100  # aim to go back to middle

    print("Stopped at {},{}, with dist {}").format(currentX, currentY,
                                                   distance)


def vector_to_target(currentX, currentY, targetX, targetY):
    '''
        Returns distance and angle between two points (in degrees)
    '''
    deltaX = targetX - currentX
    deltaY = targetY - currentY
    angle = math.degrees(math.atan2(deltaY, deltaX))
    distance = math.sqrt(deltaX * deltaX + deltaY * deltaY)

    return angle, distance


# Team driving functions
def team_go_to_points(bots, targets, offsets,
                      traceable_object, traceable_color,
                      MAX_X, MAX_Y, tracker,
                      TIMEOUT=200, stopRadius=25, Kp=0.23):
    '''
        Send each bot in the team to its designated point in targets

        :param bot: robot being controlled
        :param targets: A list of (x,y) coordinate pairs
        :param MAX_X: maximum x dimension
        :param MAX_Y: maximum Y dimension
        :param tracker: ColorTracker() object
        :param TIMEOUT: How many milliseconds pass before issuing new command
        :param stopRadius: Pixel distance threshhold before stopping
        :param Kp: Proportional control constant

        :type traceable_object: traceable object in SpheroNav library
        :type traceable_color: RGB list of values

        # Ideas for refactor
        Perhaps each point might have its own Kp or timeout or speed.
    '''

    # Turn each robot's light off before starting
    for bot in bots:
        bot.set_rgb(0, 0, 0)

    for i, bot in enumerate(bots):
        print("Bot {}".format(bot.bt_name))
        bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
        time.sleep(1.5)  # Give camera time to adjust

        targetX, targetY = targets[i]
        bot_go_to_point(bot, offsets[i], targetX, targetY,
                        traceable_object, traceable_color, MAX_X, MAX_Y,
                        tracker, TIMEOUT=200, stopRadius=stopRadius, Kp=Kp)

        bot.set_rgb(0, 0, 0)


def team_go_to_paths(bots, paths, offsets, traceable_object, traceable_color,
                     MAX_X, MAX_Y, tracker, TIMEOUT=200,
                     stopRadius=25, Kp=0.23):
    '''
        Send each bot in the team a list of points

        :param bots: a list of Sphero objets (a SpheroTeam)
        :param paths: A list of lists list of (x,y) coordinate pairs, 1 per bot
        :param MAX_X: maximum x dimension
        :param MAX_Y: maximum Y dimension
        :param tracker: ColorTracker() object
        :param TIMEOUT: How many milliseconds pass before issuing new command
        :param MAX_SECONDS: How many seconds to navigate before quitting
        :param stopRadius: Pixel distance threshhold before stopping
        :param Kp: Proportional control constant
        :param DEBUG: Boolean toggling print statements

        :type traceable_object: traceable object in SpheroNav library
        :type traceable_color: RGB list of values
    '''

    # Start by turning off each robot
    for bot in bots:
        bot.set_rgb(0, 0, 0)

    for i, bot in enumerate(bots):
        print("Bot {}".format(bot.bt_name))
        bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
        time.sleep(1)

        for target in paths[i]:
            targetX, targetY = target
            bot_go_to_point(bot, offsets[i], targetX, targetY,
                            traceable_object, traceable_color,
                            MAX_X, MAX_Y, tracker, TIMEOUT=250,
                            stopRadius=stopRadius, Kp=Kp)

        # Turn robot off when done
        bot.set_rgb(0, 0, 0)
