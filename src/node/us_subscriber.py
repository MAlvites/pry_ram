#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
import math
import numpy as np

def scan_us_callback(scan_data):
    #Find minimum range
    distance = scan_data.range
    print "\nDistancia es: ","{0:.3f}".format(distance) ,"m"
    if distance <= 0.5 :
	print("Alarma : Objeto cercano a robot")

if __name__ == '__main__':
    
    #Inicio del nodo
    rospy.init_node('us_value_node', anonymous=True)
    #Suscrito al topico /Scan
    rospy.Subscriber("ultrasound_data5", Range, scan_us_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
