#!/usr/bin/env python
import rospy
import math
import sys

import std_msgs.msg

from micro_doppler_pkg.msg import MicroDoppler_m

import numpy as np
import matplotlib.pyplot as plt

class MySimpleClass(object):
    def __init__(self):
        self.sub = rospy.Subscriber('/ti_mmwave/micro_doppler',MicroDoppler_m,self.sub_callback)
        self.now_framenum = 0
        self.mds_array   = []

    def sub_callback(self,msg):
        #header
        if self.now_framenum >= 60:
            self.now_framenum = 0

            self.mds_array = np.array(self.mds_array)
            self.mds_array = np.transpose(self.mds_array)
            print(self.mds_array.shape)
            plt.imshow(self.mds_array)
            plt.colorbar()
            plt.show()
            self.mds_array =[]

        nd                  = msg.num_chirps
        time_domain_bins    = msg.time_domain_bins
        mds_data            = np.array(msg.micro_doppler_array).reshape((nd, time_domain_bins))
        self.mds_array.append(mds_data[:, 1])

        self.now_framenum = self.now_framenum +1
        
        

if __name__ == '__main__':
    '''
    Sample code to publish a pcl2 with python
    '''
    rospy.init_node('mds_plot_node')
    rospy.loginfo("plot doppler pattern after 60 frame...")
    #give time to roscore to make the connections
    #rospy.sleep(1.)
    my_simple_class = MySimpleClass()
    rospy.loginfo("happily publishing sample pointcloud.. !")
    rospy.spin()
