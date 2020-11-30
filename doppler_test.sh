#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record1 Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -l front.bag;"&

sleep 1

xterm -title "pcl Node" -e "cd src/node1_radarinterface/src; python mmfall2.py"&

sleep 1

xterm -title "Doppler Node" -e "cd src/micro_doppler_pkg/scripts; python micro_doppler_bag.py"&

sleep 5

xterm -title "Plot Doppler" -e "cd src/micro_doppler_pkg/scripts; python plot_mds_topic.py"