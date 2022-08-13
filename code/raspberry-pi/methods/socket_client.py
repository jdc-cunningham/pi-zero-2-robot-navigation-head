# https://websockets.readthedocs.io/en/stable/
#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://192.168.1.195:80") as websocket:
        await websocket.send("_mfs_5_mfe_")
        await websocket.recv()

asyncio.run(hello())