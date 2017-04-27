# Setup

## Steps to install SpheroNav Libraries

First, clone my [fork](https://github.com/hydrosquall/spheronav) of Simon's Library.

Note this library was developed when the sphero API was version 1.2. Currently (April 2017), the API is at version 1.5. It is not clear what things have broken since then. 

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

ln -s is preferable to making a visible directory link, but mixing unix and windows subsystem could be risky
```bash
# get link to where your python path checks
# Folder name of your symlink must match python package name
# python -c 'import site; site._script()' --user-site
# mklink /D <link> <source>
# Example (Replace link and source with paths on your computer.)

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\SpheroController  C:\Users\cyick\Projects\SpheroNav\SpheroController 

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\sphero C:\Users\cyick\Projects\SpheroNav\sphero

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\util C:\Users\cyick\Projects\SpheroNav\util

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\tracker C:\Users\cyick\Projects\SpheroNav\tracker

mklink /D C:\Users\cyick\AppData\Roaming\Python\Python27\site-packages\ps3 C:\Users\cyick\Projects\SpheroNav\ps3
```

See Troubleshooting section at end if this step creates difficulties.

## Install Extra Dependencies 

These are listed on the [SpheroNav](https://github.com/hydrosquall/spheronav) project page,
but definitely include

- Pybluez
- Kivy
- Opencv 2.4

### Shell Setup

Use virtualenv or Anaconda's environment management tool. Example:

```
    conda create -n SpheroTeam python=2.7
    source activate SpheroTeam
    # First time only, install required libraries
    pip install -r requirements.txt
```

To activate the python environment
```
    source activate SpheroTeam
```

## Troubleshooting

Troubleshooting Links for pypath correction

- [Modifying Path](http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
- [Symlinks in Windows](https://www.howtogeek.com/howto/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)

Coded for a Yale seminar in Intelligent Robotics in Spring 2017 by Cameron Yick
