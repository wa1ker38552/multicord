from threading import Thread
from discord import op
import websocket
import asyncio
import signal
import json
import time
import sys


class Client:
    def __init__(self, token):
        self.token = token
        self.auth = {
            "token": self.token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": "pc"
            }
        }

        self.on_ready = []
        self.on_message = []
        self.on_message_update = []
        self.on_message_delete = []

    def event(self, func):
        if func.__name__ == 'on_ready':
            self.on_ready.append(func)
        elif func.__name__ == 'on_message':
            self.on_message.append(func)
        elif func.__name__ == 'on_edit':
            self.on_message_update.append(func)
        elif func.__name__ == 'on_delete':
            self.on_message_delete.append(func)

    def run(self):
        self.connect()
        for func in self.on_ready:
            asyncio.run(func())

    def send_to_socket(self, event, payload):
        self.socket.send(json.dumps({"op": event, "d": payload}))

    def connect(self):
        self.socket = websocket.WebSocket()
        self.socket.connect('wss://gateway.discord.gg/?v=9&encoding=json')
        self.send_to_socket(op.IDENTIFY, self.auth)
        response = json.loads(self.socket.recv())
        self.heartbeat_interval = (response["d"]["heartbeat_interval"]-2000)/1000
        Thread(target=self.send_heartbeat, daemon=True).start()
        Thread(target=self.recieve_messages, daemon=True).start()
        signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

        # block
        while True:
            time.sleep(0.1)

    def send_heartbeat(self):
        while self.heartbeat_interval is not None:
            self.send_to_socket(op.HEARTBEAT, self.auth)
            time.sleep(self.heartbeat_interval)

    def recieve_messages(self):
        while True:
            data = json.loads(self.socket.recv())
            if data['op'] == op.DISPATCH:     
                if data['t'] == 'MESSAGE_DELETE':
                    for func in self.on_message_delete:
                        asyncio.run(func(data))

                elif data['t'] == 'MESSAGE_UPDATE':
                    for func in self.on_message_update:
                        asyncio.run(func(data['d']))
                
                elif data['t'] == "MESSAGE_CREATE":
                    for func in self.on_message:
                        asyncio.run(func(data['d']))