import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32

class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.subscriber = self.create_subscription(Float32, '/battery_level', self.listener_callback, 10)
        self.subscriber  # prevent unused variable warning
    
    def listener_callback(self, msg):
        self.get_logger().info('Battery Level: "%s"' % msg.data)
        if msg.data < 20:
            self.get_logger().warn('Low Battery Level')
        else:
            pass
    
def main(args = None):
    rclpy.init(args=args)
    monitor_node_subscriber = MonitorNode()
    try:
        rclpy.spin(monitor_node_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        monitor_node_subscriber.destroy_node()
        rclpy.shutdown()
    
    
if __name__ == '__main__':
    main()