#!/bin/sh

xterm -title "Ros Node" -e "roscore"&

sleep 2

xterm -title "Record Node" -e "cd;cd RadHARex/Data/Train/swing/bagfile; rosbag play -d 1 front.bag;"&



xterm -title "Doppler Node" -e "cd src/micro_doppler_pkg/scripts; python micro_doppler_bag.py"&

sleep 1

xterm -title "New Doppler File Node" -e "cd;cd RadHARex/Data/new_data/swing/bagfile; rosbag record --duration=20 -O new_front.bag -a"

sleep 20

xterm -title "Bag to Txt" -e "cd;cd RadHARex/Data/new_data/swing; rostopic echo -b new_front.bag /node1_radarinterface/radar_scan > new_front.txt"