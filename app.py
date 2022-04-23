print("Run app")

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "https://multiplayer-snake-git-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())