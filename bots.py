import threading
from time import sleep

import rel

# ws = websocket.WebSocketApp()
# ws.send()

from tank_royal_manager.manager.controller_manager import ControllerManager
from tank_royal_manager.manager.bot_manager import *
from tank_royal_manager.manager.game_types import STANDARD
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

WS_ADDR = "ws://localhost:7654"

# wsapp = websocket.WebSocketApp(WS_ADDR, on_message=on_message)
# wsapp.run_forever()

bots = []

if __name__ == "__main__":
    controller_manager = ControllerManager(WS_ADDR)
    controller_manager.start_thread()

    messageHandler = DriveAndScanBot
    fireBot = ScanAndFireBot

    bot1 = BotManager('bot1', WS_ADDR, messageHandler)
    bot2 = BotManager('bot2', WS_ADDR, fireBot)

    bot1.start_thread()
    bot2.start_thread()
    sleep(10)
    #bot1 = threading.Thread(target=bot1.conn.run_forever)
    #bot2 = threading.Thread(target=bot2.conn.run_forever)

    #bot1.start()
    #bot2.start()
    for i in range(0, 501):
        if i % 100 == 0:
            logging.info("Steppin bitch")
        controller_manager.step()
        ## Sleep just a bit longer than the turn timeout.
        ## I think that sometimes, if we send next turn event out of sequence, then the tick event doesn't go right?
        sleep((STANDARD.turnTimeout / 1000000) + .01)
    logging.info("Finished!")
