import asyncio
import websockets
from concurrent.futures import ProcessPoolExecutor
import time, threading
from multiprocessing import Process
from flask import Flask, jsonify
import flask
from flask_cors import CORS
import waitress
list = []
connected_users = []
players = 0


app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET', 'POST'])
def aaaa():
    resp = flask.make_response(jsonify({"Nick API": "ONLINE"}))
    return resp

async def echo(websocket, client):
    global players

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
        await asyncio.Future()  # run forever

async def head():
    task1 = asyncio.create_task(main())
    #task2 = asyncio.create_task(test())
    await task1


#start_server = websockets.serve(echo, 'localhost', 8765)

#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()



async def tt():
    print("Tt")

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

def api():
    waitress.serve(app, host='0.0.0', port=8080)


_thread = threading.Thread(target=between_callback, args=())
_thread2 = threading.Thread(target=new, args=())
_thread3 = threading.Thread(target=api, args=())
_thread.start()
_thread2.start()
_thread3.start()
