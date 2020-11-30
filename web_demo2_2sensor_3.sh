#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd data/bag/camera_tf_3; rosbag play -l 2sensor_2tag_raw.bag;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2_2.py"&

sleep 1

xterm -title "bridge Node" -e "roslaunch rosbridge_server rosbridge_websocket.launch"&

sleep 1

xterm -title "TF map1" -e "rosrun tf static_transform_publisher 0.436690130728 2.83427135696 -0.0764351405955 0.690716383201 -0.656127148328 -0.148935346523 0.26500246369 map map1 100"&

sleep 1

xterm -title "TF map2" -e "rosrun tf static_transform_publisher -0.607251351828 2.41616047288 -0.225044228825 -0.648757197659 0.713845049369 -0.255346932508 0.0658580901316 map map2 100"&

sleep 1

xterm -title "TF bridge Node" -e "rosrun tf2_web_republisher tf2_web_republisher"
