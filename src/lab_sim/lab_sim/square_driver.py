import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareDriver(Node):
    def __init__(self):
        super().__init__('square_driver')
        self.declare_parameter('side', 1.0)
        self.declare_parameter('linear_speed', 0.1)
        self.declare_parameter('angular_speed', 0.5)
        side = self.get_parameter('side').value
        v = self.get_parameter('linear_speed').value
        w = self.get_parameter('angular_speed').value

        # (v, w, durasi detik): 4 sisi lurus + 4 belokan 90 derajat
        self.plan = []
        for _ in range(4):
            self.plan.append((v, 0.0, side / v))
            self.plan.append((0.0, w, (math.pi / 2.0) / w))

        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.idx = 0
        self.t0 = None
        self.done = False
        self.timer = self.create_timer(0.02, self.step)

    def step(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        if now == 0.0:          # /clock belum diterima
            return
        if self.t0 is None:
            self.t0 = now
        if now - self.t0 >= self.plan[self.idx][2]:
            self.idx += 1
            self.t0 = now
            if self.idx >= len(self.plan):
                self.pub.publish(Twist())
                self.get_logger().info('lintasan persegi selesai')
                self.timer.cancel()
                self.done = True
                return
        v, w, _ = self.plan[self.idx]
        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = w
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = SquareDriver()
    try:
        while rclpy.ok() and not node.done:     # keluar otomatis setelah selesai
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
