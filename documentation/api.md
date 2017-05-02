# Development Notes

Documentation for final report

### Development Workflow

Library was developed on a 2016 Microsoft Surface Book with 16 GB RAM, dedicated GPU, and Intel i7 processor running Windows 10. Code was prototyped using a series of Jupyter Notebooks, which is an open-source tool for mixing live code cells with explanatory text. After functionality was refined in the notebooks, critical functions were added as sub-modules to the central SpheroTeam library.

### Modifications to Sphero NAV

Our Sphero TEAM library code depends on heavily on what Simon Nistad wrote for controlling individual Sphero. We added error-handling and retry logic around his base code to enable us to connect to a multiple (a “team”) of spheros from a single function call.

John also added functionality for detecting rectangular objects.

Problems with Onboard Locator

- Tried to use with PID controller 
- Speed parameter from onboard locator service was unrealistic 
  

Key Methods of Sphero TEAM


### Core: Methods for controlling a sphero TEAM. (Methods for controlling individual robots were written too, but are omitted from discussion)

- connect_team / disconnect_team : establish / terminate bluetooth communication with up to 7 robots 
- set_team_back_led: Illuminate “tail” of all robots to assist with human calibration process 
- set_team_colors: Use RGB notation to assign a color to each robot  
- highlight_team: Illuminate each robot in a team one at a time, so that you can see which robot will be receiving new commands first 
- print_team_status: Allows user to assess what is the power state of each robot. Robot will turn off after voltage dips below 7.0. 
- roll_sphero: Move sphero  in a particular heading (in degrees) at a certain drive speed (0 - 255), given an offset heading relative to absolute compass of the arena plane. Actual speed on ground depends on ground friction, current robot voltage 
- set_team_timeout: Specify how long each command to the robot should last for. (I.e. all robots run for 5 seconds before getting new command vs getting run for 1 second). 
- roll_sphero_team_synchronized: Move all robots in same relative direction and at the same spe 
  

Driving Parameters in General

- Lets you specify P, I, D constants 
- Lets you specify what color is being used to track the object 
- Lets you specify how long each command should last for (time duration) 
- Lets you specify what degree of error is tolerated (measured in pixels) 
- Lets you specify speed/heading 
  

### Director:

Library for using camera to send robots to x,y points using P or PID controller using 1 reliably trackable color.

- bot_go_to_point 
    - Robot takes direct path towards target (as opposed to curved, or along grid lines) 
    - User can specify how many samples to use when calculating robot position for varying degrees of navigation accuracy 
    - There is a maximum number of seconds the robot is allowed to attempt to reach point to avoid getting stuck 
    - There is a parameter to specify how frequently the robot should be retracked /given new directions 
    - There is logic for if the robot drives off the tracked area, to try and have it retrace its last steps (invisible wall logic) 

- team_go_to_points: a wrapper around bot_go_to_point. It will send each robot to its own point  in a serial fashion (one after another). 
- team_go_to_paths: a wrapper around bot_go_to_point. Send each robot to visit a series of paths 
  

### Formations - Submodule for blind control

Simple functions for organizing shapes in the form of regular polygons (can specify number of sides)

Encourage people to be creative and come up with new formations, e.g. weaving in shape of letters, curves, etc

Still requires robots to be calibrated to function properly (either by eyeball or by tracker)


### Initialize

Functions that utilize data from a configurable “json” file to increase productivity when beginning any project with spheros

Rather than randomly searching airspace for any spheros you can find, use configuration file to connect directly to spheros you have known before

Took variables that were hard-coded into the original Sphero NAV library, and made those parts modular/separable

### Navigation:

Used color mask + contour finding approach used by Simon to locate each robot’s x,y position

Removed the denoising mask used by Simon because it didn’t improve ability to find robot significantly while adding considerable lag to image processing time

Added “sampling” to average the robot’s position over several frames to reduce the impact of noise

#### Key function:

Get_team_offsets: Generate the angular offsets necessary to drive all robots in a team to have a common orientation 

Get_bot_offset: can be used to redo the angular offset for an individual robot

### pidController

  
Did research on several robotics pid controllers for navigation, including corresponding with a Sphero firmware engineer, Rabia Aslam

Adapted a MATLAB script for PID control of sphero to work in Python

  
### TeamUtil:


General mathematical functions / python file processing functions to simplify usage of other parts of the module.

## Limitations:

  

- Current Sphero API is at version 1.5, Sphero NAV was built on version 1.2. There are a number of functionalities documented on the Orbotix Website  in the Sphero API that neither Simon implemented, nor the official Sphero team wrote functions for in their ROS implementation. 
  

- Sometimes we get error messages about “wrong byte being used in start header”, and it is very hard to tell why this happens (is this due to the changes from 1.2 to 1.5, or is it due to interference in the room)? 
  

- The stuff about why we are presently only using 1 color to track 
    - Tracking 7 objects in every frame is hard 
    - We theorized that we could track 1 object in each frame, but track a different object in each frame 
    - We need to be able to track 7 different colors to be able to move 7 robots simultaneously under PID control 
    - Because we are only tracking 1 color, and to take advantage of robot momentum, we opted to control 1 robot at a time for it’s full journey, rather than having each robot move 1 step and check on status of all other robots. This cuts down on wireless overhead of switching robot light colors at every timestep 

- Our control algorithm only considers target destination and the robot currently moving: robot currently does not concern itself with where the other robots are. So if robot is up against an obstacle or bumps into another robot, it may get “stuck” because it doesn’t know to move around the obstacle.
