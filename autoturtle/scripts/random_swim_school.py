#!/usr/bin/env python
import rospy
import math
import time
import random
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute

class RandSwimSchool():
    #try to teleport the turtle with rosservice and givng the destination position gave by user.
    posizione = Pose()
    faseiniziale = True
    init_pose = Pose()

    def update_pose(self, data):
        self.posizione.x = round(data.x, 2)
        self.posizione.y = round(data.y, 2)
        if(self.faseiniziale):
            self.init_pose.x = self.posizione.x
            self.init_pose.y = self.posizione.y
            rospy.loginfo("Teleported turtle in position:")
            print 'x: ',self.init_pose.x,'     y: ',self.init_pose.y
            self.faseiniziale  = not self.faseiniziale


    def __init__(self):
        rospy.init_node('SwimSchool', anonymous=False)
        rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        xran = random.uniform(2, 8)
        yran = random.uniform(2, 8)

        teleService = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleService(xran, yran, 0)

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        rate = rospy.Rate(300);

        rospy.loginfo("Set rate 300Hz")
        move_cmd = Twist()

        move_cmd.linear.x = input("Linear velocity: ")
        move_cmd.angular.z = input("Angular velocity: ")
        timetowait = round((2*math.pi)/abs(move_cmd.angular.z), 2)
        print('time to wait = ',timetowait)
        change = False
        start = time.time()

        while not rospy.is_shutdown():

            if change:
                move_cmd.angular.z = -(move_cmd.angular.z)
                change = not change
                start = time.time()

            self.cmd_vel.publish(move_cmd)
            end = time.time()
            delta = end - start

            if ((round(delta, 2) > timetowait-0.5)
              and self.posizione.x >= (self.init_pose.x - 0.05)
              and self.posizione.x <= (self.init_pose.x)
              and self.posizione.y > (self.init_pose.y - 0.1)
              and self.posizione.y < (self.init_pose.y + 0.1)):
                change = not change
                print 'swapping direction'

            rate.sleep()

    def shutdown(self):
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        RandSwimSchool()
    except:
        rospy.loginfo("End of the swim for this Turtle.")
