from threading import Thread
from websockets.sync.server import serve

# for Web Interface
class SocketServer():
  def __init__(self, main):
    self.socket = None
    self.main = main # circular dep fix

    self.start()

  def parse_msg(self, msg):
    if (msg == "start"):
      self.main.navigation.start()

  def receive(self, websocket):
    for msg in websocket:
      self.socket = websocket

      self.parse_msg(msg)

  def send(self, msg: str):
    if (not self.socket):
      print("socket not ready")
    else:
      self.socket.send(msg)

  def run(self):
    with serve(self.receive, "192.168.1.155", 5678) as server:
      server.serve_forever()

  def start(self):
    Thread(target=self.run, args=()).start()
