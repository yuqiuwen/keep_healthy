from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端向后端发送websocket连接请求时自动触发
        self.accept()

    def websocket_receive(self, message):
        # 浏览器向服务端发送消息自动触发
        print("收到消息")
        self.send("收到消息")

    def websocket_disconnect(self, message):
        # 服务端和客户端断开连接时自动触发
        print("断开连接")
        raise StopConsumer()