# radar_drone_simulation

This package provides a ROS 2 simulation for localizing a drone using FMCW antenna array radar, GNSS, and additional sensor integration. It is designed for research and testing involving drone localization, state estimation, and control.

## Prerequisites

Before running the simulation, make sure you have:

- ROS 2 installed
- `colcon` installed
- `git` installed
- A ROS 2 workspace created

## Setup

Replace `{ros2_workspace_dir}` with the path to your ROS 2 workspace.

```bash
cd {ros2_workspace_dir}/src
git clone https://github.com/AbhoySB-03/drone_localization.git radar_drone_simulation
cd {ros2_workspace_dir}
colcon build --packages-select radar_drone_simulation
source install/setup.bash
