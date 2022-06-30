import asyncio
from numpy import choose
import websockets, json, random
import requests, time, threading

local_host = True

if local_host:
    api_url = "http://localhost:8769/get/"
    app_url = "ws://127.0.0.1:8770/"
else:
    api_url = "http://api-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/get/"
    app_url = "ws://app-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/"

async def new(websocket, current_direction):
    while (True):
        new_dir = choose_direction()
        if current_direction != new_dir:
            await websocket.send(json.dumps({"type": "move", "direction": new_dir}))
            current_direction = new_dir

        await asyncio.sleep(3)

async def test(id):
    current_direction = "u"
    async with websockets.connect(app_url + str(id)) as websocket:
        await websocket.send(json.dumps({"type": "connect"}))
        await asyncio.sleep(1)
        await websocket.send(json.dumps({"type": "spawn", "colour": "#00FF00"}))
        await asyncio.sleep(1)
        print("Spawn")
        await new(websocket, current_direction)
            






async def speed_up(period, websocket):
    websocket.send(json.dumps({"type": "increase_speed"}))
    time.sleep(period)
    websocket.send(json.dumps({"type": "decrease_speed"}))

def choose_direction():
    dir = random.randint(1, 4)
    if dir == 1:
        direction = "u"
    elif dir == 2:
        direction = "d"
    elif dir == 3:
        direction = "l"
    elif dir == 4:
        direction = "r"
    
    return direction




for r in range (0, 1000):
    choose_direction()


def new2():
    response = requests.get(api_url)
    result = response.json()
    id = result["id"]
    print(id)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(test(id))
    loop.close()

#asyncio.get_event_loop().run_until_complete(test(id))

for a in range (0, 200):
    time.sleep(0.01)
    _thread2 = threading.Thread(target=new2, args=())
    _thread2.start()