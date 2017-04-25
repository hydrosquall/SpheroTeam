# formations.py
# Cameron Yick
# 4/24/2017
# Rehearsed patterns of behavior for arbitrary numbers of robots
# These patterns can be executed without a camera present.
from core import roll_sphero_team_synchronized, set_team_timeout


def roll_polygon(bots, nSides, offsets, heading, speed=60, TIMEOUT=1500):
    '''
        Roll spheros in the shape of regular polygon with nSides sides
        Side length is determined by how long the robot rolls for (TIMEOUT)
        New commands are issued every TIMEOUT seconds.

        Pushing can be expressed as a polygon with 1 side!

        :param nSides: Number of sides in a polygon
        :param speed: 0-256 speed value accepted by sphero
        :param heading: 0-359 heading of the first side of the polygon
        :param offsets: Offsets angles for each robot in degrees

        :type nSides: integer
        :type speed: integer
        :type heading: float
        :type offsets: List of positive degree values between 0 and 360
    '''
    angles = [i * (360 / nSides) + heading for i in range(nSides)]
    set_team_timeout(bots, TIMEOUT)
    for angle in angles:
        roll_sphero_team_synchronized(bots, speed, angle, offsets, TIMEOUT)


def roll_push(bots, heading, speed, offsets, TIMEOUT=1500):
    '''
        Roll spheros in the same direction at same speed for common time

        Pushing can be expressed as a polygon with 1 side!
    '''

    set_team_timeout(bots, TIMEOUT)
    roll_sphero_team_synchronized(bots, speed, heading, offsets, TIMEOUT)
