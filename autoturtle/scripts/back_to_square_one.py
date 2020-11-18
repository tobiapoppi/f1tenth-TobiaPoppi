#!/usr/bin/env python
import rospy
from geometry_msgs import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

class Square():
    posizione = Pose()
    faseiniziale = True
    init_pose = Pose()

    # def update_pose(self, data):
    #     self.posizione.x = round(data.x, 2)
    #     self.posizione.y = round(data.y, 2)
    #     if(self.faseiniziale):
    #         self.init_pose.x = self.posizione.x
    #         self.init_pose.y = self.posizione.y
    #         rospy.loginfo("Teleported turtle in position:")
    #         print 'x: ',self.init_pose.x,'     y: ',self.init_pose.y
    #         self.faseiniziale  = not self.faseiniziale


    def __init__(self):
        # rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        # rospy.init_node('SwimSchool', anonymous=False)

        length = input("Input float to determine quare's length")

        # teleService = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        # teleService(xran, yran, 0)

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        rate = rospy.Rate(300);

        rospy.loginfo("Set rate 300Hz")
        move_cmd = Twist()

        while not rospy.is_shutdown():


    def shutdown(self):
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        Square()
    except:
        rospy.loginfo("End of the swim for this Turtle.")
