print("Run app")
import time

import websockets

import asyncio
print("s")

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "multiplayer-snake-git-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())

while (1):
    time.sleep(10)
    print("Run ap 1p")