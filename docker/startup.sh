#!/bin/bash

# Change repo names accordingly

# run . $HOST_HOME_DIR/GTLIDAR/ros2_BegForked_ws/src/elevation_mapping_cupy/docker/startup.sh
catkin_ws="$HOST_HOME_DIR/GTLIDAR/ros2_BegForked_ws"

echo "Running initial setup..."
echo "Host's home directory: $HOST_HOME_DIR"

# bashrc changes
source /opt/ros/humble/setup.bash

# Digit in Mujoco
cd $catkin_ws/src/digit_mujoco/src/digit_mujoco/
rm -rf build/temp.linux-x86_64-3.8
pip install -e .

# # Global Planner (if it exists)
# if [ -d "$catkin_ws/src/global_planner_RRT" ]; then
#     cd $catkin_ws/src/global_planner_RRT 
#     pip install -r requirements.txt
#     pip install -e .
# fi

# ROS2 build
cd $catkin_ws
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
colcon build
source $catkin_ws/install/local_setup.bash
source $catkin_ws/install/setup.bash

echo "source $catkin_ws/install/local_setup.bash" >> ~/.bashrc
echo "source $catkin_ws/install/setup.bash" >> ~/.bashrc
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'export RMW_IMPLEMENTATION=rmw_fastrtps_cpp' >> ~/.bashrc
source ~/.bashrc

# # ROS2 Bridge
# source /opt/ros/foxy/setup.bash
# rosbridge_ws="$HOST_HOME_DIR/GTLIDAR/ros2_BegForked_ws"
# mkdir -p $rosbridge_ws/src
# cd $rosbridge_ws/src
# git clone https://github.com/ros2/ros1_bridge.git -b foxy
# cd ..

# source /opt/ros/noetic/setup.bash
# source /opt/ros/foxy/setup.bash
# rosdep install --from-paths src --ignore-src -r -y
# source install/setup.bash

# ros2 run ros1_bridge dynamic_bridge

# echo "source $catkin_ws/devel/local_setup.bash" >> ~/.bashrc
# echo "source $catkin_ws/devel/setup.bash" >> ~/.bashrc
# echo 'source /opt/ros/noetic/setup.bash' >> ~/.bashrc
# source ~/.bashrc