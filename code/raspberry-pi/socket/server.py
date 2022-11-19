# https://websockets.readthedocs.io/en/stable/intro/quickstart.html
#!/usr/bin/env python

import sys
import time
import asyncio
import datetime
import random
import websockets
import json

sys.path.append('/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi')

from sensors.Sensors import *
from methods.servo import *

sensors = Sensors()

async def check_command(msg, socket):
  # no switch case? megamind, I don't have 3.10

  if (msg == "left"):
    remote_left()
  elif (msg == "right"):
    remote_right()
  elif (msg == "up"):
    remote_up()
  elif (msg == "down"):
    remote_down()
  elif (msg == "center"):
    remote_center()
  elif (msg == "tof"):
    await socket.send(str(sensors.tof.get_distance()))
  elif (msg == "lidar"):
    await socket.send(str(sensors.lidar.get_distance()))
  else:
    # do nothing
    print(msg)

async def show_time(websocket):
  while True:
    msg = await websocket.recv()
    await check_command(msg, websocket)
    await asyncio.sleep(0.1)

async def main():
  async with websockets.serve(show_time, "192.168.1.156", 5678):
    await asyncio.Future()  # run forever

if __name__ == "__main__":
  asyncio.run(main())
