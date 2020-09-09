#!/bin/sh

xterm -title "Radar Module" -e "roslaunch node1_radarinterface node1_radarinterface.launch"&

sleep 1

xterm -title "LSTM Node" -e "cd src/node1_radarinterface/src; python3 voxel_realtime4.py"&

sleep 5

xterm -title "Result Node" -e "rostopic echo /predict_result"

