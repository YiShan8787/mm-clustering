#!/usr/bin/env python
import rospy
import math
import sys

from geometry_msgs.msg import PoseWithCovarianceStamped
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2

#from apriltag_ros.msg import AprilTagDetection
from apriltag_ros.msg import AprilTagDetectionArray

class MySimpleClass(object):
    def __init__(self):
        self.pose_pub = rospy.Publisher("/my_pose", PoseWithCovarianceStamped,queue_size = 1)
        self.sub = rospy.Subscriber('/tag_detections',AprilTagDetectionArray,self.sub_callback)
        self.rawdata = AprilTagDetectionArray()
        

    def sub_callback(self,msg):
        #header
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'my_bundle'
        pose = PoseWithCovarianceStamped()
        pose = msg.detections[-1].pose
        pose.header = header
        self.pose_pub.publish(msg.detections[-1].pose)
        #print("haha")
        
        

if __name__ == '__main__':
    '''
    Sample code to publish a pose with python
    '''
    rospy.init_node('pcl2_pub_example')
    rospy.loginfo("Initializing sample pose publisher node...")
    #give time to roscore to make the connections
    #rospy.sleep(1.)
    my_simple_class = MySimpleClass()
    rospy.loginfo("happily publishing sample pose.. !")
    rospy.spin()
