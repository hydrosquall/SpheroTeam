# Cameron Yick
# Python Class + Example inspired by Matlab's PID controller for sphero
# https://www.mathworks.com/matlabcentral/fileexchange/52481-sphero-connectivity-package
# Will become a higher level api wrapped around sphero that lets user 
# merely specify a set of X,Y coordinates

import time
import math

# PID controller for sphero
class pidController():

    def __init__(self):
        self.isRunning = False
        self.epsilon   = 0.0001 # some small bound? 

    def reset(self):
        self.isRunning = False
        

    # later may find that P controller is sufficient
    # Documentation is here: 
    # headingCMD = desiredHeading + (headingKp*currErrorHeading)
    # velocityCMD = velocityKp*distance
    # http://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlPID
    def getPIDSpeed(self, distance, speed, Kp, Ki, Kd, stopRadius=3, 
                   maxSpeed=150, minSpeed=2, resumeSpeed=50):
        """
            Other variables self explanatory?
            Kp: Proportional controller gain
            Ki: Intergral controller gain
            Kd: Derivative controller gain
            stopRadius: If robot is within this distance of object, try to stop.
            distance: Distance in centimeters between robot and desired point
            resumeSpeed: If robot comes to standstill, this overcomes inertia
        """

        if not self.isRunning:
            self.isRunning = True
            self.prevU = 0
            self.prevE = 0
            self.prevT = 0
            self.prev2E = time.time()
            self.prev2T = time.time()


        # 
        currentT = time.now()
        deltaT   = currentT - self.prevT
        deltaT2  = self.prevT - self.prev2T

        # u is the speed that you return
        # breaking behavior may be different from just turning motor off
        # maybe may need matlab to tune the controller constants
        if distance < stopRadius:
            u = 0
        else:  # Robot too far away, must keep moving!

            # PID equation
            # Make select mode using PID switch
            if (deltaT < self.epsilon) or (deltaT2 < self.epsilon):
                u = self.prevU + Kp * (distance - self.prevE) + Ki*deltaT*distance
            else:
                assert(deltaT != 0)
                assert(deltaT2 != 0)
                u = prevU + Kp * (distance - self.prevE) + Kd * (((distance- self.prevE) / deltaT) - \
                                                                  ((self.prevE - self.prev2E) / deltaT2) )

            # If robot has stopped moving, reset it
            if (speed < 2) and (u < resumeSpeed):
                u = resumeSpeed

        # Update internal vars
        self.prevU = u

        self.prev2E = self.prevE
        self.prevE = distance

        self.prev2T = self.prevT
        self.prevT = currentT

        # Handle saturation
        if (u > maxSpeed):
            return maxSpeed
        elif (u < minSpeed):
            return minSpeed
        else:
            return u


# How to use the pidController:
# Use params from matlab
# research pro cons of PID params
# these will need to be tuned
Kp = 1
Ki = 0.1
Kd = 0.1

# replace with calls to the locator
currentX = 0
currentY = 0
currentSpeed = 0


controller = pidController()

# Basic closed loop controller
startTime = time.time()
# run for 30 seconds
while (time.time() - startTime < 25 ):
    targetX = 30
    targetY = 30

    # Angle to distance
    deltaX = targetX - currentX
    deltaY = targetY - targetX
    angle = math.degrees(math.atan2(deltaY, deltaX ))
    distance = math.sqrt( deltaX * deltaX + deltaY * deltaY )

    while distance > stopRadius:
        outSpeed = controller.getPIDSpeed(distance, currentSpeed, Kp, Ki, Kd)

        # roll the sphero, make use of the request object
        bot.roll(outSpeed, angle)

        # get current speed
        # this can probably be refactored each time
        response = bot.get_locator()  # refactor with call to webcam
        currentX = response.x_pos
        currentY = response.y_pos
        currentSpeed = response.speed? ### lookup this param

        # Repeat waypointing calculation
        deltaX = targetX - currentX
        deltaY = targetY - targetX
        angle = math.degrees(math.atan2(deltaY, deltaX ))
        distance = math.sqrt( deltaX * deltaX + deltaY * deltaY )


# at very end, stop the robot!!
bot.roll(0,0)




