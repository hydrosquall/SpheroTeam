# General Python Helper Functions
import json
import math


# Reading Files
def readJsonFile(filename):
    '''
        Read a JSON file into a python dict
    '''

    with open(filename) as data_file:
        data = json.load(data_file)
    return data


# Doing Math
def normalize_angle(angle):
    """
        Convert angle to angle in degrees from 0 to 360
    """
    if angle < 0:
        return normalize_angle(360 + angle)
    elif angle > 360:
        return angle % 360
    else:
        return angle


def angle_between_points(x1, y1, x2, y2):
    """
        Get the angle relative to the x-axis formed by the vector starting at
        (x1, y1) and ending at (x2,y2)
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))
