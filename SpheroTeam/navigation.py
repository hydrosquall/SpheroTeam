# navigation.py
# Cameron Yick
# 4/25/2017

# Functions for figuring out where the robot is, and how to get it oriented
# in the correct direction

import time
import cv2
import logging
import camera

from teamutil import angle_between_points, normalize_angle


# For Navigation
def get_bot_position(bot, traceable_object, tracker, samples=3, DEBUG=False):
    """
        Assumes that bot is visible, return x,y position of that robot

        :param bot: Sphero robot
        :param samples: Number of images to take to determine bot position
        :type traceable_object: TraceableObject() from SpheroNav
        :type tracker: ColorTracker() from SpheroNav
    """
    # xSamples = []
    # ySamples = []

    xSum = 0
    ySum = 0
    nSamples = 0

    for sample in xrange(samples):
        image = tracker.get_video_frame()
        # if sample > 0:  # ignore the first sample

        # side effect: adds mask to tracker
        x, y = tracker._find_traceable_in_image(image, traceable_object)

        # As long as x and y are not none, store both samples.
        if x:
            # xSamples.append(x)
            # ySamples.append(y)
            xSum += x
            ySum += y
            nSamples += 1

    # Left in in case you want to print the actual x,y values stored
    # if DEBUG:
    #     camera.display_current_view(tracker)
    #     print "{} | {} ".format(xSamples, ySamples)

    if nSamples > 0:
        # return (sum(xSamples) / nSamples), (sum(ySamples) / nSamples)
        return xSum / nSamples, ySum / nSamples
    else:
        logging.warning("Robot not in view, make sure it's on?")
        return None, None


def calibrate_bot_direction(bot, traceable_object, traceable_color,
                            tracker, DEBUG=False, TIMEOUT=1500):
    """
        Calculate the angle offset needed to ensure that all robots will roll
        in the same direction

        :param bot: Sphero robot
        :param traceable_object: TraceableObject() from SpheroNav
        :param traceable_color: 3-uple of RGB values corresponding to filter
        :type tracker: ColorTracker() from SpheroNav
    """

    bot.set_rgb(traceable_color[0], traceable_color[1], traceable_color[2])
    bot.set_motion_timeout(TIMEOUT)
    time.sleep(1)  # Give robot time to change

    startX, startY = get_bot_position(bot, traceable_object,
                                      tracker, samples=4)

    cv2.waitKey(250)       # not sure how long this wait has to be

    if (startX is None) or (startY is None):
        print("Error: Robot not in view")
        return -1

    bot.roll(60, 0)  # reconfigure later
    time.sleep(TIMEOUT / 1000)
    endX, endY = get_bot_position(bot, traceable_object, tracker, samples=4)

    offset = normalize_angle(angle_between_points(startX, startY, endX, endY))

    if DEBUG:
        print "Start ({},{})".format(startX, startY)
        print "End   ({},{})".format(endX, endY)
        print "Angle {}".format(offset)

    bot.set_rgb(0, 0, 0)
    return offset


def get_team_offsets(bots, traceable_object, traceable_color, tracker):
    '''
        Return list of angular offset needed to steer each robot in the correct
        direction for every robot in a team. Offsets are in degrees.

        :param bots: List of Sphero objects
        :param traceable_object: TraceableObject() from SpheroNav
        :param traceable_color: 3-uple of RGB values corresponding to filter
        :type tracker: ColorTracker() from SpheroNav
    '''
    offsets = []

    for bot in bots:
        offset = calibrate_bot_direction(bot, traceable_object,
                                         traceable_color, tracker, DEBUG=True)
        offsets.append(offset)
        proceed = raw_input("'q' to quit, else calibrate next robot ")
        if proceed == "q":
            break
        else:
            continue

    return offsets
