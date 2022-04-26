import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Helloworld!")
        await websocket.recv()

asyncio.run(hello())