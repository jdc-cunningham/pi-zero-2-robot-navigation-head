# https://websockets.readthedocs.io/en/stable/
#!/usr/bin/env python

import sys

sys.path.insert(1, '/home/pi/chisel-bot-2/code/raspberry-pi/methods') # stupidly long paths

import asyncio
import websockets
import time
from servo import tmp_look_around

async def move_forward():
  async with websockets.connect("ws://192.168.1.195:80") as websocket:
    await websocket.send("_mfs_10_mfe_")
    # await websocket.recv()

# asyncio.run(connect())

async def turn_left():
  async with websockets.connect("ws://192.168.1.195:80") as websocket:
    await websocket.send("_mls_10_mle_")

async def drive_away():
  async with websockets.connect("ws://192.168.1.195:80") as websocket:
    await websocket.send("_mfs_20_mfe_")

async def run_all():
  async with websockets.connect("ws://192.168.1.195:80") as websocket:
    await websocket.send("_mfs_20_mfe_")
    time.sleep(5)
    await websocket.send("_mls_90_mle_")
    time.sleep(5)
    tmp_look_around()
    # time.sleep(5)
    await websocket.send("_mfs_20_mfe_") # can't do 25 for some reason or 30

# time.sleep(16)
asyncio.run(run_all())
