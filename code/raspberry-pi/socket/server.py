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

# from methods.start_imu import *
from sensors.Sensors import *

sensors = Sensors()

print(sensors.dump())

async def show_time(websocket):
  while True:
    mpu_sample = sensors.Imu.mpu_sample
    # print(mpu_sample)
    await websocket.send('yo')
    # await websocket.send(mpu_sample)
    await asyncio.sleep(0.1)

async def main():
  async with websockets.serve(show_time, "192.168.1.156", 5678):
    await asyncio.Future()  # run forever

if __name__ == "__main__":
  asyncio.run(main())
