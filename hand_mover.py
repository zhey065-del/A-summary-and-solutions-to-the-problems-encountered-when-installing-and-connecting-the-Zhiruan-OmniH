import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class HandMover(Node):
    def __init__(self):
        super().__init__('hand_mover_node')
        self.br = TransformBroadcaster(self)
        # 设置定时器，每 0.05 秒更新一次位置 (20Hz)
        self.timer = self.create_timer(0.05, self.broadcast_timer_callback)
        self.angle = 0.0

    def broadcast_timer_callback(self):
        t = TransformStamped()
        
        # 1. 设置时间戳和坐标系名称
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'      # 父坐标系：世界
        t.child_frame_id = 'base_link'   # 子坐标系：灵巧手的根部

        # 2. 计算圆周运动轨迹
        radius = 0.5  # 半径 0.5 米
        self.angle += 0.05
        t.transform.translation.x = radius * math.cos(self.angle)
        t.transform.translation.y = radius * math.sin(self.angle)
        t.transform.translation.z = 0.2 # 离地 0.2 米

        # 3. 设置姿态（这里保持不旋转，设为单位四元数）
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        # 4. 发送坐标变换
        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = HandMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == '__main__':
    main()
