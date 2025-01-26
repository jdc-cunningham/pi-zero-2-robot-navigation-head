from threading import Thread
from websockets.sync.client import connect

# to ESP-01
class SocketClient():
  def __init__(self):
    self.socket = None

    self.start()

  def receive(self, msg):
    print(msg)

  def send(self, msg):
    if (not self.socket):
      print("no connection")
    else:
      self.socket.send(msg)

  def run(self):
    with connect("ws://192.168.1.159:80") as websocket:
      self.socket = websocket

      while True:
        msg = websocket.recv()
        self.receive(msg)

  def start(self):
    Thread(target=self.run, args=()).start()
  