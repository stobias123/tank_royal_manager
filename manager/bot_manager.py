import websocket
from robocode_event_models import bot_handshake
from robocode_event_models import bot_list_update
import logging




class BotManager:
    def __init__(self, name: str, conn: websocket.WebSocket):
        self.conn = conn
        self.handshake = bot_handshake.BotHandshake(
            name=name,
            version='1.0',
            secret="abc123",
            authors=["stobias"],
            countryCodes=["US"],
            gameTypes=["1v1","melee","classic"]
        )

    def connect(self):
        self.conn.send(self.handshake.json())

    async def connect_and_listen(self) -> bot_list_update.BotListUpdate:
        await self.conn.send(self.handshake.json())
        raw = await self.conn.recv()
        return bot_list_update.BotListUpdate.parse_raw(raw)

    async def connect_and_listen_forever(self):
        await self.conn.send(self.handshake.json())
        while True:
            raw = await self.conn.recv()
            logging.info(f"[BotManager] {raw}")