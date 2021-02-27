Wiki for wall_following-tobi

First, all this repo uses ROS Melodic on Ubuntu 18.04

The f1/10 simulator has to be installed in catkin workspace: https://github.com/f1tenth-dev/simulator

Then, to start the program:

"roslaunch f1tenth-sim simulator.master"
"roslaunch f1tenth-sim racecar.access listen_offboard:=true"
"rosparam set /car_1/command_priority 'SIMULATOR_OFFBOARD'"
"rosrun wall_following_tobi dist_finder.py"
"rosrun wall_following_tobi control.py"
keep pressed W to make the car go autonomously (in the "racecar.access" terminal)

to stop the car:
"rosparam set /car_1/command_priority 'REMOTE_KEYBOARD'"
press Q in the "racecar.access" terminal

to reset car's position:
"rosparam set /car_1/reset_to_pit_stop '1'"
