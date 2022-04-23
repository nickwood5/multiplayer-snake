#!/usr/bin/env python

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "100.65.191.217", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())