import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, EnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    pkg = 'radar_drone_simulation'
    share = get_package_share_directory(pkg)
    # <prefix>/share/radar_drone_simulation -> <prefix>/lib/radar_drone_simulation
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(share)), 'lib', pkg)
    models_dir = os.path.join(share, 'models')
    worlds_dir = os.path.join(share, 'worlds')
    resources = models_dir + ':' + worlds_dir

    def prepend(var):
        return [EnvironmentVariable(var, default_value=''), ':']

    world = LaunchConfiguration('world')
    gz_cmd = LaunchConfiguration('gz_cmd')
    msgs = LaunchConfiguration('gz_msgs')   # 'ignition.msgs' (Fortress) or 'gz.msgs' (Garden+)
    model = LaunchConfiguration('model')    # model name in the SDF, used for namespaced topics

    def bridge(topic, ros_type, gz_type, direction='['):
        """Build one parameter_bridge argument.

        direction: '[' = Gazebo -> ROS, ']' = ROS -> Gazebo, '@' = bidirectional
        topic may be a plain string or a list of substitutions.
        """
        topic = topic if isinstance(topic, list) else [topic]
        return topic + ['@', ros_type, direction, msgs, '.', gz_type]

    bridge_args = [
        # ---- Clock ----
        bridge('/clock', 'rosgraph_msgs/msg/Clock', 'Clock'),

        # ---- Radar (existing) ----
        # Humble bridges Float_V to ros_gz_interfaces/msg/Float32Array (field: data).
        bridge('/radar/polar', 'geometry_msgs/msg/Point', 'Vector3d', '['),

        # ---- Control: ROS -> Gazebo ----
        bridge(['/', model, '/cmd_vel'], 'geometry_msgs/msg/Twist', 'Twist', ']'),
        bridge(['/', model, '/enable'], 'std_msgs/msg/Bool', 'Boolean', ']'),

        # ---- Sensors: Gazebo -> ROS ----
        bridge('/imu', 'sensor_msgs/msg/Imu', 'IMU'),
        bridge('/navsat', 'sensor_msgs/msg/NavSatFix', 'NavSat'),
        bridge('/air_pressure', 'sensor_msgs/msg/FluidPressure', 'FluidPressure'),
        bridge('/altimeter', 'sensor_msgs/msg/Altimeter', 'Altimeter'),
        bridge('/magnetometer', 'sensor_msgs/msg/MagneticField', 'Magnetometer'),
        bridge('/camera_front', 'sensor_msgs/msg/Image', 'Image'),
        bridge('/camera_front/camera_info', 'sensor_msgs/msg/CameraInfo', 'CameraInfo'),
        bridge('/front_laser', 'sensor_msgs/msg/LaserScan', 'LaserScan'),
        bridge('/front_laser/points', 'sensor_msgs/msg/PointCloud2', 'PointCloudPacked'),

        # ---- Odometry from the OdometryPublisher plugin ----
        bridge(['/drone/odom'], 'nav_msgs/msg/Odometry', 'Odometry'),

        # NOTE: the altimeter sensor (/altimeter) is not bridged because
        # ros_gz_bridge has no ROS message mapping for gz Altimeter that I know of.
        # Use /air_pressure or the odometry z position for altitude on the ROS side.
    ]

    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value=os.path.join(worlds_dir, 'radar_world.sdf')),
        # Fortress: "ign gazebo"   |   Garden and newer: "gz sim"
        DeclareLaunchArgument('gz_cmd', default_value='ign gazebo'),
        # Fortress: "ignition.msgs"   |   Garden and newer: "gz.msgs"
        DeclareLaunchArgument('gz_msgs', default_value='ignition.msgs'),
        DeclareLaunchArgument('model', default_value='M100'),

        # Fortress variable names
        SetEnvironmentVariable('IGN_GAZEBO_SYSTEM_PLUGIN_PATH', prepend('IGN_GAZEBO_SYSTEM_PLUGIN_PATH') + [plugin_dir]),
        SetEnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', prepend('IGN_GAZEBO_RESOURCE_PATH') + [resources]),
        # Garden/Harmonic/Ionic variable names (harmless on Fortress)
        SetEnvironmentVariable('GZ_SIM_SYSTEM_PLUGIN_PATH', prepend('GZ_SIM_SYSTEM_PLUGIN_PATH') + [plugin_dir]),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', prepend('GZ_SIM_RESOURCE_PATH') + [resources]),

        ExecuteProcess(
            cmd=[gz_cmd, '-r', world, '-v 4'],
            shell=True,
            output='screen'),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=bridge_args,
            # Expose the drone command as a plain /cmd_vel on the ROS side
            remappings=[(['/', model, '/cmd_vel'], '/cmd_vel')],
            output='screen'),
    ])