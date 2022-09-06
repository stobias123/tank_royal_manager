import json

import websocket
from pydantic import BaseModel

from robocode_event_models import bot_handshake, Message, MessageType, GameStartedEventForBot, BotReady, BotListUpdate
from robocode_event_models import bot_list_update
import logging


class BotManager:
    def __init__(self, name: str, ws_addr: str):
        self.conn = websocket.WebSocket()
        self.conn.connect(ws_addr)
        self.bot_name = name
        logging.info(f"[{self.bot_name}] Init: " + self.conn.recv())
        self.handler = BotMessageHandler(man=self)

        self.handshake = bot_handshake.BotHandshake(
            name=name,
            version='1.0',
            secret="abc123",
            authors=["stobias"],
            countryCodes=["US"],
            gameTypes=["1v1", "melee", "classic"]
        )

    def connect(self):
        handshake_json = self.handshake.json()
        self.conn.send(handshake_json)

    def listen_forever(self):
        while True:
            raw = self.conn.recv()
            logging.info("Wow this is bad code.")
            self.handler.handle_message(str_message=raw)


class BotMessageHandler:
    def __init__(self, man: BotManager):
        self.man = man
        self.BOT_MESSAGE_MAP = {
            MessageType.BotListUpdate: BotListUpdate,
            MessageType.GameStartedEventForBot: GameStartedEventForBot
        }

        self.BOT_FUNC_MAP = {
            MessageType.GameStartedEventForBot: self.handle_game_started,
            MessageType.RoundStartedEvent: self.handle_round_started
        }

    # parse_message parses the message type so that we can construct an object,
    # then returns the correct (python) type for that message.
    def deserialize_message(self, str_message: str) -> BaseModel:
        m = json.loads(str_message)
        try:
            return self.BOT_MESSAGE_MAP[MessageType[m['type']]](**m)
        except KeyError as e:
            logging.error(f"Key error, incoming message did not match a message type. \n {str_message}")

    def handle_message(self, str_message: str):
        m = self.deserialize_message(str_message)
        if m is None:
            logging.error(f"Problem with the message deserializagion")
        return self.BOT_FUNC_MAP[m.type](m)

    def handle_game_started(self, event: GameStartedEventForBot):
        logging.debug(f"[{self.man.bot_name}] Received game started event!")
        self.man.conn.send(BotReady().json())
    def handle_round_started(self, event: RoundStartedEvent):
        logging.debug(f"[{self.man.bot_name}] Received game started event!")
        self.man.conn.send(BotReady().json())
