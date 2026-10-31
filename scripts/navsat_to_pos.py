#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float32MultiArray


class NavSatToGazeboNode(Node):
    def __init__(self):
        super().__init__('navsat_to_gazebo_node')

        # -------------------------------------------------------------
        # ROS 2 Parameters (Match these with your SDF <spherical_coordinates>)
        # -------------------------------------------------------------
        self.declare_parameter('datum_latitude_deg', 28.6139)
        self.declare_parameter('datum_longitude_deg', 77.2090)
        self.declare_parameter('datum_elevation_m', 216)
        self.declare_parameter('heading_deg', 0.0)
        self.declare_parameter('world_frame_id', 'world')

        # Fetch parameter values
        lat0_deg = self.get_parameter('datum_latitude_deg').value
        lon0_deg = self.get_parameter('datum_longitude_deg').value
        self.h0 = self.get_parameter('datum_elevation_m').value
        heading_deg = self.get_parameter('heading_deg').value
        self.world_frame_id = self.get_parameter('world_frame_id').value

        # Radians conversion
        self.lat0 = math.radians(lat0_deg)
        self.lon0 = math.radians(lon0_deg)
        self.theta = math.radians(heading_deg)

        # -------------------------------------------------------------
        # Precompute WGS84 Curvature Radii at Datum
        # -------------------------------------------------------------
        a = 6378137.0                      # Equatorial radius (semi-major axis)
        f = 1.0 / 298.257223563            # Flattening
        e2 = 2 * f - f**2                  # First eccentricity squared

        sin_lat = math.sin(self.lat0)
        denom = math.sqrt(1.0 - e2 * sin_lat**2)

        self.N0 = a / denom                # Prime vertical radius of curvature
        self.M0 = a * (1.0 - e2) / (denom**3) # Meridian radius of curvature

        # -------------------------------------------------------------
        # Subscriber and Publisher
        # -------------------------------------------------------------
        self.sub = self.create_subscription(
            NavSatFix,
            '/navsat',
            self.navsat_callback,
            10
        )

        self.pub = self.create_publisher(
            Float32MultiArray,
            '/position',
            10
        )

        self.get_logger().info(
            f'NavSat to Gazebo node initialized. Datum: '
            f'({lat0_deg}°, {lon0_deg}°, {self.h0}m), Heading: {heading_deg}°'
        )

    def navsat_callback(self, msg: NavSatFix):
        # Ignore invalid GPS fixes if status is reported as no fix
        if msg.status.status < 0:
            self.get_logger().warn('Received invalid GPS fix. Ignoring measurement.', throttle_duration_sec=2.0)
            return

        # Convert incoming coordinates to radians
        lat = math.radians(msg.latitude)
        lon = math.radians(msg.longitude)
        alt = msg.altitude

        # DelTas relative to world origin datum
        d_lat = lat - self.lat0
        d_lon = lon - self.lon0
        d_alt = alt - self.h0

        # Displacements in local tangent East-North-Up (ENU)
        east = (self.N0 + self.h0) * math.cos(self.lat0) * d_lon
        north = (self.M0 + self.h0) * d_lat
        up = d_alt

        # Rotate ENU displacement by Gazebo heading offset
        x_w = east * math.cos(self.theta) - north * math.sin(self.theta)
        y_w = east * math.sin(self.theta) + north * math.cos(self.theta)
        z_w = up

        # Prepare and publish PointStamped
        point_msg = Float32MultiArray()
        point_msg.data = [x_w, y_w, z_w]

        self.pub.publish(point_msg)


def main(args=None):
    rclpy.init(args=args)
    node = NavSatToGazeboNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()