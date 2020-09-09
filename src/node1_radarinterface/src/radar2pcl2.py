#!/usr/bin/env python
import rospy
import math
import sys
import struct

from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2
from std_msgs.msg import Header

import numpy as np

from node1_radarinterface.msg import RadarScan

class MySimpleClass(object):
    def __init__(self):
        self.pcl_pub = rospy.Publisher("/my_pcl_topic", PointCloud2,queue_size = 1)
        self.sub = rospy.Subscriber('/node1_radarinterface/radar_scan',RadarScan,self.sub_callback)
        self.radardata = RadarScan()

    def sub_callback(self,msg):
        #header
        #header = std_msgs.msg.Header()
        #header.stamp = rospy.Time.now()
        #header.frame_id = 'map'
        #create pcl from points
        cloud_points = np.array([[1.0, 1.0, 0.0],[1.0, 2.0, 0.0]])
        colors = np.array([[0,0,0],[0,0,0]])
        msg =  xyzrgb_array_to_pointcloud2(cloud_points,colors,rospy.Time.now(),'map')
        '''
        points = []
        lim = 8
        for i in range(lim):
            for j in range(lim):
                for k in range(lim):
                    x = float(i) / lim
                    y = float(j) / lim
                    z = float(k) / lim
                    r = int(x * 255.0)
                    g = int(y * 255.0)
                    b = int(z * 255.0)
                    a = 255
                    #print r, g, b, a
                    rgb = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]
                    #print hex(rgb)
                    pt = [x, y, z, rgb]
                    points.append(pt)

        fields = [PointField('x', 0, PointField.FLOAT32, 1),
                PointField('y', 4, PointField.FLOAT32, 1),
                PointField('z', 8, PointField.FLOAT32, 1),
                # PointField('rgb', 12, PointField.UINT32, 1),
                PointField('rgba', 12, PointField.UINT32, 1),
                ]

        #print points

        header = Header()
        header.frame_id = "map"
        pc2 = point_cloud2.create_cloud(header, fields, points)

        
        pc2.header.stamp = rospy.Time.now()
        #pcl_pub.publish(pc2)
        '''


        #scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points)
        #publish    
        self.pcl_pub.publish(msg)
        #self.radardata = msg
        
def xyzrgb_array_to_pointcloud2(points, colors, stamp=None, frame_id=None, seq=None):
    '''
    Create a sensor_msgs.PointCloud2 from an array
    of points.
    '''
    msg = PointCloud2()
    assert(points.shape == colors.shape)

    buf = []

    if stamp:
        msg.header.stamp = stamp
    if frame_id:
        msg.header.frame_id = frame_id
    if seq: 
        msg.header.seq = seq
    if len(points.shape) == 3:
        msg.height = points.shape[1]
        msg.width = points.shape[0]
    else:
        N = len(points)
        xyzrgb = np.array(np.hstack([points, colors]), dtype=np.float32)
        msg.height = 1
        msg.width = N

    msg.fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
        PointField('r', 12, PointField.FLOAT32, 1),
        PointField('g', 16, PointField.FLOAT32, 1),
        PointField('b', 20, PointField.FLOAT32, 1)
    ]
    msg.is_bigendian = False
    msg.point_step = 24
    msg.row_step = msg.point_step * N
    msg.is_dense = True; 
    msg.data = xyzrgb.tostring()

    return msg 


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
