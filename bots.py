import json
import threading
from builtins import type

import asyncio
from time import sleep

import websockets
import concurrent.futures

from manager.controller_manager import ControllerManager
from manager.bot_manager import BotManager
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

WS_ADDR = "ws://localhost:7654"

# wsapp = websocket.WebSocketApp(WS_ADDR, on_message=on_message)
# wsapp.run_forever()

bots = []


if __name__ == "__main__":
    controller_manager = ControllerManager(WS_ADDR)
    controller_manager.connect_and_listen()

    bot1 = BotManager('bot1', WS_ADDR)
    bot1.connect()

    bot2 = BotManager('bot2', WS_ADDR)
    bot2.connect()

    t = threading.Thread(target=controller_manager.listen_forever)
    bot1 = threading.Thread(target=bot1.listen_forever)
    bot2 = threading.Thread(target=bot2.listen_forever)

    t.start()
    bot1.start()
    bot2.start()
