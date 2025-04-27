#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from f100_gripper_interfaces.srv import GetHandAngle  # 取得用サービス

class HandAngleGetterClient(Node):
    def __init__(self):
        super().__init__('hand_angle_getter_client')
        self.cli = self.create_client(GetHandAngle, 'get_hand_angle')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('サービス "get_hand_angle" が利用可能になるまで待っています...')
        self.req = GetHandAngle.Request()  # リクエストは空

    def send_request(self):
        self.future = self.cli.call_async(self.req)
        return self.future

def main(args=None):
    rclpy.init(args=args)
    client = HandAngleGetterClient()

    client.get_logger().info("ハンド角度取得リクエスト送信中...")

    future = client.send_request()

    rclpy.spin_until_future_complete(client, future)

    if future.result() is not None:
        result = future.result()
        if result.success:
            client.get_logger().info(f"現在のハンド角度: {result.angle} 度")
        else:
            client.get_logger().warn(f"取得失敗: {result.message}")
    else:
        client.get_logger().error("サービス呼び出しに失敗しました")

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
