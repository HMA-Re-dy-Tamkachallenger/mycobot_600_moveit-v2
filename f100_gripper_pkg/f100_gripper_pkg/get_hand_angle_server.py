#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from f100_gripper_interfaces.srv import GetHandAngle  # 取得用カスタムサービス
from f100_gripper_pkg.elegripper import Gripper

class GripperAngleGetter(Node):
    def __init__(self):
        super().__init__('gripper_angle_getter')
        self.srv = self.create_service(GetHandAngle, 'get_hand_angle', self.handle_get_hand_angle)
        self.get_logger().info('グリッパー角度取得サービスサーバーが起動しました。')

        self.g = Gripper("/dev/ttyACM0", baudrate=115200, id=14)
        print("The actual ID of the gripper is:", self.g.get_gripper_Id())

    def handle_get_hand_angle(self, request, response):
        try:
            # 角度取得コマンドの実装：g.get_gripper_value() を仮定（なければ置き換え）
            angle = self.g.get_gripper_value()  # ここが角度を取得する関数
            response.angle = angle
            response.success = True
            response.message = f'現在のハンド角度は {angle} 度です。'
            self.get_logger().info(response.message)
        except Exception as e:
            response.angle = -1
            response.success = False
            response.message = f'角度取得に失敗しました: {e}'
            self.get_logger().error(response.message)
        return response

def main(args=None):
    rclpy.init(args=args)
    server = GripperAngleGetter()
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        server.get_logger().info('グリッパー角度取得サービスサーバーを終了します...')
    finally:
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
