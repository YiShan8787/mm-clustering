#!/usr/bin/env python
import rospy
import math
import sys

from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2

from node1_radarinterface.msg import RadarScan

class MySimpleClass(object):
    def __init__(self):
        self.pcl_pub = rospy.Publisher("/my_pcl_topic", PointCloud2,queue_size = 1)
        self.sub = rospy.Subscriber('/node1_radarinterface/radar_scan',RadarScan,self.sub_callback)
        self.radardata = RadarScan()
        self.now_framenum = 0
        self.cloud_points = []

    def sub_callback(self,msg):
        #header
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'map'
        #create pcl from points
        #cloud_points = [[1.0, 1.0, 0.0],[1.0, 2.0, 0.0]]
        if self.now_framenum == msg.frame_num:
            tmp = []
            tmp.append(msg.x)
            tmp.append(msg.y)
            tmp.append(msg.z)
            self.cloud_points.append(tmp)
        else:
            self.now_framenum = msg.frame_num
            self.cloud_points = []
            tmp = []
            tmp.append(msg.x)
            tmp.append(msg.y)
            tmp.append(msg.z)
            self.cloud_points.append(tmp)
        scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, self.cloud_points)
        #publish    
        self.pcl_pub.publish(scaled_polygon_pcl)
        #self.radardata = msg
        

if __name__ == '__main__':
    '''
    Sample code to publish a pcl2 with python
    '''
    rospy.init_node('pcl2_pub_example')
    rospy.loginfo("Initializing sample pcl2 publisher node...")
    #give time to roscore to make the connections
    #rospy.sleep(1.)
    my_simple_class = MySimpleClass()
    rospy.loginfo("happily publishing sample pointcloud.. !")
    rospy.spin()
