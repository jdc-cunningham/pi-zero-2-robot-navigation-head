# https://websockets.readthedocs.io/en/stable/
#!/usr/bin/env python

import asyncio
import websockets

socket_conn = None

async def connect():
    async with websockets.connect("ws://192.168.1.195:80") as websocket:
        socket_conn = websocket
        print("connected")
        # await websocket.send("_mfs_5_mfe_")
        # await websocket.recv()

asyncio.run(connect())
