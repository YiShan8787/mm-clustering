#!/usr/bin/env python3
import rospy
import math
import sys
import glob
import os
import time

from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2
import numpy as np
from visualization_msgs.msg import Marker

from node1_radarinterface.msg import RadarScan

from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String

import keras
from keras.models import load_model

class MySimpleClass(object):
    def __init__(self):
        #self.voxel_pub = rospy.Publisher("/voxels", numpy_msg(Floats),queue_size = 10)
        #self.data_pro_pub = rospy.Publisher("/data_pro", numpy_msg(Floats),queue_size = 10)
        
        self.radardata = RadarScan()
        
        self.now_framenum = 0
        #store current frame points
        self.nowframe = []
        #store current 60 frames
        self.data =[]
        #store per frame after voxalize
        self.voxels = []
        self.model = load_model('/home/wt/RadHAR/Data/model/LSTM.h5')
        self.test_data = []
        self.finish = 0
        self.predict_result = -1
        self.predict_text = "processing"

        self.marker = Marker()
        self.marker.header.frame_id = "map"
        self.marker.header.stamp    = rospy.Time.now()
        self.marker.ns = "predict"
        self.marker.id = 0

        self.marker.type = self.marker.TEXT_VIEW_FACING
        self.marker.action = self.marker.ADD

        self.marker.scale.x = 1.2
        self.marker.scale.y = 1.2
        self.marker.scale.z = 1.2
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
        self.marker.pose.orientation.w = 1.0
        self.marker.pose.position.x = 0
        self.marker.pose.position.y = 0
        self.marker.pose.position.z = 3
        self.marker.text="recording"
        self.sub = rospy.Subscriber('/node1_radarinterface/radar_scan',RadarScan,self.sub_callback)
        self.marker_pub = rospy.Publisher("/predict_marker", Marker,queue_size = 10)
        self.predict_pub = rospy.Publisher("/predict_result", numpy_msg(Floats),queue_size = 10)
        self.timecost_pub = rospy.Publisher("/time_cost", String,queue_size = 10)

    def sub_callback(self,msg):
        #for marker
        #marker = Marker()
        self.marker.header.stamp    = rospy.Time.now()
        self.marker_pub.publish(self.marker)
        
        #print(len(self.data))
        
            
        if msg.point_id != 0:
            self.nowframe.append([msg.x, msg.y, msg.z, msg.doppler_bin])
        else:
            if len(self.nowframe) >0:
                self.data.append(self.nowframe)
                self.nowframe = []
                if len(self.data) < 61:
                    None
                elif len(self.data) > 61:
                    self.data.pop(0)
                    self.marker.text = "processing"
                    self.transfer()
                else:
                    self.marker.text = "processing"
                    self.transfer()
            self.nowframe.append([msg.x, msg.y, msg.z, msg.doppler_bin])
        
        #if len(self.data) > 61:
        #   self.data.pop(0)
            
        #    if not self.finish:

    def transfer(self):
        #print("start transfer")
        start_time = time.time()
        together_frames = 1
        sliding_frames = 1
        total_frames = 61
        #print(len(self.data[0]))
        i = 0
        j = 0
        data_pro = dict()
        while together_frames+i < total_frames:

            curr_j_data =[]
            for k in range(together_frames):
                curr_j_data = curr_j_data + self.data[i+k]
            #print(len(curr_j_data))
            data_pro[j] = curr_j_data
            j = j+1
            i = i+sliding_frames

        pixels = []
        #print("finish pro1")
        #self.data.pop(0)
        # Now for 2 second windows, we need to club together the frames and we will have some sliding windows
        for i in data_pro:
            f = data_pro[i]
            f = np.array(f)

            #y and z points in this cluster of frames
            #print(f.shape)
            x_c = f[:,0]
            y_c = f[:,1]
            z_c = f[:,2]
            #vel_c=f[:,3]
            doppler_c=f[:,3]

            #pix = voxalize(10, 32, 32, x_c, y_c, z_c, vel_c)
            pix = voxalize(10, 32, 32, x_c, y_c, z_c, doppler_c)
            #print(i, f.shape,pix.shape)
            pixels.append(pix)

        pixels = np.array(pixels)
        #print("finish voxelize")

        frames_together = 60
        tmp_data = []
        local_data = []

        for j in range(frames_together):
            local_data.append(pixels[j])
        tmp_data.append(local_data)    

        self.test_data = np.array(tmp_data)
        #self.voxel_pub.publish(test_data)
        #print(self.test_data.shape)
        #print("finish publish")
        end_time = time.time()
        #print(end_time-start_time)
        self.timecost_pub.publish('%.5f time: %s' %(end_time-start_time,rospy.get_time()))
        self.predict()
        

    def predict(self):
        test_tmp = self.test_data.reshape(self.test_data.shape[0],self.test_data.shape[1], self.test_data.shape[2]*self.test_data.shape[3]*self.test_data.shape[4])
        self.predict_result = self.model.predict(test_tmp)
        #self.predict_text = self.predict_result
        #print(self.predict_result)
        self.predict_pub.publish(self.predict_result[0])
        
        if round(self.predict_result[0,1]):
            self.predict_text = "swing"
        else:
            self.predict_text = "stand"
        self.marker.text = str(self.predict_text)
        

            


def voxalize(x_points, y_points, z_points, x, y, z, velocity):
    x_min = np.min(x)
    x_max = np.max(x)

    y_min = np.min(y)
    y_max = np.max(y)

    z_max = np.max(z)
    z_min = np.min(z)

    z_res = (z_max - z_min)/z_points
    y_res = (y_max - y_min)/y_points
    x_res = (x_max - x_min)/x_points

    pixel = np.zeros([x_points,y_points,z_points])

    x_current = x_min
    y_current = y_min
    z_current = z_min

    x_prev = x_min
    y_prev = y_min
    z_prev = z_min


    x_count = 0
    y_count = 0
    z_count = 0
    #start_time = time.time()
    if x_res==0 or y_res==0 or z_res ==0:
        return pixel
    
    for i in range(y.shape[0]):
        x_count = math.floor((x[i] - x_min)/((x_max - x_min)/x_points))
        if x_count>=x_points:
            x_count = x_count - 1
        y_count = math.floor((y[i] - y_min)/((y_max - y_min)/y_points))
        if y_count>=y_points:
            y_count = y_count - 1
        z_count = math.floor((z[i] - z_min)/((z_max - z_min)/z_points))
        if z_count>=z_points:
            z_count = z_count - 1
        pixel[x_count,y_count,z_count] = pixel[x_count,y_count,z_count] + 1
    
    '''
    for i in range(y.shape[0]):
        x_current = x_min
        x_prev = x_min
        x_count = 0
        done=False

        while x_current <= x_max and x_count < x_points and done==False:
            y_prev = y_min
            y_current = y_min
            y_count = 0
            while y_current <= y_max and y_count < y_points and done==False:
                z_prev = z_min
                z_current = z_min
                z_count = 0
                while z_current <= z_max and z_count < z_points and done==False:
                    if x[i] < x_current and y[i] < y_current and z[i] < z_current and x[i] >= x_prev and y[i] >= y_prev and z[i] >= z_prev:
                        pixel[x_count,y_count,z_count] = pixel[x_count,y_count,z_count] + 1
                        done = True

                        #velocity_voxel[x_count,y_count,z_count] = velocity_voxel[x_count,y_count,z_count] + velocity[i]
                    z_prev = z_current
                    z_current = z_current + z_res
                    z_count = z_count + 1
                y_prev = y_current
                y_current = y_current + y_res
                y_count = y_count + 1
            x_prev = x_current
            x_current = x_current + x_res
            x_count = x_count + 1

    #end_time = time.time()
    #diff = end_time - start_time
    #print(diff)
    '''
    return pixel
        
        

if __name__ == '__main__':
    '''
    Sample code to publish a pcl2 with python
    '''
    
    
    rospy.init_node('voxel_pub_example')
    rospy.loginfo("Initializing sample pcl2 publisher node...")
    
    
    rospy.loginfo("happily publishing sample pointcloud.. !")

    

    

    my_simple_class = MySimpleClass()
    
                
                
    
    
    rospy.spin()
