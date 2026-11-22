import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_srvs.srv import Trigger

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.publisher_ = self.create_publisher(Float32, '/battery_level',10)
        self.srv = self.create_service(Trigger, '/recharge', self.recharge_callback)
        self.battery_level = 100.0
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = Float32()
        msg.data = self.battery_level
        self.publisher_.publish(msg)
        self.get_logger().info(f'Pil Seviyesi: %{self.battery_level:.1f}')
        if self.battery_level > 0.0:
            self.battery_level = max(0.0, self.battery_level - 1.0)
        
    def recharge_callback(self, request, response):
        self.battery_level = 100.0
        response.success = True
        response.message = 'Pil şarj edildi'
        self.get_logger().info('Şarj servisi çağrıldı: Pil %100.0 yapıldı.')
        return response    
        
def main(args=None):
    rclpy.init(args=args)
    battery_level_publisher = BatteryNode()
    try:
        rclpy.spin(battery_level_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        battery_level_publisher.destroy_node()
        rclpy.shutdown()
    
    
if __name__ == '__main__':
    main()
        