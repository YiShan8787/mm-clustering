# mm-clustering
for ti-mmwave human behavior clustering

# Quick Start
Starting with a working ROS installation (Kinetic is supported):

    export ROS_DISTRO=kinetic               # Set this to your distro, e.g. kinetic or melodic
    source /opt/ros/$ROS_DISTRO/setup.bash  # Source your ROS distro 
    mkdir -p ~/mmcluster_ws/src                # Make a new workspace 
    cd ~/mmcluster_ws/src                      # Navigate to the source space
    git clone https://github.com/YiShan8787/mm-clustering.git      # Clone this rep
    cd ~/mmcluster_ws                          # Navigate to the workspace
    rosdep install --from-paths src --ignore-src -r -y  # Install any missing packages
    catkin build    # Build all packages in the workspace (catkin_make_isolated will work also)
