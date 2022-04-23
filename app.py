print("Run app")
import time

import websockets

import asyncio
print("s")

async def echo(websocket, client):
    async for message in websocket:
        print(client)
        print(message)
        print(time.time())
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())

while (1):
    time.sleep(10)
    print("Run ap 1p")