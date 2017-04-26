# General Python Helper Functions
import json
import math


# Reading Files
def readJsonFile(filename):
    '''
        Read a JSON file into a python dict

        :param filename: String path to some JSON file
    '''

    with open(filename) as data_file:
        data = json.load(data_file)
    return data


# Doing Math
def normalize_angle(angle):
    """
        Convert angle to angle in degrees from 0 to 360

        :param angle: An angle which may or may not be in valid number range
    """
    if angle < 0:
        return normalize_angle(360 + angle)  # works for domain of arctan2
    elif angle > 360:
        return angle % 360
    else:
        return angle


def angle_between_points(x1, y1, x2, y2):
    """
        Get the angle relative to the x-axis formed by the vector starting at
        (x1, y1) and ending at (x2,y2)

        :param x1: p1.x
        :param y1: p1.y
        :param x2: p2.x
        :param y2: p2.y
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))
