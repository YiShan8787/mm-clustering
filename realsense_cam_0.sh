#!/bin/sh

xterm -title "ros" -e "roscore"&

sleep 1

xterm -title "raw bag" -e "cd data/bag/camera_tf_8;rosbag play -l raw.bag"&

sleep 1

xterm -title "proc" -e "ROS_NAMESPACE=camera1/color rosrun image_proc image_proc"&

sleep 1

xterm -title "apriltag" -e "roslaunch apriltag_ros continuous_detection.launch camera_name:=camera1/color image_topic:=image_rect"&

sleep 1

xterm -title "record bag" -e "cd data/bag/camera_tf_8;rosbag record /tag_detections -O radar_0_tag.bag --duration=10"&

sleep 11

xterm -title "tr bag" -e "cd data/bag/camera_tf_8;rostopic echo -b radar_0_tag.bag /tag_detections > radar_0_tag.txt"