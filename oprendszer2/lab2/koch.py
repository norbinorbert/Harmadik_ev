# colcon build --packages-select py_pubsub
# source install/setup.bash
# ros2 run py_pubsub koch

import rclpy
from rclpy.node import Node

from turtlesim.srv import TeleportAbsolute
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
import mathS

def koch_curve(order, length):
    if order == 0:
        return [(length, 0)]
    else:
        segment = length / 3.0
        return (
            koch_curve(order - 1, segment) +
            [(0, 60)] + koch_curve(order - 1, segment) +
            [(0, -120)] + koch_curve(order - 1, segment) +
            [(0, 60)] + koch_curve(order - 1, segment)
        )
        
class KochTurtle(Node):

    def __init__(self):
        super().__init__('koch_turtle')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.clear_client = self.create_client(Empty, '/clear')

        self.steps = koch_curve(2, 9.0)
        self.index = 0
        
        self.teleport_turtle()

    def teleport_turtle(self):
        req = TeleportAbsolute.Request()
        req.x = 1.0
        req.y = 5.5
        req.theta = 0.0

        future = self.teleport_client.call_async(req)
        future.add_done_callback(self.clear_canvas)
        
    def clear_canvas(self, future):
        req = Empty.Request()
        future = self.clear_client.call_async(req)
        future.add_done_callback(self.start_timer)
        
    def start_timer(self, future):
        self.timer = self.create_timer(1.0, self.move_turtle)

    def move_turtle(self):
        if self.index < len(self.steps):
            move_cmd = Twist()
            length, angle = self.steps[self.index]
            if length > 0:
                move_cmd.linear.x = length
            else:
                move_cmd.angular.z = math.radians(angle)
            
            self.publisher_.publish(move_cmd)
            self.index += 1
        else:
            self.timer.cancel()
            exit(0)


def main(args=None):
    rclpy.init(args=args)
    node = KochTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
