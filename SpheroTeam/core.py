# core.py
# Cameron Yick
# 4/24/2017

# A SpheroTeam should inherit the properties of a SpheroManager
# It stores config file information about a SpheroTeam and orchestrates the
# team's movements.
# Prototyped in Notebook #3: Sphero Group Control
# Bluetooth Initial / Closing communication

import time
from teamutil import normalize_angle


# Helper functions for working with sphero class objects
def connect_team(bots, RETRIES=3, DELAY=1):
    '''
        Connect to all specified robots

        :param bots: List of Sphero Objects
        :param RETRIES: Number of times to reattempt connecting to robot
        :param DELAY: Number of seconds to wait between retries
    '''
    for i, bot in enumerate(bots):
        bot.disconnect()  # Kill any previous running connection threads

        for j in range(RETRIES):
            try:
                bot.connect()
            except Exception as ex:
                template = "An exception of type {0} occurred. Args:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                bot.disconnect()
                time.sleep(DELAY)


def disconnect_team(bots):
    '''
        Disconnect from all robots

        :param bots: List of Sphero Objects
    '''
    for i, bot in enumerate(bots):
        bot.disconnect()


# Light control
# ==============
def set_team_back_led(bots, status):
    """
    :param bots: List of Sphero objects
    :param status: If true, back led turns on for all robots
    :type status: Boolean
    """
    # Bright if true, dim if false
    status = 0xaa if status else 0x00
    for bot in bots:
        bot.set_back_led_output(status)


def set_team_colors(bots, colors):
    """
        Assign a color to each robot, colors usually provided in config.json

        :param bots: List of Sphero Objects
        :param colors: List of 3-uple RGB values
    """
    for i, bot in enumerate(bots):
        colorTriple = colors[i]
        bot.set_rgb(colorTriple[0], colorTriple[1], colorTriple[2])


def highlight_bot(bots, iBot, highlight_color=[255, 0, 0]):
    """
        Light up 1 target robot and turn off all other robots
        By default, makes target robot red

        :param bots: List of Sphero Objects
        :param iBot: Index of the bot you want to highlight, < len(bots)
        :param highlight_color: 3-uple RGB value of the color to highligh with
    """
    for i, bot in enumerate(bots):
        if i == iBot:
            bot.set_rgb(highlight_color[0],
                        highlight_color[1],
                        highlight_color[2])
        else:
            bot.set_rgb(0, 0, 0)


def highlight_team(bots, duration=1):
    """
        Light up 1 robot at a time

        :param bots: List of Sphero Objects
        :param duration: Time to wait in between highlights, in seconds
    """
    for i, bot in enumerate(bots):
        highlight_bot(bots, i)
        time.sleep(duration)


# Diagnostics
def print_team_status(bots):
    '''
        Prints out the power status of all robots

        :param bots: List of Sphero Objects
    '''
    for bot in bots:
        response = bot.get_power_state()
        print "{}:{} | {} V".format(bot.bt_name,
                                    response.power_state, response.bat_voltage)


# MOVEMENT
def roll_sphero(bot, speed, heading, offset):
    """
        Roll robot towards HEADING at a given speed

        :param bot: Sphero object
        :param speed: 0-255 speed value sent to sphero
        :param heading: 0-359 degree direction to send sphero in
        :param offset: corrective angle for proper steering
    """
    bot.roll(speed, normalize_angle(heading + offset))


def set_team_timeout(bots, motionTimeout=2000):
    """
        How long robot should apply motor for.

        :param bots: List of Sphero Objects
        :param motionTimeout: Duration in milliseconds
    """
    for bot in bots:
        bot.set_motion_timeout(motionTimeout)


def roll_sphero_team_synchronized(bots, speed, heading, offsets,
                                  motionTimeout=2000):
    """
        Move all robots in same relative direction at common speed

        Also prints how long it takes to send all the commands.

        :param bots: List of Sphero object
        :param speed: 0-255 speed value sent to sphero
        :param heading: 0-359 degree direction to send sphero in
        :param offsets: lists of corrective angle for proper steering
    """

    tStart = time.time()
    for i, bot in enumerate(bots):
        roll_sphero(bot, speed, heading, offsets[i])
    tEnd = time.time()
    print("Dispatch Time {}".format(tEnd - tStart))
    time.sleep(motionTimeout / 1000)  # wait for bots to finish rolling
