**ROS 2 Package Name:** radar_drone_simulation
## Setup
cd {ros2_workspace_dir}/src
git clone https://github.com/AbhoySB-03/drone_localization.git radar_drone_simulation
cd ..
colcon build --packages-select radar_drone_simulation
source install/setup.bash

## Launch the simulation
source {ros2_workspace_dir}/install/setup.bash
ros2 launch radar_drone_simulation radar_sim.launch.py
