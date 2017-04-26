

# Setup

## Install Sphero Client

- For now, just use the Tordensky base class
- Revise later with the new sphero APIS from 1.2 to 1.5
- Lots of issues when piloting more than 2 at once.

## Install SpheroNav Library

-- Tentatively Deprecated, to be determined --

First, clone my [fork](https://github.com/hydrosquall/spheronav) of Simon's Library.

### Linux / UNIX Subsystem

This feels the most portable. Add the following to `.bashrc`.

```
# Example to install files at <filepath>:
#PYTHONPATH=$PYTHONPATH:/c/Users/cyick/Projects/SpheroNav
#PYTHONPATH=$PYTHONPATH
PYTHONPATH=$PYTHONPATH:<filepath>
```

### Windows

Run in elevated command prompt (cmd) for each library you might use. Decide whether
it's more disruptive to create symlinks or to modify the python path.

ln -s is preferable to making a visible directory link, but mixing unix and windows subsystem could be dicey.
```bash
# get link to where your python path checks
# Folder name of your symlink must match python package name
# python -c 'import site; site._script()' --user-site
# mklink /D <link> <source>

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\SpheroController  C:\Users\cyick\Projects\SpheroNav\SpheroController 

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\sphero C:\Users\cyick\Projects\SpheroNav\sphero

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\util C:\Users\cyick\Projects\SpheroNav\util

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\tracker C:\Users\cyick\Projects\SpheroNav\tracker

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\ps3 C:\Users\cyick\Projects\SpheroNav\ps3
```

## Install Extra Dependencies 

These are listed on the [SpheroNav](https://github.com/hydrosquall/spheronav) project page,
but definitely include

- Pybluez
- Kivy
- Opencv 2.4

## Usage

```
    import SpheroTeam
```

See `.ipynb` files for example application of the SpheroTeam library.

### Setup

Use virtualenv or Anaconda's environment management tool. Example is provided here

```
    conda create -n SpheroTeam python=2.7
    source activate SpheroTeam
    # First time only, install required libraries
    pip install -r requirements.txt
```

To activate 
```
    source activate SpheroTeam
```

### Sphero Care

- Spheros are officially rated for 1 hour of playtime on full charge, but
if you're not driving them continuously, you can make them last longer
- Spheros will automatically turn off when their voltage dips below 7.0 V
- Spheros cannot be overcharged, according to Sphero FAQ the chargers automatically shut off when the battery is full.

### Next Steps

#### Challenges: 

- Path planning is not the same thing as simply choosing to arrive at a point.
    - Need to come up with algorithm to avoid obstacles, knowing that you may miss goal points by 10-20 centimeters (fuzzy logic)
- Tuning the right KP parameter is tricky
- Coming up with recovery paths is tricky
- How to stop robots from bumping into each other
- When robot runs out of bounds, we can't see it... need to create a "fence" around the arena and that would fix it.

- Tracker can only reliably "see" 1 color at once, so workaround is only using that 1 color for tracking. Ideally could track multiple colors at once.

#### Path Forward

- Alternate control idea
    - When swarm needs to converge on 1 point: have everyone drive at fixed speed
    - drive for however long that distance takes in pixels
    - Let everyone drive simultaneously by giving each robot a blind directive, and not using any feedback to tune its behavior (aka a "formation")
- Write a function that given a singular (x,y) point, generates a list of pixels that each robot would aim for, along with an "shape" and relevant parameters for how the robots should be arranged (aka box, line, circle, hexagon, etc)
- Write a function that given a singular target (x,y) point and a robot, define a list of points that the robot should visit before reaching the target points

### Troubleshooting

Troubleshooting Links for path correction

- [Modifying Path](http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
- [Symlinks in Windows](https://www.howtogeek.com/howto/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)
