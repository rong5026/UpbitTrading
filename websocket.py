import asyncio
import pprint
import websockets
import json


async def upbit_ws_client():
    uri = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(uri) as websocket:
        subscribe_fmt = [
            {"ticket": "test"},
            {
                "type": "ticker",
                "codes": ["KRW-BTC"],
                "isOnlyRealtime": True
            },
           # {"format": "SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            if websocket.open:

                data = await websocket.recv()
                data = json.loads(data)
                pprint.pprint( data)
            else:
                print("연결 안됨")

loop = asyncio.get_event_loop()
asyncio.ensure_future(upbit_ws_client())
loop.run_forever()


#async def main():
#    await upbit_ws_client()


#asyncio.run(main())