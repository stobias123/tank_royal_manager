import asyncio
import websockets
from manager.controller_manager import ControllerManager

WS_ADDR = "ws://localhost:7654"

bots = []

async def printer(websocket):
    async for message in websocket:
        print(message)

async def run_controller(ws):
    controller = ControllerManager(ws)
    await controller.connect_and_listen()
    print("connected")
    await asyncio.sleep(15)
    for i in range(10):
        await controller.step()

async def main():
    async with websockets.connect(WS_ADDR) as controller_socket:
        ## Print all messages
        printerTask = asyncio.create_task(printer(controller_socket))
        ## Start the controller....
        controllerTask =  asyncio.create_task(run_controller(controller_socket))
        await asyncio.wait([printerTask,controllerTask])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()