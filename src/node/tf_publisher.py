#!/usr/bin/env python
import tf
import rospy

if __name__ == '__main__':

  rospy.init_node('tf_brodcaster')

  # blink is a contraction of base link
  base_blink = tf.TransformBroadcaster()
  camera_blink = tf.TransformBroadcaster()
  rplidar_blink = tf.TransformBroadcaster()


  rate = rospy.Rate(50)

  while not rospy.is_shutdown():

    camera_blink.sendTransform((0.1, 0.00, 0.336),
        tf.transformations.quaternion_from_euler(0, 0, 0),
        rospy.Time.now(),"realsense_frame","base_link")

    rplidar_blink.sendTransform((0.0656, 0.00, 0.031),
        tf.transformations.quaternion_from_euler(0, 0, 0),
        rospy.Time.now(),"rplidar_frame","base_link")

    rate.sleep()
