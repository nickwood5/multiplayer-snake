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

    return message

async def change_direction(websocket, new_dir):
    await websocket.send(json.dumps({"type": "move", "direction": new_dir}))
    

async def random_direction(websocket, bot_x, bot_y, current_letter_direction):
    valid_directions = []

    if bot_x != 1:
        valid_directions.append("l")
    if bot_x != 100:
        valid_directions.append("r")

    if bot_y != 1:
        valid_directions.append("u")
    if bot_y != 50:
        valid_directions.append("d")

    #print("Valids are {}".format(valid_directions))


    if current_letter_direction == "u" and "d" in valid_directions:
        valid_directions.remove("d")
    elif current_letter_direction == "d" and "u" in valid_directions:
        valid_directions.remove("u")
    elif current_letter_direction == "l" and "r" in valid_directions:
        valid_directions.remove("r")
    elif current_letter_direction == "r" and "l" in valid_directions:
        valid_directions.remove("l")

    dir_index = random.randint(0, len(valid_directions) - 1)
    #print("Dir_index is {}, dirs are {}".format(dir_index, valid_directions))
    dir = valid_directions[dir_index]
    if dir == "l":
        bot_direction = {"x": -1, "y": 0}
    elif dir == "r":
        bot_direction = {"x": 1, "y": 0}
    elif dir == "d":
        bot_direction = {"x": 0, "y": 1}
    elif dir == "u":
        bot_direction = {"x": 0, "y": -1}


    await change_direction(websocket, dir)

    return bot_direction, dir


async def test(id):
    async with websockets.connect(app_url + str(id)) as websocket:
        bot_id = "/" + id
        await websocket.send(json.dumps({"type": "connect"}))
        message = await websocket.recv()
        message = json.loads(message)
        #print(message)
        await asyncio.sleep(1)
        await websocket.send(json.dumps({"type": "spawn", "colour": "#00FF00"}))
        message = await websocket.recv()
        message = json.loads(message)
        #print(message)

        while bot_id not in message["new_users"].keys():
            message = await websocket.recv()
            message = json.loads(message)


        bot_spawn_info = message["new_users"][bot_id]
        bot_head = bot_spawn_info["nodes"][0]
        bot_x = bot_head["x"]
        bot_y = bot_head["y"]
        bot_direction = bot_spawn_info["direction"]

        if bot_direction == {"x": 1, "y": 0}:
            direction = 'r' # R
        elif bot_direction == {"x": -1, "y": 0}:
            direction = "l" # L
        elif bot_direction == {"x": 0, "y": 1}:
            direction = "d" # D
        elif bot_direction == {"x": 0, "y": -1}:
            direction = "u" # U
        
        #print(direction)
        


        #print(bot_spawn_info)

        idle_steps = 20
        step = 1

        while 1:
            message = await websocket.recv()
            message = json.loads(message)
            user_steps = message["user_steps"]
            dead_users = message["dead_clients"]
            if (bot_id) in user_steps:
                #print("bot stepped")
  

                
                bot_x += bot_direction["x"]
                bot_y += bot_direction["y"]
                #print("bot head is {}, {}".format(bot_x, bot_y))

                if step != idle_steps:
                    step += 1
                else:
                    step = 1

                if step == idle_steps or bot_y == 1 or bot_y == 50 or bot_x == 1 or bot_x == 100:
                    bot_direction, direction = await random_direction(websocket, bot_x, bot_y, direction)

            

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
    for index in range(5):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        time.sleep(0.5)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)