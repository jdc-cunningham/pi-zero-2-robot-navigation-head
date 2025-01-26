from threading import Thread
from websockets.sync.client import connect

# to ESP-01
# ESP-01 does not send anything back, it could
class SocketClient():
  def send(self, msg):
    with connect("ws://192.168.1.159:80") as websocket:
      socket = websocket

      if (not socket):
        print("no connection")
      else:
        socket.send(msg)
