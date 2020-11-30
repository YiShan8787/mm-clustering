import matplotlib.pyplot as plt
import rospy
import rosbag
import numpy as np
import argparse

import glob
import os
import numpy as np

from micro_doppler_pkg.msg import MicroDoppler_m

parent_dir = '/home/wt/RadHARex/Data/Train/swing/bagfile'

def parse_RF_files(file_ext='*.bag'):

    files=sorted(glob.glob(os.path.join(parent_dir, file_ext)))
    #print(files)
    for fn in files:
        print(fn)
        write_data(fn)


def write_data(file_path):
    bag = rosbag.Bag(file_path)
    mds_array   = []



parse_RF_files()