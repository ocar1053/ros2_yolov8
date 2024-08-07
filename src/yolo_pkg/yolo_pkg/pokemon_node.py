import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO
import cv2
import os


class PokemonNode(Node):

    def __init__(self):
        super().__init__('pokemon_yolo_node')
        self.get_logger().info('Pokemon Node is running')
        self.bridge = CvBridge()
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.model_path = os.path.join(self.current_dir, '../','resource', 'best.pt')
        self.model = YOLO(self.model_path)
        self.subscription = self.create_subscription(
            Image,
            'camera_topic',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info('Received frame')
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        results = self.model.track(
            frame, persist=True)  # convert to track mode

        # visualizing results
        annotated_frame = results[0].plot()

        # show the frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # click 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            rclpy.shutdown()


def main():
    rclpy.init()
    node = PokemonNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
