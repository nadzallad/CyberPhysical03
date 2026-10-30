import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleStop(Node):
    def __init__(self):
        super().__init__('obstacle_stop')
        self.declare_parameter('stop_distance', 0.35)
        self.declare_parameter('linear_speed', 0.15)
        self.declare_parameter('angular_speed', 0.6)
        self.declare_parameter('front_fov_deg', 60.0)
        self.declare_parameter('scan_timeout', 0.5)

        self.min_front = float('inf')
        self.last_scan = None
        self.sub = self.create_subscription(
            LaserScan, 'scan', self.on_scan, qos_profile_sensor_data)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.control)

    def on_scan(self, msg):
        half = math.radians(self.get_parameter('front_fov_deg').value) / 2.0
        best = float('inf')
        for i, r in enumerate(msg.ranges):
            if not (msg.range_min < r < msg.range_max):
                continue                      # inf, nan, di luar jangkauan
            a = msg.angle_min + i * msg.angle_increment
            a = math.atan2(math.sin(a), math.cos(a))   # normalisasi ke [-pi, pi]
            if abs(a) <= half:
                best = min(best, r)
        self.min_front = best
        self.last_scan = self.get_clock().now()

    def control(self):
        cmd = Twist()
        timeout = self.get_parameter('scan_timeout').value
        fresh = (self.last_scan is not None and
                 (self.get_clock().now() - self.last_scan).nanoseconds * 1e-9 < timeout)
        if fresh:
            if self.min_front > self.get_parameter('stop_distance').value:
                cmd.linear.x = self.get_parameter('linear_speed').value
            else:
                cmd.angular.z = self.get_parameter('angular_speed').value
        self.pub.publish(cmd)       # tidak fresh -> Twist nol (berhenti)


def main():
    # Ctrl+C ditangani sendiri agar context masih aktif saat mengirim Twist nol
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    node = ObstacleStop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())       # robot berhenti saat node dimatikan
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
