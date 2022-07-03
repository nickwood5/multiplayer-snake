import asyncio
import websockets, json, random
import requests, time, threading

local_host = False

if local_host:
    api_url = "http://localhost:8769/get/"
    app_url = "ws://127.0.0.1:8770/"
else:
    api_url = "https://nickwood5.pythonanywhere.com/get/"
    app_url = "wss://websockets-echo-nick.herokuapp.com/"


async def new(websocket, current_direction):
    while (True):
        new_dir = choose_direction()
        if current_direction != new_dir:
            await websocket.send(json.dumps({"type": "move", "direction": new_dir}))
            current_direction = new_dir

        await asyncio.sleep(1)

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

#asyncio.get_event_loop().run_until_complete(test(id))


abormal_termination = False




def create():
    time.sleep(0.01)
    _thread2 = threading.Thread(target=new2, args=())
    _thread2.start()
    _thread2.join()

    _thread2 = threading.Thread(target=new2, args=())
    _thread2.start()
    _thread2.join()




import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)

    new2()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(1):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)