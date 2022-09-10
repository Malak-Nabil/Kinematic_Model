#!/usr/bin/env python3
import os
from secrets import choice
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
x=0
y=0
yaw=0
choice=input('Enter f for forward OR b for backward:')
v=float(input('enter velocity:'))
delta=float(input('enter steering angle:'))
t=int(input('enter time of simulation:'))
l_back=rospy.get_param("/l_back")
l_front=rospy.get_param("/l_front")
l_total=l_back+l_front
def takepose(pose_message):
    if choice=='f':
        back_callback(pose_message.theta)
    else:
        front_callback(pose_message.theta)

def front_callback(theta):
    velocity_message = Twist() 
    beta=math.atan((l_front/l_total)*math.tan(delta))
    x=v*math.cos(beta+theta)
    y=v*math.sin(beta+theta)
    w=(v/l_total)*math.tan(delta)*math.cos(beta)   
    velocity_message.linear.x=x
    velocity_message.linear.y=y
    velocity_message.angular.z=w
    velocity_publisher.publish(velocity_message)

def back_callback(theta):
    velocity_message = Twist() 
    beta=delta-(math.atan((l_back/l_total)*math.tan(delta)))
    x=v*math.cos(beta+theta)
    y=v*math.sin(beta+theta)
    w=(v/l_total)*math.cos(delta-beta)*math.tan(delta)
    velocity_message.linear.x=x
    velocity_message.linear.y=y
    velocity_message.angular.z=w
    velocity_publisher.publish(velocity_message)

        
def out2(event):
    rospy.signal_shutdown("stop")

rospy.init_node("back_node", anonymous=True)
velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
rospy.Subscriber("/turtle1/pose", Pose, takepose)
rospy.Timer(rospy.Duration(t),callback=out2)
rospy.spin()
