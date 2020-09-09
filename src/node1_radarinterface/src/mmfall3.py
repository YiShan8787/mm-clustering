#!/usr/bin/env python
import rospy
import math
import sys
import glob
import os

from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2
import numpy as np

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
        
def get_data(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    frame_num_count = -1
    frame_num = []
    x = []
    y = []
    z = []
    velocity = []
    intensity = []
    wordlist = []
    tmp = []
    cloud_points = []

    for x1 in lines:
        for word in x1.split():
            wordlist.append(word)

    length1 = len(wordlist)

    for i in range(0,length1):
        if wordlist[i] == "point_id:" and wordlist[i+1] == "0":
            frame_num_count += 1
            if tmp:
                tmp = []
            if cloud_points:
                
                cloud_points = []
            
        if wordlist[i] == "point_id:":
            frame_num.append(frame_num_count)
        if wordlist[i] == "x:":
            x.append(wordlist[i+1])
        if wordlist[i] == "y:":
            y.append(wordlist[i+1])
        if wordlist[i] == "z:":
            z.append(wordlist[i+1])
        if wordlist[i] == "velocity:":
            velocity.append(wordlist[i+1])
        if wordlist[i] == "intensity:":
            intensity.append(wordlist[i+1])
            
    
            
    '''
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    frame_num = np.asarray(frame_num)
    velocity = np.asarray(velocity)
    intensity = np.asarray(intensity)

    x = x.astype(np.float)
    y = y.astype(np.float)
    z = z.astype(np.float)
    velocity = velocity.astype(np.float)
    intensity = intensity.astype(np.float)
    frame_num = frame_num.astype(np.int)

    
    data = dict()

    for i in range(len(frame_num)):
        if int(frame_num[i]) in data:
            data[frame_num[i]].append([x[i],y[i],z[i],velocity[i],intensity[i]])
        else:
            data[frame_num[i]]=[]
            data[frame_num[i]].append([x[i],y[i],z[i],velocity[i],intensity[i]])

    data_pro1 = dict()

    # Merging of frames together with sliding of  frames
    together_frames = 1
    sliding_frames = 1

    #we have frames in data
    frames_number = []
    for i in data:
        frames_number.append(i)

    frames_number=np.array(frames_number)
    total_frames = frames_number.max()

    i = 0
    j = 0

    while together_frames+i < total_frames:

        curr_j_data =[]
        for k in range(together_frames):
            curr_j_data = curr_j_data + data[i+k]
        #print(len(curr_j_data))
        data_pro1[j] = curr_j_data
        j = j+1
        i = i+sliding_frames

    pixels = []

    # Now for 2 second windows, we need to club together the frames and we will have some sliding windows
    for i in data_pro1:
        f = data_pro1[i]
        f = np.array(f)

        #y and z points in this cluster of frames
        x_c = f[:,0]
        y_c = f[:,1]
        z_c = f[:,2]
        vel_c=f[:,3]

        #pix = voxalize(10, 32, 32, x_c, y_c, z_c, vel_c)
        #print(i, f.shape,pix.shape)
        #pixels.append(pix)

    pixels = np.array(pixels)

    frames_together = 60
    sliding = 10

    train_data=[]

    i = 0
    while i+frames_together<=pixels.shape[0]:
        local_data=[]
        for j in range(frames_together):
            local_data.append(pixels[i+j])

        train_data.append(local_data)
        i = i + sliding

    train_data = np.array(train_data)

    del x,y,z, velocity, data, data_pro1, pixels

    return train_data'''

def parse_RF_files(parent_dir, sub_dirs, file_ext='*.txt'):
    print(sub_dirs)
    features =np.empty((0, 60, 10, 32, 32) )
    #features =np.empty((60, 10, 32, 32) )
    labels = []

    for sub_dir in sub_dirs:
        files=sorted(glob.glob(os.path.join(parent_dir,sub_dir, file_ext)))
        #print(files)
        for fn in files:
            print(fn)
            print(sub_dir)
            train_data = get_data(fn)
            features=np.vstack([features,train_data])


            for i in range(train_data.shape[0]):
                labels.append(sub_dir)
            print(features.shape,len(labels))

            del train_data

    #return features, labels
        

if __name__ == '__main__':
    '''
    Sample code to publish a pcl2 with python
    '''
    parent_dir = '/home/wt/RadHAR/Data/Topic'
    sub_dirs=['walk']
    #extract_path = '/home/wt/RadHAR/Data/extract/Train_Data_voxels_'
    
    rospy.init_node('pcl2_pub_example')
    rospy.loginfo("Initializing sample pcl2 publisher node...")
    rate = rospy.Rate(30) # 30hz
    
    pcl_pub = rospy.Publisher("/my_pcl_topic", PointCloud2,queue_size = 1)
    rospy.loginfo("happily publishing sample pointcloud.. !")
    while not rospy.is_shutdown():
        for sub_dir in sub_dirs:
            print(sub_dirs)
            for sub_dir in sub_dirs:
                files=sorted(glob.glob(os.path.join(parent_dir,sub_dir, "*.txt")))
                for fn in files:
                    print(fn)
                    print(sub_dir)
                    with open(fn) as f:
                        lines = f.readlines()
                
                    frame_num_count = -1
                    frame_num = []
                    x = []
                    y = []
                    z = []
                    velocity = []
                    intensity = []
                    wordlist = []
                    tmp = []
                    cloud_points = []
                    
                    header = std_msgs.msg.Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = 'map'
                    
                    for x1 in lines:
                        for word in x1.split():
                            wordlist.append(word)
                
                    length1 = len(wordlist)
                
                    for i in range(0,length1):
                        if wordlist[i] == "point_id:" and wordlist[i+1] == "0":
                            frame_num_count += 1
                            if cloud_points:
                                scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points)
                                pcl_pub.publish(scaled_polygon_pcl)
                                cloud_points = []
                                print(frame_num_count)
                                rate.sleep()
                        if wordlist[i] == "point_id:":
                            frame_num.append(frame_num_count)
                        if wordlist[i] == "x:":
                            x.append(wordlist[i+1])
                            tmp = []
                            tmp.append(int(float(wordlist[i+1])))
                        if wordlist[i] == "y:":
                            y.append(wordlist[i+1])
                            tmp.append(int(float(wordlist[i+1])))
                        if wordlist[i] == "z:":
                            z.append(wordlist[i+1])
                            tmp.append(int(float(wordlist[i+1])))
                            cloud_points.append(tmp)
                        if wordlist[i] == "velocity:":
                            velocity.append(wordlist[i+1])
                        if wordlist[i] == "intensity:":
                            intensity.append(wordlist[i+1])
                #train_data = get_data(fn)
        rospy.loginfo("end")
                
                
    #give time to roscore to make the connections
    #rospy.sleep(1.)
    #my_simple_class = MySimpleClass()
    
    rospy.spin()
