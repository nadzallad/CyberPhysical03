
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')

        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('depth', 10)

        reliability = self.get_parameter('reliability').value
        depth = self.get_parameter('depth').value

        rel = (
            ReliabilityPolicy.RELIABLE
            if reliability == 'reliable'
            else ReliabilityPolicy.BEST_EFFORT
        )

        qos = QoSProfile(
            depth=depth,
            reliability=rel,
            history=HistoryPolicy.KEEP_LAST
        )

        self.count = 0
        self.sub = self.create_subscription(
            Float32, 'sensor_data', self.on_data, qos
        )

    def on_data(self, msg):
        self.count += 1


def main():
    rclpy.init()
    node = SensorSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        print(f'Total pesan diterima: {node.count}')
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
