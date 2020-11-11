#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class SwimSchool():

    posizione = Pose()

    def update_pose(self, data):
        self.posizione.x = round(data.x, 2)
        self.posizione.y = round(data.y, 2)

    def __init__(self):
        rospy.init_node('SwimSchool', anonymous=False)
        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        init_pose = Pose()
        init_pose.x = 5.54
        init_pose.y = 5.54

        rate = rospy.Rate(300);

        rospy.loginfo("Set rate 1Hz")
        move_cmd = Twist()
        move_cmd.linear.x = input("Linear velocity: ")
        move_cmd.angular.z = input("Angular velocity: ")
        timetowait = round((2*math.pi)/abs(move_cmd.angular.z), 2)
        change = False
        start = time.time()
        #check = True
        while not rospy.is_shutdown():
            #print(self.posizione.x, self.posizione.y)
            if change:
                move_cmd.angular.z = -(move_cmd.angular.z)
                change = not change
                start = time.time()
            self.cmd_vel.publish(move_cmd)
            print (self.posizione.x)
            print (self.posizione.y)
            #if check:
                #init_pose.x = self.posizione.x
                #init_pose.y = self.posizione.y
                #print(init_pose.x)
                #print(init_pose.y)
                #check = not check
            end = time.time()
            d = end - start
            if (round(d, 2) > timetowait - 1) and (self.posizione.x >= (init_pose.x - 0.05) and self.posizione.x <= (init_pose.x)) and (self.posizione.y > (init_pose.y - 0.1) and self.posizione.y < (init_pose.y + 0.1)):
                change = not change
            rate.sleep()

    def shutdown(self):
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        SwimSchool()
    except:
        rospy.loginfo("End of the swim for this Turtle.")
