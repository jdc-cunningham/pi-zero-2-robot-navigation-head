import asyncio
import websockets

class Websocket():
  def __init__(self):
    self.socket = False

  async def check_command(self, msg, socket):
    await socket.send("str")

  async def receive(self, websocket):
    while True:
      msg = await websocket.recv()
      await self.check_command(msg, websocket)
      await asyncio.sleep(0.1)

  async def main(self):
    async with websockets.serve(self.receive, "192.168.1.155", 5678):
      await asyncio.Future()

  def start(self):
    asyncio.run(self.main())
