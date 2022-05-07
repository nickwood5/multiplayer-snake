import asyncio
from calendar import c
from pydoc import cli
from struct import pack
import websockets
import time, threading, json

list = []
connected_users = []
alive_clients = []
available_ids = [1, 2, 3, 4, 5, 6, 7, 8]
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

head_positions = {}
movements = {}
moves = {}
inactivity = {}
player_nodes = {}
player_growth = {}

client_sockets = {}

fruits = [{"x": 20, "y": 20}]

async def echo(websocket, client):
    async for message in websocket:
        if message == "c":
            connected_users.append(client)
            alive_clients.append(client)
            new_users.append(client)
            head_positions[client] = {"x": 2, "y": 3}
            moves[client] = ['u']
            movements[client] = {"x": 0, "y": -1}
            client_sockets[client] = websocket
            inactivity[client] = 0

            # Pick a spawn location for player
            player_nodes[client] = []
            player_nodes[client].append(head_positions[client])
            player_growth[client] = 5
            package = {"data": {}}
            package['data']["nodes"] = player_nodes
            package['data']["directions"] = movements
            package['data']["growth"] = player_growth
            package['data']['fruits'] = fruits

            #print("Transmit {}".format(package))
            await websocket.send(json.dumps(package))
        else:
            
            #print("Client {} sent message {}".format(client, message))

            if len(moves[client]) == 0:
                moves[client].append(message)
            else:
                if message == "u":
                    if moves[client][-1] != ("u" or "d"):
                        moves[client].append(message)
                elif message == "d":
                    if moves[client][-1] != ("u" or "d"):
                        moves[client].append(message)
                elif message == "l":
                    if moves[client][-1] != ("l" or "r"):
                        moves[client].append(message)
                elif message == "r":
                    if moves[client][-1] != ("l" or "r"):
                        moves[client].append(message)
            #print("MOVES ARE {}".format(moves))

async def send(client, data):
    await client.send(data)

async def test():
    while (1):
        time.sleep(0.1)
        start_time = time.time()
        #print("Hey")
        #print("List is {}".format(list))
        #print(players)
        #print(inactivity)
        #print(connected_users)
        changes = {"movements": {}, "new_users": {}, "dead_clients": {}, "growth": {}}


        if len(new_users) > 0:
            #print(new_users)
            for new_user in new_users:
                changes["new_users"][new_user] = {}
                changes["new_users"][new_user]["nodes"] = player_nodes[new_user]
                changes["new_users"][new_user]["direction"] = movements[new_user]
                changes["new_users"][new_user]["growth"] = player_growth[new_user]

            new_users.clear()
            

        for client in connected_users:
            print("CHECKING CLIENT {} CONNECTION".format(client))
            if client in alive_clients:
                print({"CLIENT {} LIVES".format(client)})
                if len(moves[client]) > 0:
                    #print("Change client {} direction".format(client))
                    if moves[client][0] == "u":
                        if movements[client]["y"] == 0:
                            movements[client]["y"] = -1
                            movements[client]["x"] = 0

                            changes["movements"][client] = movements[client]
                            #print(movements[client])
                    elif moves[client][0] == "d":
                        if movements[client]["y"] == 0:
                            movements[client]["y"] = 1
                            movements[client]["x"] = 0

                            changes["movements"][client] = movements[client]
                            #print(movements[client])
                    elif moves[client][0] == "l":
                        if movements[client]["x"] == 0:
                            movements[client]["x"] = -1
                            movements[client]["y"] = 0
    
                            changes["movements"][client] = movements[client]
                            #print(movements[client])
                    elif moves[client][0] == "r":
                        if movements[client]["x"] == 0:
                            movements[client]["x"] = 1
                            movements[client]["y"] = 0

                            changes["movements"][client] = movements[client]
                            #print(movements[client])
                    moves[client].pop(0)
                    inactivity[client] = 0
                else:
                    inactivity[client] += 1

                if player_growth[client] > 0:
                    print("GROWING SNAKE!!!!")
                    player_nodes[client].insert(0, {"x": player_nodes[client][0]["x"] + movements[client]["x"], "y": player_nodes[client][0]["y"] + movements[client]["y"]} ) 
                    player_growth[client] -= 1
                else:
                    print("GROWING SNAKE!!!")
                    player_nodes[client].insert(0, {"x": player_nodes[client][0]["x"] + movements[client]["x"], "y": player_nodes[client][0]["y"] + movements[client]["y"]} )
                    player_nodes[client].pop()
                
                print(player_nodes)
            else:
                inactivity[client] += 1
          
            if inactivity[client] > 100:
                dead_clients.append(client)
                connected_users.remove(client)       
                #alive_clients.remove(client)
        
        dead_clients = []

        for client in alive_clients:
            # Check collisions
            player_head = player_nodes[client][0]
            player_collision = False
            for target_client in alive_clients:
                if client != target_client:
                    #print("Client {} nodes:".format(target_client))
  
                    if player_head in player_nodes[target_client]:
                        #print("Client {} hit client {}".format(client, target_client))
                        dead_clients.append(client)
                        player_collision = True
                        break
            if not player_collision:
                if player_head["x"] == 0 or player_head["x"] == 51 or player_head["y"] == 0 or player_head["y"] == 51:
                    print("CLIENT {} HIT THE WALL".format(client))
                    dead_clients.append(client)
                    player_collision = True
            if not player_collision:
                for fruit_position in fruits:
                    if player_head == fruit_position:
                        #print("Player {} ate fruit {}".format(client, fruit_position))
                        player_growth[client] += 5
                        changes["growth"][client] = 5
                        break



        if dead_clients:
            changes["dead_clients"] = dead_clients
            


        #print("Changes are {}".format(changes))
        if changes["movements"] or changes["new_users"] or changes["dead_clients"] or changes["growth"]:
            print("SENDING AN UPDATE PACKET: {}".format(changes))
            for client in connected_users:
                #print("Sending data to {}!!".format(client))
                try:
                    await client_sockets[client].send(json.dumps(changes))
                except:
                    #print("Couldnt send")
                    pass
        else:
            print("SENDING A STEP MESSAGE")
            for client in connected_users:
                print("Sending data to {}".format(client))
                try:
                    await client_sockets[client].send("s")
                except:
                    print("Couldnt send")
                    pass
        end_time = time.time()
        time_elapsed = end_time - start_time

        if dead_clients:
            print(dead_clients)
            print(alive_clients)
            for dead_client in dead_clients:
                alive_clients.remove(dead_client)
                player_nodes.pop(dead_client)
                movements.pop(dead_client)
                player_growth.pop(dead_client)

            dead_clients.clear()

        #print("Time elapsed was {}".format(time_elapsed))
async def main():
    print("Main")
    print(time.time())
    #async with websockets.serve(echo, "0.0.0.0", 8080):
    async with websockets.serve(echo, "127.0.0.1", 8764):
        await asyncio.Future()  # run forever

async def head():
    task1 = asyncio.create_task(main())
    #task2 = asyncio.create_task(test())
    await task1


#start_server = websockets.serve(echo, 'localhost', 8765)

#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()

async def some_callback():
    await main()

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




_thread = threading.Thread(target=between_callback, args=())
_thread2 = threading.Thread(target=new, args=())
_thread.start()
_thread2.start()