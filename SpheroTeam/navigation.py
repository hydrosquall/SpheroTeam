# navigation.py
# Cameron Yick
# 4/25/2017

# Functions for figuring out where the robot is, and how to get it oriented
# in the correct direction

import time
import cv2
import logging
import camera

import math
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

def get_rectangle_position(traceable_object, NUM_SPHEROS=5):
    '''
       Modified a function from John to tell spheros where to go
       relative to a rectangle on the screen

       Temporarily commented out the portions that output image to screen
    '''

    # a NUM_SPHEROS-sized list of tuples for 2D xy coordinates
    # each coordinate corresponds to a different position for a sphero to line up at
    spheroLinePositions = []

    image = self.get_video_frame()

    # UPDATE SCREEN POSITION
    traceable_object.screen_size = self.image_size

    # ------ Scaz Group Addition -------------
    # FIND EDGES OF THE RECTANGULAR BLOCK
    origbox = self._find_largest_rectangle_in_image(image, traceable_object)

    # TRANSLATE INTO PIXEL INTEGERS & DISPLAY
    box = np.int0(origbox)

    # cv2.drawContours(image,[box],0,(0,0,255),2)

    # FIND THE LONGEST EDGE OF THE BLOCK
    longestEdgeLength = 0
    longestEdge = [[0,0], [0, 0]]
    perp_coincident1 = [0, 0]
    perp_coincident2 = [0, 0]
    for x in range(0, 4):
        nextNum = (x + 1) % 4
        x1 = origbox[x][0]
        y1 = origbox[x][1]
        x2 = origbox[nextNum][0]
        y2 = origbox[nextNum][1]
        edgelen = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        # print(edgelen)
        if longestEdgeLength < edgelen:
            longestEdgeLength = edgelen
            longestEdge = np.int0([[x1, y1], [x2, y2]])
            prevNum = (x-1+4) % 4
            nextnextNum = (x+2)%4
            perp_coincident1 = [ origbox[prevNum][0], origbox[prevNum][1] ]
            perp_coincident2 = [ origbox[nextnextNum][0], origbox[nextnextNum][1] ]

    # FIND A PARALLEL LINE SEGMENT TO THE LONGEST EDGE, OUTSIDE THE BLOCK
    diffx1 = longestEdge[0][0] - perp_coincident1[0]
    diffy1 = longestEdge[0][1] - perp_coincident1[1]
    diffx2 = longestEdge[1][0] - perp_coincident2[0]
    diffy2 = longestEdge[1][1] - perp_coincident2[1]
    spheroLineEndpoints = [ (int(longestEdge[0][0] + diffx1), int(longestEdge[0][1] + diffy1)), (int(longestEdge[1][0] + diffx2), int(longestEdge[1][1] + diffy2)) ]

    # print(spheroLineEndpoints)
    # cv2.circle(image, spheroLineEndpoints[0], 5, (0,0,0), -1)
    # cv2.circle(image, spheroLineEndpoints[1], 5, (0,0,0), -1)

    # CREATE POINTS ALONG THIS LINE TO TARGET SPHEROS
    diffx = spheroLineEndpoints[1][0] - spheroLineEndpoints[0][0]
    diffy = spheroLineEndpoints[1][1] - spheroLineEndpoints[0][1]
    percentage_across = 0.0
    if NUM_SPHEROS > 0:
        percentage_across = 1.0 / (NUM_SPHEROS + 1)

    # STORE IN LOCAL ARRAY spheroLinePositions
    for x in range(1, NUM_SPHEROS+1):
        spheroLinePositions.append( (int(spheroLineEndpoints[0][0] + diffx*percentage_across*x), int(spheroLineEndpoints[0][1] + diffy*percentage_across*x)) )

    return spheroLinePositions


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
