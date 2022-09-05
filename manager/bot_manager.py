import json

import websocket
from robocode_event_models import bot_handshake, Message, MessageType
from robocode_event_models import bot_list_update
import logging


class BotManager:
    def __init__(self, name: str, conn: websocket.WebSocket):
        self.conn = conn
        self.bot_name = name
        self.handshake = bot_handshake.BotHandshake(
            name=name,
            version='1.0',
            secret="abc123",
            authors=["stobias"],
            countryCodes=["US"],
            gameTypes=["1v1", "melee", "classic"]
        )

    async def connect_and_listen(self) -> bot_list_update.BotListUpdate:
        json = self.handshake.json()
        await self.conn.send(self.handshake.json())
        raw = await self.conn.recv()
        logging.info(f"[BotManager] [{self.bot_name}] {raw}")
        return bot_list_update.BotListUpdate.parse_raw(raw)

    async def connect_and_listen_forever(self):
        json = self.handshake.json()
        await self.conn.send(json)
        while True:
            raw = await self.conn.recv()
            logging.info(f"[BotManager] [{self.handshake.name}] {raw}")


class MessageHandler:
    def __init(self):
        pass

    ## Todo test when m does not have type.
    async def handleMessage(self, strmessage):
        m = json.loads(strmessage)
        str_type = m['type']
        if str_type == MessageType.BotListUpdate:
            logging.info(str_type)
