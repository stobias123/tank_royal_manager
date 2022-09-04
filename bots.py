import json
from builtins import type

import asyncio
import websockets
import concurrent.futures

from manager.controller_manager import ControllerManager
from manager.bot_manager import BotManager
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


WS_ADDR = "ws://localhost:7654"

# wsapp = websocket.WebSocketApp(WS_ADDR, on_message=on_message)
# wsapp.run_forever()

bots = []


async def startBot1():
    async with websockets.connect(WS_ADDR) as botSocket:
        bot1 = BotManager(name="bot1", conn=botSocket)
        botUpdate = await bot1.connect_and_listen_forever()

async def startBot2():
    async with websockets.connect(WS_ADDR) as botSocket:
        bot2 = BotManager(name="bot2", conn=botSocket)
        botUpdate = await bot2.connect_and_listen_forever()
        #bots.append(bot_info_to_bot_update(botUpdate.bots[0]))

async def main():
    controller: ControllerManager
    asyncio.create_task(startBot1())
    asyncio.create_task(startBot2())
    async with websockets.connect(WS_ADDR) as controller_socket:
        ## Start the server.
        controller = ControllerManager(controller_socket)
        await controller.connect_and_listen()
        await controller.listen_forever()



if __name__ == "__main__":
    asyncio.run(main())