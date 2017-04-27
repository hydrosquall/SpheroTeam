# pidController.py
# Cameron Yick
# 4/26/2017

# A PID (Proportional Integral Derivative) Controller for Sphero
# Python Class + Example inspired by Matlab's PID controller for sphero

# References
# https://www.mathworks.com/matlabcentral/fileexchange/52481-sphero-connectivity-package
# http://rabiaaslam.com/designing-the-sphero-control-system/
# http://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlPID

import time


class pidController():

    def __init__(self):
        self.isRunning = False
        self.epsilon = 0.1  # some small bound?

    def reset(self):
        self.isRunning = False

    def getPIDSpeed(self, distance, speed, Kp=.23, Ki=.08, Kd=.08,
                    stopRadius=3, maxSpeed=80, minSpeed=20, resumeSpeed=45):

        """
            Returns a speed value (0 - 255) for based on distance to target
            Kp, Ki, and Kd need to be tuned to your floor and robot.

            Kp: Proportional controller gain
            Ki: Integral controller gain
            Kd: Derivative controller gain
            stopRadius: If robot is within this distance of object, stop
            distance: Distance in centimeters between robot and desired point
            resumeSpeed: If robot stops, this speed overcomes inertia
        """

        if not self.isRunning:
            self.isRunning = True
            self.prevU = 0
            self.prev2E = 0
            self.prevE = 0
            self.prev2T = time.time()
            self.prevT = time.time()

        currentT = time.time()
        deltaT = currentT - self.prevT
        deltaT2 = self.prevT - self.prev2T

        # u is the speed that you return
        # breaking behavior may be different from just turning motor off
        # maybe may need matlab to tune the controller constants

        if distance < stopRadius:
            u = 0

        else:  # Robot too far away, must keep moving!

            # PID equation
            # Make select mode using PID switch
            if (deltaT < self.epsilon) or (deltaT2 < self.epsilon):
                u = self.prevU + Kp * (distance - self.prevE) \
                               + Ki * deltaT * distance
            else:
                u = self.prevU + Kp * (distance - self.prevE) \
                               + Ki * deltaT * distance \
                               + Kd * \
                                 (((distance - self.prevE) / deltaT) -
                                  ((self.prevE - self.prev2E) / deltaT2))

            # If robot has stopped moving, reset it
            if (speed < 2) and (u < resumeSpeed):
                u = resumeSpeed

        # Update internal vars
        self.prevU = u

        self.prev2E = self.prevE
        self.prevE = distance
        self.prev2T = self.prevT
        self.prevT = currentT

        print "candidate u: {}".format(u)
        # Handle saturation
        if (u > maxSpeed):
            return maxSpeed
        elif (u < minSpeed):

            return minSpeed
        else:
            return u
