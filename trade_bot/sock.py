import asyncio
import json
import websockets
        # from .models import BotStop

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            with open('botstatus.json','r') as fl:
                event=fl.read()
                print(event)
            await websocket.send(event)
        except:
            pass 

async def main():
    async with websockets.serve(handler, "192.168.29.20", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())