#!/bin/sh

xterm -title "Radar0 Module" -e "roslaunch node1_radarinterface node1_radarinterface.launch"&

sleep 2

xterm -title "Radar1 Module" -e "roslaunch node1_radarinterface node1_radarinterface_2.launch"&

sleep 1

xterm -title "cam Module" -e "roslaunch realsense2_camera rs_multiple_devices.launch"&

sleep 1

xterm -title "doppler 0" -e "cd src/micro_doppler_pkg/scripts; python micro_doppler_0.py"&

sleep 1

xterm -title "doppler 0" -e "cd src/micro_doppler_pkg/scripts; python micro_doppler_1.py"&

sleep 3

xterm -title "Record Node" -e "cd; cd RadHARex/Data/new_data/left_right_stand; rosbag record -O front.bag --duration=20 /camera1/color/image_raw /camera2/color/image_raw /node1_radarinterface/radar_scan_0 /node1_radarinterface/radar_scan_1 /ti_mmwave/micro_doppler_0 /ti_mmwave/micro_doppler_1"&

