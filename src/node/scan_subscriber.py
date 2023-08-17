#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import math
import numpy as np

def scan_callback(scan_data):
    #Find minimum range
    longitud = len(scan_data.ranges)
    min_value, min_index = min_range_index(scan_data.ranges)
    print "\nMinima distancia es: ","{0:.3f}".format(min_value) ,"m",", con angulo :", "{0:.2f}".format(min_index*field_of_view(scan_data)/longitud)
    

    max_value, max_index = max_range_index(scan_data.ranges)
    print "Maxima distancia es: ", "{0:.3f}".format(max_value) ,"m",", con angulo :", "{0:.2f}".format(max_index*field_of_view(scan_data)/longitud)

    average_value = average_range (scan_data.ranges)
    #print "\nthe average range value is: ", average_value

    average2 = average_between_indices(scan_data.ranges, 2, 7)
    #print "\nthe average between 2 indices is: ", average2

    print "Campo de vision efectivo: ", field_of_view(scan_data)

def field_of_view(scan_data):
    return (scan_data.angle_max-scan_data.angle_min)*180.0/3.14

def min_range_index(ranges):
    return (min(ranges), ranges.index(min(ranges)))

def max_range_index(ranges):
    range_m = np.array(ranges)
    range_m[np.isinf(range_m)]=0
    return (max(range_m), ranges.index(max(range_m)))

def average_range(ranges):
    ranges = [x for x in ranges if not math.isinf(x)]
    return ( sum(ranges) / float(len(ranges)) )

def average_between_indices(ranges, i, j):
    ranges = [x for x in ranges if not math.isinf(x)]
    slice_of_array = ranges[i: j+1]
    return ( sum(slice_of_array) / float(len(slice_of_array)) )


if __name__ == '__main__':
    
    #Inicio del nodo
    rospy.init_node('scan_node', anonymous=True)
    #Suscrito al topico /Scan
    rospy.Subscriber("scan", LaserScan, scan_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
