#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, os
import tty, termios

MAX_LIN_VEL = 1.5
MAX_ANG_VEL = 4.0

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.05
msg = """

Control Manual De Robot
---------------------------
Movimientos:
        w
   a    s    d
        x

w/x : aumentar/disminuir velocidad linear 
a/d : aumentar/disminuir velocidad angular 

s, espacio : parar movimiento

CTRL-C para salir
"""

e = """
Communications Failed
"""

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel,-MAX_LIN_VEL, MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    vel = constrain(vel,-MAX_ANG_VEL,MAX_ANG_VEL)
    return vel

def callback(key_pressed):
    global status
    global target_linear_vel 
    global target_angular_vel 
    global control_linear_vel  
    global control_angular_vel

    k_p=key_pressed.data
    if k_p == 'w' :
        target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
        #status = status + 1
        print(vels(target_linear_vel,target_angular_vel))
        #rospy.loginfo("arriba")
    elif k_p == 'x' :
        target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
        status = status + 1
        print(vels(target_linear_vel,target_angular_vel))
        #rospy.loginfo("abajo")
    elif k_p == 'a' :
        target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
        status = status + 1
        print(vels(target_linear_vel,target_angular_vel))
        #rospy.loginfo("izquierda")
    elif k_p == 'd' :
        target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
        status = status + 1
        print(vels(target_linear_vel,target_angular_vel))
        #rospy.loginfo("derecha")
    elif k_p == ' ' or k_p == 's' :
        target_linear_vel   = 0.0
        control_linear_vel  = 0.0
        target_angular_vel  = 0.0
        control_angular_vel = 0.0
        print(vels(target_linear_vel, target_angular_vel))
        #rospy.loginfo("parar")

status = 0
target_linear_vel   = 0.0
target_angular_vel  = 0.0
control_linear_vel  = 0.0
control_angular_vel = 0.0

if __name__=="__main__":
    print(msg)
    rospy.init_node('teleoperacion',anonymous=True)
    sub = rospy.Subscriber('keys', String, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)  #Frecuencia de 10 HZ
    while not rospy.is_shutdown():
        twist = Twist()
        control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
        twist.linear.x = control_linear_vel
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = control_angular_vel
        pub.publish(twist)
        rate.sleep()
