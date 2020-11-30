#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -l front.bag;"&

sleep 1

xterm -title "Record2 Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -l left.bag /node1_radarinterface/radar_scan:=/node1_radarinterface/radar_scan2 /usb_webcam/image_raw:=/usb_webcam/image_raw2;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2_2.py"&

sleep 1

xterm -title "bridge Node" -e "roslaunch rosbridge_server rosbridge_websocket.launch"&

sleep 1

xterm -title "TF map1" -e "rosrun tf static_transform_publisher 0.0769366955335 -0.188204475001 0.569669749349 0.724123518945 0.651235853023 0.207721676636 -0.09158983624049999 map map1 100"&

sleep 1

xterm -title "TF map2" -e "rosrun tf static_transform_publisher 0.188204475001 0.07693669553349995 0.5696697493489999 0.972525938487044 -0.051539362838305736 0.0821176118553319 -0.21164520044217777 map map2 100"&

sleep 1

xterm -title "TF bridge Node" -e "rosrun tf2_web_republisher tf2_web_republisher"

