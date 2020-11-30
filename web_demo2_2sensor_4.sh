#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd data/bag/camera_tf_4; rosbag play -l 2sensor_2tag_raw2.bag;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2_2.py"&

sleep 1

xterm -title "bridge Node" -e "roslaunch rosbridge_server rosbridge_websocket.launch"&

sleep 1

xterm -title "TF map1" -e "rosrun tf static_transform_publisher -0.339915793877 2.69443122413 -0.157428869418 0.962158884136 0.0113586052095 0.267631443268 0.0499467150204 map map1 100"&

sleep 1

xterm -title "TF map2" -e "rosrun tf static_transform_publisher 0.493533543111 2.80038615474 0.110089844213 0.985241695336 0.0463615833168 -0.155392305582 0.0547963204039 map map2 100"&

sleep 1

xterm -title "TF bridge Node" -e "rosrun tf2_web_republisher tf2_web_republisher"
