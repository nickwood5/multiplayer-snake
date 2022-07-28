from flask import Flask, jsonify
import flask, uuid
from flask_cors import CORS
#from waitress import serve
#from flask_restful import Api

#local_host = False

#if local_host:
#    address = 'localhost'
#    port = 8769
#else:
#    address = "0.0.0.0"
#    port = 8080

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    resp = flask.make_response(jsonify({"API": "HI"}))
    return resp

@app.route('/get/')
def get():
    id = uuid.uuid4()
    print("Adding user {}".format(id))
    resp = flask.make_response(jsonify({"id": id}))
    return resp

if __name__ == '__main__':
    print("STARTING APP UP")
    app.run()