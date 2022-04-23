#!/usr/bin/env python

import asyncio
import json
import websockets

async def hello():
    async with websockets.connect("ws://10.131.3.106:8080") as websocket:
        await websocket.send("1:U")
        await websocket.recv()

asyncio.run(hello())