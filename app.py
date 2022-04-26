import asyncio
import websockets
import time, threading, json

list = []
connected_users = []
available_ids = [1, 2, 3, 4, 5, 6, 7, 8]
players = 0

def get_new_id():
    id = 0
    while id in connected_users:
        id += 1
    print("Valid id is {}".format(id))
    return id

head_positions = {}
movements = {}
moves = {}
inactivity = {}

client_sockets = {}

async def echo(websocket, client):
    async for message in websocket:
        if client not in connected_users:
            connected_users.append(client)
            moves[client] = []
            head_positions[client] = {"x": 0, "y": 0}
            movements[client] = {"x": 0, "y": 0}
            client_sockets[client] = websocket
            inactivity[client] = 0
        print("Client {} sent message {}".format(client, message))

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
        print("MOVES ARE {}".format(moves))
        await websocket.send("AAAA")

async def send(client, data):
    await client.send(data)

async def test():
    while (1):
        time.sleep(0.05)
        print("Hey")
        print("List is {}".format(list))
        print(players)
        print(inactivity)
        print(connected_users)
        changes = {}

        for client in connected_users:
            if len(moves[client]) > 0:
                print("Change client {} direction".format(client))
                if moves[client][0] == "u":
                    if movements[client]["y"] == 0:
                        movements[client]["y"] = -1
                        movements[client]["x"] = 0

                        changes[client[1:]] = movements[client]
                        print(movements[client])
                elif moves[client][0] == "d":
                    if movements[client]["y"] == 0:
                        movements[client]["y"] = 1
                        movements[client]["x"] = 0

                        changes[client[1:]] = movements[client]
                        print(movements[client])
                elif moves[client][0] == "l":
                    if movements[client]["x"] == 0:
                        movements[client]["x"] = -1
                        movements[client]["y"] = 0
 
                        changes[client[1:]] = movements[client]
                        print(movements[client])
                elif moves[client][0] == "r":
                    if movements[client]["x"] == 0:
                        movements[client]["x"] = 1
                        movements[client]["y"] = 0

                        changes[client[1:]] = movements[client]
                        print(movements[client])
                moves[client].pop(0)
                inactivity[client] = 0
            else:
                inactivity[client] += 1

            head_positions[client]["x"] += movements[client]["x"]
            head_positions[client]["y"] += movements[client]["y"]

        print("Changes are {}".format(changes))
        if changes:
            for client in connected_users:
                print("Sending data to {}".format(client))
                try:
                    await client_sockets[client].send(json.dumps(changes))
                except:
                    print("Couldnt send")
                    pass

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