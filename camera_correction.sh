#!/bin/sh

xterm -title "Radar Module" -e "roslaunch node1_radarinterface node1_radarinterface.launch"&

sleep 1

xterm -title "Image Process" -e "ROS_NAMESPACE=usb_webcam rosrun image_proc image_proc"&

sleep 5

xterm -title "AprilTag Node" -e "roslaunch apriltag_ros continuous_detection.launch"

