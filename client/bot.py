import asyncio
from turtle import TurtleScreen
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


async def receive_websocket_message(websocket):
    message = await websocket.recv()
    print(message)

    return message

async def change_direction(websocket, new_dir):
    await websocket.send(json.dumps({"type": "move", "direction": new_dir}))
    
async def turn_left(websocket, current_direction):
    if current_direction == 1:
        new_direction = 4
        dir = "u"
    elif current_direction == 2:
        new_direction = 3
        dir = "d"
    elif current_direction == 3:
        new_direction = 1
        dir = "r"
    elif current_direction == 4:
        new_direction = 2
        dir = "l"

    await change_direction(websocket, dir)

    return new_direction

async def turn_right(websocket, current_direction):
    if current_direction == 1:
        new_direction = 3
        dir = "d"
    elif current_direction == 2:
        new_direction = 4
        dir = "u"
    elif current_direction == 3:
        new_direction = 2
        dir = "l"
    elif current_direction == 4:
        new_direction = 1
        dir = "r"

    await change_direction(websocket, dir)

    return new_direction

async def random_turn(websocket, current_direction):
    print("Turning")
    turn = random.randint(1, 2)
    if turn == 1:
        new_direction = await turn_left(websocket, current_direction)
    else:
        new_direction = await turn_right(websocket, current_direction)
    
    return new_direction


async def test(id):
    current_direction = "u"
    async with websockets.connect(app_url + str(id)) as websocket:
        bot_id = "/" + id
        await websocket.send(json.dumps({"type": "connect"}))
        message = await websocket.recv()
        message = json.loads(message)
        print(message)
        await asyncio.sleep(1)
        await websocket.send(json.dumps({"type": "spawn", "colour": "#00FF00"}))
        message = await websocket.recv()
        message = json.loads(message)
        print(message)

        bot_spawn_info = message["new_users"][bot_id]
        bot_head = bot_spawn_info["nodes"][0]
        bot_x = bot_head["x"]
        bot_y = bot_head["y"]
        bot_direction = bot_spawn_info["direction"]

        if bot_direction == {"x": 1, "y": 0}:
            direction = 1
        elif bot_direction == {"x": -1, "y": 0}:
            direction = 2
        elif bot_direction == {"x": 0, "y": 1}:
            direction = 3
        elif bot_direction == {"x": 0, "y": -1}:
            direction = 4
        
        print(direction)


        print(bot_spawn_info)

        while 1:
            message = await websocket.recv()
            message = json.loads(message)
            user_steps = message["user_steps"]
            dead_users = message["dead_clients"]
            if (bot_id) in user_steps:
                print("bot stepped")
                bot_x += bot_direction["x"]
                bot_y += bot_direction["y"]
                print("bot head is {}, {}".format(bot_x, bot_y))

                if (bot_y == 1 and direction != 1 and direction != 2) or (bot_x == 1 and direction != 3 and direction != 4) or (bot_x == 100 and direction != 3 and direction != 4) or (bot_y == 50 and direction != 1 and direction != 2):
                    direction = await random_turn(websocket, direction)
                    if direction == 1:
                        bot_direction = {"x": 1, "y": 0}
                    elif direction == 2:
                        bot_direction = {"x": -1, "y": 0}
                    elif direction == 3:
                        bot_direction = {"x": 0, "y": 1}
                    elif direction == 4:
                        bot_direction = {"x": 0, "y": -1}

                    
            print(message)

            

            if bot_id in dead_users:
                return


        #await asyncio.sleep(1)
        #print("Spawn")
        #await new(websocket, current_direction)

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