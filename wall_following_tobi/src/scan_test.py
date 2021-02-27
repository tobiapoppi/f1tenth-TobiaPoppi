#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan


def callback(data):

    print "angle min ", data.angle_min, " angle max ", data.angle_max, " increment ", data.angle_increment
    #for i in range(len(data.ranges)):
        #if i < 200 and i > 0:
            #print i, ": ", data.ranges[i], "\n"
        #print i 
    #index = 0 * (len(data.ranges)/270)
    #print len(data.ranges)
    



rospy.init_node("scan_test", anonymous=False)

sub = rospy.Subscriber("/car_1/scan", LaserScan, callback)
rospy.spin()
