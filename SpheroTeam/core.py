# core.py
# Cameron Yick
# 4/24/2017

# A SpheroTeam should inherit the properties of a SpheroManager
# It stores config file information about a SpheroTeam and orchestrates the
# team's movements.
# Prototyped in Notebook #3: Sphero Group Control
# Bluetooth Initial / Closing communication

import time
from util import normalize_angle


# Helper functions for working with sphero class objects
def connect_team(bots):
    for i, bot in enumerate(bots):
        bot.disconnect()  # Kill any previous attempts
        bot.connect()


def disconnect_team(bots):
    for i, bot in enumerate(bots):
        bot.disconnect()


# Light control
# ==============
def set_team_back_led(bots, status):
    # Bright if true, dim if false
    status = 0xaa if status else 0x00
    for bot in bots:
        bot.set_back_led_output(status)


def set_team_colors(bots, colors):
    for i, bot in enumerate(bots):
        colorTriple = colors[i]
        bot.set_rgb(colorTriple[0], colorTriple[1], colorTriple[2])


def highlight_bot(bots, iBot, highlight_color=[255, 0, 0]):
    for i, bot in enumerate(bots):
        if i == iBot:
            bot.set_rgb(highlight_color[0],
                        highlight_color[1],
                        highlight_color[2])
        else:
            bot.set_rgb(0, 0, 0)


def highlight_team(bots, duration=1):
    for i, bot in enumerate(bots):
        highlight_bot(bots, i)
        time.sleep(duration)


# Diagnostics
def print_team_status(bots):
    for bot in bots:
        response = bot.get_power_state()
        print "{}:{} | {} V".format(bot.bt_name,
                                    response.power_state, response.bat_voltage)


# MOVEMENT
def roll_sphero(bot, speed, heading, offset):
    """
        Roll robot towards HEADING at a given speed
    """
    bot.roll(speed, normalize_angle(heading + offset))


def set_team_timeout(bots, motionTimeout=2000):
    """
        How long robot should apply motor force for.
    """
    for bot in bots:
        bot.set_motion_timeout(motionTimeout)


def roll_sphero_team_synchronized(bots, speed, heading, offsets,
                                  motionTimeout=2000):
    """
        Move all robots in same direction at shared speed
    """
    # assert(len(bots) == len(offsets))
    tStart = time.time()
    for i, bot in enumerate(bots):
        roll_sphero(bot, speed, heading, offsets[i])
    tEnd = time.time()
    print("Dispatch Time {}".format(tEnd - tStart))
    time.sleep(motionTimeout / 1000)  # wait for bots to finish rolling
