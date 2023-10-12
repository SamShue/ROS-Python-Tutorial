#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

min_distance = None

def callback(laser_scan_msg):
	global min_distance
      	if not laser_scan_msg.ranges:
        	return

	min_distance = None
	for distance in laser_scan_msg.ranges:
		if not math.isnan(distance):
			if distance < min_distance or min_distance == None:
				min_distance = distance
  
def wanderer():
	rospy.init_node('wanderer', anonymous=True)
	rospy.Subscriber('scan', LaserScan, callback)
	cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
		twist_cmd = Twist()
		print min_distance

		if min_distance < 0.5:
	    	twist_cmd.angular.z = 1.0

			for i in range(25):
	    		cmd_vel_pub.publish(twist_cmd)
	    		rospy.sleep(0.1)

	    	twist_cmd.angular.z = 0.0
	    	cmd_vel_pub.publish(twist_cmd)
		else:
			twist_cmd.linear.x = 0.25
	    	cmd_vel_pub.publish(twist_cmd)
		
		rate.sleep()

if __name__ == '__main__':
    try:
        wanderer()
    except rospy.ROSInterruptException:
        pass
