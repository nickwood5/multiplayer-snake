#!/usr/bin/env python

import asyncio
import json
import websockets

async def hello():
    async with websockets.connect("ws://100.65.191.217:8765") as websocket:
        a = {"a": 20}
        await websocket.send("1:U")
        await websocket.recv()

asyncio.run(hello())