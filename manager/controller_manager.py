import json

from pydantic import BaseModel

from robocode_event_models import ControllerHandshake, BotAddress, StartGame, NextTurn, MessageType, BotListUpdate
from manager.game_types import *
from typing import List, Optional
import logging
import websocket


class ControllerManager:
    def __init__(self, ws_address):
        self.conn = websocket.WebSocket()
        self.conn.connect(ws_address)
        self.message_handler = ControllerMessageHandler(self)
        self.bot_list: List[BotAddress] = []
        logging.info("[ControllerManager]" + self.conn.recv())

    def connect_and_listen(self):
        HANDSHAKE = ControllerHandshake(
            name='gym_server',
            version='1.0',
            secret="abc123")
        self.conn.send(HANDSHAKE.json())
        logging.info("[ControllerManager]" + self.conn.recv())

    def listen_forever(self):
        while True:
            raw = self.conn.recv()
            self.message_handler.handle_message(raw)
            logging.info(f"[ControllerManager] {raw}")

    def handle_message(self, str_message):
        m = json.loads(str_message)
        str_type = m['type']
        if str_type == MessageType.BotListUpdate.value:
            bot_list_update = BotListUpdate(**m)
            for bot in bot_list_update.bots:
                self.bot_list.append(BotAddress(host=bot.host, port=bot.port))

    def start(self):
        packet = StartGame(
            gameSetup=STANDARD,
            botAddresses=self.bot_list
        )
        self.conn.send(packet.json())
        logging.info(f"[ControllerManager] Game Started! Game setup is: \n{self.conn.recv()}")

    def step(self):
        packet = NextTurn()
        self.conn.send(packet.json())
        res = self.conn.recv()
        return res


class ControllerMessageHandler:
    def __init__(self, man: ControllerManager):
        self.man = man
        self.CONTROLLER_MESSAGE_MAP = {
            MessageType.BotListUpdate: BotListUpdate,
        }

        self.BOT_FUNC_MAP = {
            MessageType.BotListUpdate: self.handle_bot_list_update
        }

    # parse_message parses the message type so that we can construct an object,
    # then returns the correct (python) type for that message.
    def deserialize_message(self, str_message: str) -> BaseModel:
        m = json.loads(str_message)
        try:
            return self.CONTROLLER_MESSAGE_MAP[MessageType[m['type']]](**m)
        except KeyError as e:
            logging.error(f"Key error, incoming message did not match a message type. \n {str_message}")

    def handle_message(self, str_message: str):
        m = self.deserialize_message(str_message)
        test = type(m)
        return self.BOT_FUNC_MAP[m.type](m)

    def handle_bot_list_update(self, bot_list: BotListUpdate):
        # Clear it b/c we get a whole new array every time.
        self.man.bot_list = []
        for bot in bot_list.bots:
            self.man.bot_list.append(BotAddress(host=bot.host, port=bot.port))
        if len(self.man.bot_list) > 1:
            logging.debug(f"[ControllerManager] Starting this bitch.")
            self.man.start()
