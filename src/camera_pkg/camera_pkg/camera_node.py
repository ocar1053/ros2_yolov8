import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class cameraNode(Node):

    def __init__(self):
        super().__init__('camera_node')
        self.get_logger().info('Camera Node is running')
        self.publisher_ = self.create_publisher(Image, 'camera_topic', 10)
        self.cap = cv2.VideoCapture('/home/ocar1053/ros2_ws/src/camera_pkg/resource/20240717_175123.mp4')
        self.bridge = CvBridge()
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
      

    def timer_callback(self):

        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().info('End of video, stopping node.')
            self.cap.release()
            rclpy.shutdown()
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing frame captured')

def main():
    rclpy.init()
    node = cameraNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main() 