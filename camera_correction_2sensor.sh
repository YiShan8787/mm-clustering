#!/bin/sh

xterm -title "Radar 0 Module" -e "roslaunch node1_radarinterface camera_correction_0.launch"&

sleep 1

xterm -title "Radar 0 Module" -e "roslaunch node1_radarinterface camera_correction_1.launch"