import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_srvs.srv import Trigger

class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.subscriber = self.create_subscription(Float32, '/battery_level', self.listener_callback, 10)
        self.subscriber  # prevent unused variable warning
        self.client = self.create_client(Trigger, '/recharge')
        self.recharging = False
        
             
            
    def listener_callback(self, msg):
        self.get_logger().info('Battery Level: "%s"' % msg.data)
        if msg.data < 20:
            self.get_logger().warn('Low Battery Level')
        else:
            pass
        
        if msg.data < 5 and not self.recharging:
            if self.client.service_is_ready():
                self.recharging = True
                req = Trigger.Request()
                future = self.client.call_async(req)
                future.add_done_callback(self.recharge_response_callback)
                
    def recharge_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(response.message)
        except Exception as e:
            self.get_logger().error(f'Servis çağrısı başarısız: {e}')            
        finally:
            self.recharging = False
    
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