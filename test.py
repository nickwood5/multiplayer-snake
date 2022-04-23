#!/usr/bin/env python

import asyncio
import json
import websockets

async def hello():
    async with websockets.connect("ws://multiplayer-snake2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/:8080") as websocket:
        await websocket.send("1:U")
        await websocket.recv()

asyncio.run(hello())