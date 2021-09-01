# Maze-Solver
Maze solving algorithm to solve a maze of any size.

## How to run
To run the program, simply download maze-solver.py and it will prompt the user to enter a file name. In the example-mazes, there are 24 example mazes that can be utilized. 
The program will catch the following errors:
* No route from start to end
* File does not exist
* File does not contain a valid maze
* No start/end found

## Creating your own maze
You may create your own maze by following these guidelines: 
* #-Walls
* S-Start
  * There may be multiple start points. The maze solver will change from one to another if there is any that do not work. At the end, the program will delete any unnecessary starts.
* E-End
  * There may be multiple end points. The maze solver will attempt to get to any end point. It will stop at the first end point.

### Notice
This program does not currently use the fastest path as it was a beginner program.
