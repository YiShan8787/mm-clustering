#!/bin/sh

xterm -title "ros" -e "roscore"&

sleep 1

xterm -title "raw bag" -e "cd data/bag/camera_tf_8;rosbag play -l raw.bag"&

sleep 1

xterm -title "proc" -e "ROS_NAMESPACE=camera2/color rosrun image_proc image_proc"&

sleep 1

xterm -title "apriltag" -e "roslaunch apriltag_ros continuous_detection.launch camera_name:=camera2/color image_topic:=image_rect"&

sleep 1

xterm -title "record bag" -e "cd data/bag/camera_tf_8;rosbag record /tag_detections -O radar_1_tag.bag --duration=10"&

sleep 11

xterm -title "tr bag" -e "cd data/bag/camera_tf_8;rostopic echo -b radar_1_tag.bag /tag_detections > radar_1_tag.txt"