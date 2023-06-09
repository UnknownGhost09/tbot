import threading
import time
import websocket
import json
from random import randint
from .models import BotStop



class Main():
    def __init__(self):
        while True:
            delay = randint(5, 10)
            ws = websocket.create_connection("ws://127.0.0.1:8000")
            obj=BotStop.objects.get(id='1')
            data={'status':obj.status}

            ws.send(data)
            data = ws.recv()
            ws.close()
            data = json.loads(data)
            time.sleep(delay)






