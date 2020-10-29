#!/usr/bin/env python
import rospy
import math
import sys

from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2

        

if __name__ == '__main__':
    '''
    Sample code to publish a pcl2 with python
    '''
    rospy.init_node('pcl2_pub_example')
    rospy.loginfo("Initializing sample pcl2 publisher node...")
    #give time to roscore to make the connections
    pcl_pub = rospy.Publisher("/my_pcl_topic", PointCloud2,queue_size = 1)
    rate = rospy.Rate(30) # 30hz
    while not rospy.is_shutdown():
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'map'
        cloud_points = [[3.0, 3.0, 1.0]]
        scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points)
        pcl_pub.publish(scaled_polygon_pcl)
        rate.sleep()
    rospy.loginfo("happily publishing sample pointcloud.. !")
    rospy.spin()
