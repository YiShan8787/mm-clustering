#!/bin/sh

xterm -title "ros" -e "roslaunch realsense2_camera rs_multiple_devices.launch"&

sleep 4

xterm -title "record bag" -e "cd data/bag/camera_tf_8;rosbag record -a -O raw.bag --duration=11"