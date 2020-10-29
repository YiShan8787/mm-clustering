#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -l front.bag;"&

sleep 1

xterm -title "Record2 Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -l left.bag /node1_radarinterface/radar_scan:=/node1_radarinterface/radar_scan2 /usb_webcam/image_raw:=/usb_webcam/image_raw2;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "bridge Node" -e "roslaunch rosbridge_server rosbridge_websocket.launch"&

sleep 1

xterm -title "TF bridge Node" -e "rosrun tf2_web_republisher tf2_web_republisher"
