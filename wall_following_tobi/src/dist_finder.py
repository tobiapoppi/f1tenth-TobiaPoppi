#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

angle_range = 270		
car_length = 1.5	
desired_trajectory = 1
vel = 20
error = 0.0

pub = rospy.Publisher('/car_1/error', pid_input, queue_size=10)


def getRange(data,theta):

	index = (theta + 40) * (len(data.ranges)/270)
	if math.isnan(data.ranges[int(index)]) or math.isinf(data.ranges[int(index)]):
		return 30
	else:
		return data.ranges[int(index)]

def callback(data):

	theta = 40
	a = getRange(data,theta) 
	b = getRange(data,0)
	thetaR = math.radians(theta)


	AC = 7.0
	alpha = math.atan((a * math.cos(thetaR) - b) / (a * math.sin(thetaR)))
	AB = b * math.cos(alpha)
	CD = AB + AC * math.sin(alpha)
	error = desired_trajectory - CD
	print "AB:", AB, "CD:", CD, "errore:", error


	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel	
	pub.publish(msg)
	print msg
	

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("/car_1/scan",LaserScan,callback)

	rospy.spin()
