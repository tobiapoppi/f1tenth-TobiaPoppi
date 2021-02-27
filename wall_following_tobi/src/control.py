#!/usr/bin/env python

import rospy
from race.msg import pid_input
from race.msg import drive_param
from ackermann_msgs.msg import AckermannDrive
import math

kp = 0.62 #0.7 
kd = 0.16 #0.00125 #0.09
servo_offset = 0
prev_error = 0.0 
steering_angle = 0.0
vel_prev = 0.0
vel_input = 0.3

pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size=10)

def control(data):
	global prev_error
	global vel_input
	global kp
	global kd
	global steering_angle
	global vel_prev
 	

	if abs(data.pid_error) < 0.003:
		error = 0
	else:
		error = data.pid_error

	v0 = (kp * error) + (kd * (prev_error - error))
	#v0 = (kp * error) + (kd * (prev_error - error))
	vel_input = vel_prev +( 0.022 - 1.4 * math.pow( abs(prev_error - data.pid_error),2))


	steering_angle = prev_error - v0

	if steering_angle < -100:
		steering_angle = -100
	elif steering_angle > 100:
		steering_angle = 100

	prev_error = error

	vel_prev = vel_input

	msgAck = AckermannDrive()
	msgAck.speed = vel_input
	#msgAck.speed = 1
	msgAck.steering_angle = steering_angle
	pub.publish(msgAck)

	print msgAck

if __name__ == '__main__':

	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("/car_1/error", pid_input, control)
	rospy.spin()
