from threading import Thread
from websockets.sync.server import serve

# for Web Interface
class SocketServer():
  def __init__(self):
    self.socket = None

    self.start()

  def receive(self, websocket):
    for msg in websocket:
      self.socket = websocket

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
