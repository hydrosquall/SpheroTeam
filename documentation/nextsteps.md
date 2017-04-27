### Next Steps
#### Challenges to overcome for better pushing: 

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