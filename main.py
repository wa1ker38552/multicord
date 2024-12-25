from flask_socketio import SocketIO
from flask import render_template
from flask_socketio import emit
from flask import redirect
from flask import request
from flask import Flask

from discord.client import Client
from database import Database
from threading import Thread


app = Flask(__name__)
client = Client(open('token.txt', 'r').read())
socket = SocketIO(app)
db = Database('config.json')

import api_routes # api routes located in a seperate file so it's more clean

@app.route('/')
def app_index():
    return render_template('index.html')

@client.event
async def on_message(message):
    socket.emit('MESSAGE_CREATE', message)

Thread(target=client.run, daemon=True).start()
socket.run(app, host='0.0.0.0', port=8080, debug=True)
# app.run(host='0.0.0.0', port=8080, debug=True)