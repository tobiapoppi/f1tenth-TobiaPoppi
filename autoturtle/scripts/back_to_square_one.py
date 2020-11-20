#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from turtlesim.msg import Color
from std_srvs.srv import Empty

class Square():
    posizione = Pose()

    def changeBackground(self):
        rospy.wait_for_service('/clear')
        try:
            rospy.set_param('/turtlesim/background_r', 255)
            rospy.set_param('/turtlesim/background_g', 50)
            rospy.set_param('/turtlesim/background_b', 50)
            changeCol = rospy.ServiceProxy('/clear', Empty)
            changeCol()

        except rospy.ServiceException as e:
            rospy.loginfo('Service failed with the exception {e}')


    def update_pose(self, data):
        self.posizione.x = round(data.x, 3)
        self.posizione.y = round(data.y, 3)

    def rotate(self, count):
        if count == 1:
            self.move_cmd.linear.x = 0
            self.move_cmd.linear.y = 2
        if count == 2:
            self.move_cmd.linear.x = -2
            self.move_cmd.linear.y = 0
        if count == 3:
            self.move_cmd.linear.x = 0
            self.move_cmd.linear.y = -2
        if count == 0:
            self.move_cmd.linear.x = 2
            self.move_cmd.linear.y = 0

    def __init__(self):

        rospy.init_node('turtle_Square', anonymous=False)

        length = input("Input float to determine square's length: ")
        self.changeBackground()

        killService = rospy.ServiceProxy('/kill', Kill)
        spawnService = rospy.ServiceProxy('/spawn', Spawn)
        killService('turtle1')
        spawnService(1, 1, 0, 'turtle1')

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        rate = rospy.Rate(300);

        rospy.loginfo("Set rate 300Hz")
        self.move_cmd = Twist()
        self.rotate(0)
        self.move_cmd.angular.z = 0

        rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        isX = True
        count = 0

        rospy.loginfo("Starting in 3..2..1..")
        rospy.sleep(3)

        while not rospy.is_shutdown():
            if isX:
                scarto0 = 0
                scarto2 = 0
                if count == 0:
                    scarto0 = (self.posizione.x - 1)
                else:
                    scarto2 = (self.posizione.x - 1 - length)
                start = time.time()
                travelled = 0 #distance travelled right now

                while ((self.posizione.x) <= (length + 1 + scarto2)) and ((self.posizione.x) >= ( 1 + scarto0)):
                    self.cmd_vel.publish(self.move_cmd)
                    end = time.time()
                    travelled = travelled + abs(self.move_cmd.linear.x * (end - start))
                    start = time.time()
                    left = length - travelled #strada rimasta da percorrere
                    if left <= (length*20/100):
                        if abs(self.move_cmd.linear.x) > 0.3:
                            x = (left*100)/(length*20/100)
                            self.move_cmd.linear.x = (self.move_cmd.linear.x * x)/100
                    rate.sleep()
            else:
                scarto1 = 0
                scarto3 = 0
                if count == 1:
                    scarto1 = (self.posizione.y - 1)
                else:
                    scarto3 = (self.posizione.y - 1 - length)
                start = time.time()
                travelled = 0 #distance travelled right now
                while ((self.posizione.y) <= (length + 1 + scarto3)) and ((self.posizione.y) >= (1 + scarto1)):
                    self.cmd_vel.publish(self.move_cmd)
                    end = time.time()
                    travelled = travelled + abs(self.move_cmd.linear.y * (end - start))
                    start = time.time()
                    left = length - travelled #strada rimasta da percorrere
                    if left <= (length*20/100):
                        if abs(self.move_cmd.linear.y) > 0.3:
                            x = (left*100)/(length*20/100)
                            self.move_cmd.linear.y = (self.move_cmd.linear.y * x)/100
                    rate.sleep()
            print self.posizione.x, self.posizione.y
            isX = not isX
            if count == 3:
                count = 0
            else:
                count += 1
            self.rotate(count)

    def shutdown(self):
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        Square()
    except:
        rospy.loginfo("End of the swim for this Turtle.")
