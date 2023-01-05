# https://websockets.readthedocs.io/en/stable/intro/quickstart.html
#!/usr/bin/env python

import sys
import time
import asyncio
import datetime
import random
import websockets
import json

sys.path.append('/home/pi/chisel-bot-2/code/raspberry-pi')

# from methods.start_imu import *
from sensors.Sensors import *

sensors = Sensors()

async def show_time(websocket):
  while True:
    mpu_sample = sensors.imu.mpu_sample
    print(mpu_sample)
    await websocket.send(mpu_sample) # should already be a json
    # await websocket.send(mpu_sample)
    await asyncio.sleep(sensors.imu.sample_rate) # 0.005 normal sampling rate

async def main():
  async with websockets.serve(show_time, "192.168.1.155", 5678):
    await asyncio.Future()  # run forever

if __name__ == "__main__":
  asyncio.run(main())
