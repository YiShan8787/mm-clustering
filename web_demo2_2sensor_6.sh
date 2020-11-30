#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd ;cd RadHARex/Data/new_data/boxing; rosbag play -l front.bag;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2_2.py"&

sleep 1

xterm -title "bridge Node" -e "roslaunch rosbridge_server rosbridge_websocket.launch"&

sleep 1

xterm -title "TF map1" -e "rosrun tf static_transform_publisher 0.358071247976 2.64577158994 -0.0746722596597 0.989116656774 -0.00591192322853 -0.130184246541 -0.0683033703979 map map1 100"&

sleep 1

xterm -title "TF map2" -e "rosrun tf static_transform_publisher -0.91750478718 2.67003172978 -0.116629253056 0.999906158348 0.0073161750411 0.0103786057357 0.0051412666373 map map2 100"&

sleep 1

xterm -title "TF bridge Node" -e "rosrun tf2_web_republisher tf2_web_republisher"
