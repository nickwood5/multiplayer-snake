import asyncio
import websockets
from concurrent.futures import ProcessPoolExecutor
import time, threading
from multiprocessing import Process

list = []
connected_users = []
available_ids = [1, 2, 3, 4, 5, 6, 7, 8]
players = 0

async def echo(websocket, client):
    global players
    print("Cleint is {}".format(client))
    if client in available_ids:
        print("Taking id {}".format(client))
        available_ids.remove(int(client[1:]))

    async for message in websocket:
        #if message == "assign_id":
        #    players += 1
        #    await websocket.send(players)
        #else:
        if message == "assign_id":
            players += 1
            print("Assign ID {}".format(players))
            await websocket.send(str(players))
        else:
            print(client)
            connected_users.append(client)
            print(message)
            list.append(message)
            await websocket.send(message)

async def echo2(websocket):
    print("Local websocket")
    print(min(available_ids))
    user_id = min(available_ids)
    await websocket.send(str(user_id) + "USER ID")
    available_ids.remove(user_id)
    print(available_ids)
async def test():
    while (1):
        time.sleep(1)
        print("Hey")
        print("List is {}".format(list))
        print(players)
        print(connected_users)

async def main():
    print("Main")
    print(time.time())
    async with websockets.serve(echo, "0.0.0.0", 8080):
    #async with websockets.serve(echo, "127.0.0.1", 8764):
        await asyncio.Future()  # run forever

async def head():
    task1 = asyncio.create_task(main())
    #task2 = asyncio.create_task(test())
    await task1


#start_server = websockets.serve(echo, 'localhost', 8765)

#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()


async def main2():
    print("Main2")
    print(time.time())
    async with websockets.serve(echo2, "127.0.0.1", 8080):
        await asyncio.Future()  # run forever

async def local_websocket():
    await main2()

def local_websocket_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(local_websocket())
    loop.close()

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
_thread3 = threading.Thread(target=local_websocket_callback, args=())
_thread.start()
_thread2.start()
_thread3.start()