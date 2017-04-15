

# Setup

Cross your fingers and be persistent!


## Install Sphero Client

- For now, just use the Tordensky base class
- Revise later with the new methods from 1.2 to 1.5
- Lots of issues when piloting more than 2 at once.

For now, dumping `requirements.txt`... refine this later with a dedicate conda environment.
- pybluez

## Install SpheroNav Library

-- Tentatively Deprecated, to be determined --

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

ln -s might be preferable to making a visible directory link, but mixing unix and windows subsystem could be dicey.
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

Troubleshooting Links
- [Modifying Path](http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
- [Symlinks in Windows](https://www.howtogeek.com/howto/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)


## Install Extra Dependencies

### First time
```
    conda create -n SpheroTeam python=2.7
```

### Ongoing
```
    source activate SpheroTeam
```

### Issue with PID

The units for the speed and position are very different when the bot is rolling
E.g. thinks it's moving at 600 cm / second ground speed (sog)

So we are dependent on the camera for getting proper feedback

also a few of the bots have some big issues (red firmware blinking)
