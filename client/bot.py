import asyncio
import websockets, json, random
import requests, time, threading

local_host = False
max_x = 150
max_y = 100

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

if local_host:
    api_url = "http://localhost:5000/get/"
    app_url = "ws://127.0.0.1:8000/"
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
    

async def random_direction(websocket, bot_x, bot_y, current_letter_direction, player_nodes, bot_direction):
   
                
    valid_directions = []


    if bot_x != 1:
        valid_directions.append({"x": -1, "y": 0})
    if bot_x != max_x:
        valid_directions.append({"x": 1, "y": 0})

    if bot_y != 1:
        valid_directions.append({"x": 0, "y": -1})
    if bot_y != max_y:
        valid_directions.append({"x": 0, "y": 1})

    #print("Valids are {}".format(valid_directions))

    if bot_direction == {"x": 0, "y": -1} and {"x": 0, "y": 1} in valid_directions:
        valid_directions.remove({"x": 0, "y": 1})
    elif bot_direction == {"x": 0, "y": 1} and {"x": 0, "y": -1} in valid_directions:
        valid_directions.remove({"x": 0, "y": -1})
    elif bot_direction == {"x": -1, "y": 0} and "r" in valid_directions:
        valid_directions.remove({"x": 1, "y": 0})
    elif bot_direction == {"x": 1, "y": 0} and {"x": -1, "y": 0} in valid_directions:
        valid_directions.remove({"x": -1, "y": 0})

    #print("Bot is currently at {}, {}".format(bot_x, bot_y))
    #print("Valid directions are {}".format(valid_directions))
    good_directions = []
    for direction in valid_directions:
        #print("Test direction {}".format(direction))
        projected_bot_x = bot_x + direction["x"]
        projected_bot_y = bot_y + direction["y"]

        projected_bot_pos = {"x": projected_bot_x, "y": projected_bot_y}
        #print("Projected pos is {}".format(projected_bot_pos))

        evade = False
        for player in player_nodes:
            nodes = player_nodes[player]
            #print("Nodes for {} are {}".format(player, nodes))
            if projected_bot_pos in nodes:
                #print("Evade")
                evade = True
        
        if evade == False:
            good_directions.append(direction)
            #valid_directions.remove(direction)

    #print("Valid directions are {}".format(good_directions))
    if (len(good_directions) - 1) > 0:
        dir_index = random.randint(0, len(good_directions) - 1)
        #print("Dir_index is {}, dirs are {}".format(dir_index, valid_directions))
        bot_direction = good_directions[dir_index]

        if bot_direction == {"x": -1, "y": 0}:
            dir = "l"
        elif bot_direction == {"x": 1, "y": 0}:
            dir = "r"
        elif bot_direction == {"x": 0, "y": 1}:
            dir = "d"
        elif bot_direction == {"x": 0, "y": -1}:
            dir = "u"

        #print("Select {}: {}".format(dir, bot_direction))
        await change_direction(websocket, dir)


        return bot_direction, dir
    return {"x": 0, "y": -1}, "u"


async def play():
    while 1:
        response = requests.get(api_url)
        result = response.json()
        id = result["id"]
        async with websockets.connect(app_url + str(id)) as websocket:

            #print("Start")
            bot_id = "/" + id
            await websocket.send(json.dumps({"type": "connect"}))
            try:
                message = await websocket.recv()
                message = json.loads(message)
            except:
                return
            #print("Connection message is {}".format(message))
            #print(message)

            if ('data' not in message.keys()):
                return
            player_nodes = message["data"]["nodes"]
            player_directions = message["data"]["directions"]
            player_growth = {}

            for player in player_nodes.keys():
                if player in message["data"]["growth"].keys():
                    player_growth[player] = message["data"]["growth"][player]
                else:
                    player_growth[player] = 0
            

            await asyncio.sleep(1)
            color = "%06x" % random.randint(0, 0xFFFFFF)
            #print("Color is {}".format(color))
            await websocket.send(json.dumps({"type": "spawn", "colour": "#FFFFFF"}))
            message = await websocket.recv()
            message = json.loads(message)
            #print(message)
            #print("Intermediate message is {}".format(message))
            movements = message["movements"]
            for player in movements:
                player_new_direction = movements[player]
                player_directions[player] = player_new_direction
            new_players = message["new_users"]
            for new_player in new_players.keys():
                new_player_info = new_players[new_player]
                #print("New player info for {} is {}".format(new_player, new_player_info))
                player_nodes[new_player] = new_player_info["nodes"]
                player_directions[new_player] = new_player_info["direction"]
                player_growth[new_player] = new_player_info["growth"]

            added_growth = message["growth"]
            for player in added_growth:
                new_player_growth = added_growth[player]
                player_growth[player] += new_player_growth
                #print("Player growth is {}".format(player_growth))

            player_steps = message["user_steps"]
            for player in player_steps:
                player_direction = player_directions[player]
                if player_growth[player] > 0:
                    player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                    player_growth[player] -= 1
                else:
                    player_direction = player_directions[player]
                    player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                    player_nodes[player].pop()

            if bot_id not in message["new_users"].keys():
                while bot_id not in message["new_users"].keys():
                    message = await websocket.recv()
                    message = json.loads(message)
                    #print("Intermediate message is {}".format(message))
                    movements = message["movements"]
                    for player in movements:
                        player_new_direction = movements[player]
                        player_directions[player] = player_new_direction
                    new_players = message["new_users"]
                    for new_player in new_players.keys():
                        new_player_info = new_players[new_player]
                        #print("New player info for {} is {}".format(new_player, new_player_info))
                        player_nodes[new_player] = new_player_info["nodes"]
                        player_directions[new_player] = new_player_info["direction"]
                        player_growth[new_player] = new_player_info["growth"]

                    added_growth = message["growth"]
                    for player in added_growth:
                        new_player_growth = added_growth[player]
                        player_growth[player] += new_player_growth
                        #print("Player growth is {}".format(player_growth))

                    player_steps = message["user_steps"]
                    for player in player_steps:
                        player_direction = player_directions[player]
                        if player_growth[player] > 0:
                            player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                            player_growth[player] -= 1
                        else:
                            player_direction = player_directions[player]
                            player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                            player_nodes[player].pop()


            #print("Spawn message is {}".format(message))
            new_players = message["new_users"]
            for new_player in new_players.keys():
                new_player_info = new_players[new_player]
                #print("New player info for {} is {}".format(new_player, new_player_info))
                player_nodes[new_player] = new_player_info["nodes"]
                player_directions[new_player] = new_player_info["direction"]
                player_growth[new_player] = new_player_info["growth"]

            added_growth = message["growth"]
            for player in added_growth:
                new_player_growth = added_growth[player]
                player_growth[player] += new_player_growth
                #print("Player growth is {}".format(player_growth))
                

            player_steps = message["user_steps"]
            for player in player_steps:
                player_direction = player_directions[player]
                if player_growth[player] > 0:
                    player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                    player_growth[player] -= 1
                else:
                    player_direction = player_directions[player]
                    player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                    player_nodes[player].pop()

            #print("Player nodes are {}".format(player_nodes))

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

            idle_steps = random.randint(7, 20)
            #idle_steps = 2
            step = 1

            living = True
            while living:
                try:
                    message = await websocket.recv()
                except:
                    return
                message = json.loads(message)
                #print(message)
                movements = message["movements"]
                for player in movements:
                    player_new_direction = movements[player]
                    player_directions[player] = player_new_direction
                new_players = message["new_users"]
                for new_player in new_players.keys():
                    new_player_info = new_players[new_player]
                    #print("New player info for {} is {}".format(new_player, new_player_info))
                    player_nodes[new_player] = new_player_info["nodes"]
                    player_directions[new_player] = new_player_info["direction"]
                    player_growth[new_player] = new_player_info["growth"]

                added_growth = message["growth"]
                for player in added_growth:
                    new_player_growth = added_growth[player]
                    player_growth[player] += new_player_growth
                    #print("Player growth is {}".format(player_growth))

                player_steps = message["user_steps"]
                for player in player_steps:
                    player_direction = player_directions[player]
                    if player_growth[player] > 0:
                        player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                        player_growth[player] -= 1
                    else:
                        player_direction = player_directions[player]
                        player_nodes[player].insert(0, {"x": player_nodes[player][0]["x"] + player_direction["x"], "y": player_nodes[player][0]["y"] + player_direction["y"]})
                        player_nodes[player].pop()


                user_steps = message["user_steps"]
                dead_users = message["dead_clients"]
                if (bot_id) in user_steps:
                    #print("bot stepped")


                    
                    bot_x += bot_direction["x"]
                    bot_y += bot_direction["y"]
                    

                    if step != idle_steps:
                        step += 1
                    else:
                        step = 1

                    projected_x = bot_x + bot_direction["x"]
                    projected_y = bot_y + bot_direction["y"]
                    projected_node = {"x": projected_x, "y": projected_y}

                    #if projected_node in player_nodes[bot_id]:
                    #    print("TRIGGER")

                    dodge = False

                    for other_player in player_nodes.keys():
                        if other_player != bot_id:
                            if projected_node in player_nodes[other_player]:
                                dodge = True
                                break

                

                    if step == idle_steps or bot_y == 1 or bot_y == max_y or bot_x == 1 or bot_x == max_x or projected_node in player_nodes[bot_id] or dodge:
                        bot_direction, direction = await random_direction(websocket, bot_x, bot_y, direction, player_nodes, bot_direction)
                        idle_steps = random.randint(7, 20)
                        #idle_steps = 2
                        step = 1

                

                if bot_id in dead_users:
                    #print("WE DIED")
                    living = False


            #await asyncio.sleep(1)
            #print("Spawn")
            #await new(websocket, current_direction)

async def test():
    while 1:
        try:
            await play()
        except:
            pass

async def speed_up(period, websocket):
    websocket.send(json.dumps({"type": "increase_speed"}))
    time.sleep(period)
    websocket.send(json.dumps({"type": "decrease_speed"}))






for r in range (0, 1000):
    choose_direction()


def new2():
    
    #print(id)


    while (1):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(test())

#asyncio.get_event_loop().run_until_complete(test(id))





def create():
    time.sleep(0.01)
    _thread2 = threading.Thread(target=new2, args=())
    _thread2.start()
    _thread2.join()

    _thread2 = threading.Thread(target=new2, args=())
    _thread2.start()
    _thread2.join()

abormal_termination = False


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
    for index in range(12):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()
#e
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)