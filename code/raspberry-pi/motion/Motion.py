import pigpio
import time
import asyncio
import websockets

# there is a boot script that centers the servos

class Motion:
  def __init__(self):
    self.pi = pigpio.pi()
    self.pan_servo = 12
    self.tilt_servo = 13

  class PanTilt():
    def __init__(self):
      self.pan_servo
      self.tilt_servo

  # this is a websocket control against the WiFi buggy
  class Wheels():
    def __init__(self):
      self.socket_addr = "ws://192.168.1.195:80"
      self.left
      self.right
      self.move_forward
      self.move_left
      self.move_right
      self.move_backward

    async def send_command(self, msg):
      async with websockets.connect(self.socket_addr) as websocket:
        await websocket.send(msg)

    # hmm 
    # asyncio.run(send_command())
