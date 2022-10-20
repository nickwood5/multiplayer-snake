import asyncio
import websockets
import time, threading, json
import random
import signal
import os

game_width = 150
game_height = 100

local_host = False
index = 0

step_length = 2
step = 1

if local_host:
    address = "127.0.0.1"
    port = 8770
else:
    address = "0.0.0.0"
    port = 8080

list = []
connected_users = []
alive_clients = []
players = 0



new_users = []

def remove_client(client):
    connected_users.remove(client)
    movements.pop(client)
    moves.pop(client)
    inactivity.pop(client)
    player_nodes.pop(client)
    player_growth.pop(client)
    client_sockets.pop(client)

movements = {}
moves = {}
inactivity = {}
player_nodes = {}
player_growth = {}
player_colours = {}
player_speeds = {}
player_names = {}

client_sockets = {}

fruits = []

def createFruit():
    global player_nodes, fruits

    valid_fruit_position = False
    while valid_fruit_position == False:

        y = random.randint(1, game_height)
        x = random.randint(1, game_width)
        location = {"x": x, "y": y}

        valid_fruit_position = True
        for client in player_nodes.keys():
            if location in player_nodes[client]:
                valid_fruit_position = False
                break

        if location in fruits:
            valid_fruit_position = False

    return location





for a in range (0, 30):
    fruit = createFruit()
    fruits.append(createFruit())


async def connection_handler(websocket, client):
    global connected_users, inactivity, client_sockets, player_nodes, movements, player_growth, fruits, player_colours, player_names

    connected_users.append(client)         
    inactivity[client] = 0
    client_sockets[client] = websocket
    
    package = {"data": {}}
    package['data']["nodes"] = player_nodes
    package['data']["directions"] = movements
    package['data']["growth"] = player_growth
    package['data']['fruits'] = fruits
    package['data']['colours'] = player_colours
    package['data']['names'] = player_names

    await websocket.send(json.dumps(package))


def choose_spawn_position():
    global player_nodes, fruits

    valid_spawn = False
    while valid_spawn == False:
        x = random.randint(5, game_width - 5)
        y = random.randint(5, game_height - 5)

        location = {"x": x, "y": y}

        valid_spawn = True

        for client in player_nodes.keys():
            if location in player_nodes[client]:
                valid_spawn = False
                break

        if location in fruits:
            valid_spawn = False
    
    return location

def spawn_handler(message, client):
    global alive_clients, new_users, player_nodes, player_growth, player_colours, player_speeds, moves, movements, player_names

    player_colour = message["colour"]
    player_name = message["name"]

    player_names[client] = player_name
    player_colours[client] = player_colour
    

    new_users.append(client)

def move_handler(message, client):
    global moves

    new_direction = message["direction"]

    if len(moves[client]) == 0:
        moves[client].append(new_direction)
    else:
        #print(moves[client])
        if new_direction == "u":
            if len(moves[client]) > 0:
                if moves[client][-1] != "u" and  moves[client][-1] != "d":
                    moves[client].append(new_direction)
            else:
                moves[client].append(new_direction)
        elif new_direction == "d":
            if len(moves[client]) > 0:
                if moves[client][-1] != "u" and  moves[client][-1] != "d":
                    moves[client].append(new_direction)
            else:
                moves[client].append(new_direction)
        elif new_direction == "l":
            if len(moves[client]) > 0:
                if moves[client][-1] != "l" and  moves[client][-1] != "r":
                    moves[client].append(new_direction)
            else:
                moves[client].append(new_direction)
        elif new_direction == "r":
            if len(moves[client]) > 0:
                if moves[client][-1] != "l" and  moves[client][-1] != "r":
                    moves[client].append(new_direction)
            else:
                moves[client].append(new_direction)


async def input_handler(websocket, client):
    global connected_users, player_speeds

    async for message in websocket:
        message = json.loads(message)
        input_type = message["type"]

        if input_type == "connect":
            await connection_handler(websocket, client)
            
        elif input_type == "spawn" and client in connected_users:
            spawn_handler(message, client)
            
        elif input_type == "move" and client in alive_clients:
            move_handler(message, client)
        
        elif input_type == "increase_speed" and client in alive_clients:
            player_speeds[client] = 1

        elif input_type == "decrease_speed" and client in alive_clients:
            player_speeds[client] = 2


async def send(client, data):
    await client.send(data)


def update_moves(client, changes):
    global moves, movements, inactivity

    if moves[client][0] == "u":
        if movements[client]["y"] == 0:
            movements[client]["y"] = -1
            movements[client]["x"] = 0
            changes["movements"][client] = movements[client]
    elif moves[client][0] == "d":
        if movements[client]["y"] == 0:
            movements[client]["y"] = 1
            movements[client]["x"] = 0
            changes["movements"][client] = movements[client]
    elif moves[client][0] == "l":
        if movements[client]["x"] == 0:
            movements[client]["x"] = -1
            movements[client]["y"] = 0
            changes["movements"][client] = movements[client]
    elif moves[client][0] == "r":
        if movements[client]["x"] == 0:
            movements[client]["x"] = 1
            movements[client]["y"] = 0
            changes["movements"][client] = movements[client]

    moves[client].pop(0)
    inactivity[client] = 0

def move_snake(client, changes, user_steps):
    global inactivity, player_growth, player_nodes, movements

    user_steps.append(client)

    if len(moves[client]) > 0:
        update_moves(client, changes)
    else:
        inactivity[client] += 1

    player_nodes[client].insert(0, {"x": player_nodes[client][0]["x"] + movements[client]["x"], "y": player_nodes[client][0]["y"] + movements[client]["y"]})

    if player_growth[client] > 0:
        player_growth[client] -= 1
        
    else:
        player_nodes[client].pop()

    return user_steps


def random_direction():
    dir = random.randint(1, 4)

    if dir == 1:
        bot_direction = {"x": -1, "y": 0}
        letter_direction = "l"
    elif dir == 2:
        bot_direction = {"x": 1, "y": 0}
        letter_direction = "r"
    elif dir == 3:
        bot_direction = {"x": 0, "y": 1}
        letter_direction = "d"
    elif dir == 4:
        bot_direction = {"x": 0, "y": -1}
        letter_direction = "u"

    return bot_direction, letter_direction


async def test():
    global index, step, changes, player_nodes, movements, player_growth, player_colours, pending_clients, connected_users, alive_clients, new_users, player_speeds, inactivity, fruits, player_names
    alive_disconnected_clients = []
    while (1):
        users_added = 0
        
        start_time = time.time()

        changes = {"movements": {}, "new_users": {}, "dead_clients": {}, "growth": {}, "new_fruits": [], "eaten_fruits": []}
        pending_clients = []
        if len(new_users) > 0:
            for new_user in new_users:
                pos = choose_spawn_position()

                player_nodes[new_user] = []
                player_nodes[new_user].append(pos)
                player_growth[new_user] = 5
                player_speeds[new_user] = 2

                dir, letter_dir = random_direction()
                moves[new_user] = [letter_dir]
                movements[new_user] = dir
                alive_clients.append(new_user)
                changes["new_users"][new_user] = {}
                changes["new_users"][new_user]["nodes"] = player_nodes[new_user]
                changes["new_users"][new_user]["direction"] = movements[new_user]
                changes["new_users"][new_user]["growth"] = player_growth[new_user]
                changes["new_users"][new_user]["colours"] = player_colours[new_user]
                changes["new_users"][new_user]["names"] = player_names[new_user]

                users_added += 1

        user_steps = []

        for client in connected_users:
            if client in alive_clients and client not in new_users and client not in pending_clients:
                if player_speeds[client] == 2:
                    if step == 2:
                        user_steps = move_snake(client, changes, user_steps)
                elif player_speeds[client] == 1:
                    user_steps = move_snake(client, changes, user_steps)

            else:
                inactivity[client] += 1
        
        changes["user_steps"] = user_steps

        new_users.clear()
        
        dead_clients = []

        for client in alive_clients:
            # Check collisions
            player_head = player_nodes[client][0]
            player_collision = False
            for target_client in alive_clients:
                if player_collision:
                    break
                for node_num in range (0, len(player_nodes[target_client])):
                    node = player_nodes[target_client][node_num]
                    if player_head == node:
                        if client == target_client:
                            if node_num != 0:
                                dead_clients.append(client)
                                player_collision = True
                                break
                        else:
                            player_growth[target_client] += 5
                            changes["growth"][target_client] = 5
                            dead_clients.append(client)
                            player_collision = True
                            break

            if not player_collision:
                if player_head["x"] == 0 or player_head["x"] == (game_width + 1) or player_head["y"] == 0 or player_head["y"] == (game_height + 1):
                    dead_clients.append(client)
                    player_collision = True
            if not player_collision:
                for fruit_position in fruits:
                    if player_head["x"] == fruit_position["x"] and player_head["y"] == fruit_position["y"]:
                        fruits.remove(fruit_position)
                        new_fruit = createFruit()
                        fruits.append(new_fruit)
                        changes["new_fruits"].append(new_fruit)
                        player_growth[client] += 5

                        if client in changes["growth"].keys():
                            changes["growth"][client] += 5
                        else:
                            changes["growth"][client] = 5
                        changes["eaten_fruits"].append({"x": fruit_position["x"], "y": fruit_position["y"]})
                        break


        if dead_clients:
            changes["dead_clients"] = dead_clients
            for client in dead_clients:
                if client in user_steps:
                    user_steps.remove(client)

        if changes["movements"] or changes["new_users"] or changes["dead_clients"] or changes["growth"] or changes["user_steps"]:
            changes["index"] = index
            for client in connected_users:
                try:
                    await client_sockets[client].send(json.dumps(changes))
                except:
                    alive_disconnected_clients.append(client)
                    pass

        if dead_clients:
            for dead_client in dead_clients:

                alive_clients.remove(dead_client)
                if dead_client in player_nodes:
                    player_nodes.pop(dead_client)
                movements.pop(dead_client)
                player_growth.pop(dead_client)
                if dead_client in alive_disconnected_clients:
                    connected_users.remove(dead_client)
                    alive_disconnected_clients.remove(dead_client)
            dead_clients.clear()

        index += 1

        if step == step_length:
            step = 1
        else:
            step += 1

        end_time = time.time()
        time_elapsed = end_time - start_time

        sleep_time = 0.05 - time_elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("Not sleeping, because the function took {} seconds. Added {} users. {} alive clients".format(time_elapsed, users_added, len(alive_clients)))

async def main():
    async with websockets.serve(
        input_handler,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await asyncio.Future()


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
    loop.close()


def new():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(test())
    loop.close()
    

input_thread = threading.Thread(target=between_callback, args=())
game_thread = threading.Thread(target=new, args=())
input_thread.start()
game_thread.start()
game_thread.join()