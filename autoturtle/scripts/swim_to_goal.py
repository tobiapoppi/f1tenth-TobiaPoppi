#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class SwimToGoal():

    def __init__(self):
        rospy.init_node('SwimToGoal', anonymous = False)
        self.position = Pose()
        msg = rospy.wait_for_message('/turtle1/pose', Pose)
        self.updatePose(msg)
        rospy.Subscriber('/turtle1/pose', Pose, self.updatePose)
        rospy.loginfo('Press CTRL+c to stop moving the turtle')
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        move_cmd = Twist()
        rate = rospy.Rate(100)
        goalx = input('Insert the x coordinate for the goal: ')
        goaly = input('Insert the y coordinate for the goal: ')
        tol = input('Insert a tolerance accepted for the destination: ')
        ciphers = int(math.log10(1/tol))
        goalx = round(goalx, ciphers)
        goaly = round(goaly, ciphers)

        while not rospy.is_shutdown():
            if round(self.position.x, ciphers) != goalx and (self.position.y, ciphers) != goaly:
                dist = math.sqrt(math.pow((goalx - self.position.x), 2) + math.pow((goaly - self.position.y), 2))
                move_cmd.linear.x = 0.7 * dist
                angle_to_goal = (math.atan2(goaly - self.position.y, goalx - self.position.x))
                move_cmd.angular.z = 4 * (angle_to_goal - self.position.theta)
                print round(self.position.x, ciphers) - goalx
                self.cmd_vel.publish(move_cmd)
                rate.sleep()
            else:
                rospy.loginfo('The position reaced is: ')
                print self.position.x, self.position.y
                break

           

    def updatePose(self, msg):
        self.position.x = round(msg.x, 3)
        self.position.y = round(msg.y, 3)
        self.position.theta = msg.theta

    def shutdown(self):
        rospy.loginfo('Stopping the turtle')
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
    

if __name__ == '__main__':
    try:
        SwimToGoal()
    except:
        rospy.loginfo("End of the swim for this turtle.")