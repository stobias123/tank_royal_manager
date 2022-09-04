from robocode_event_models import ControllerHandshake, BotAddress, StartGame, NextTurn
from manager.game_types import *
from typing import List, Optional
import logging


HANDSHAKE = ControllerHandshake(
    name='gym_server',
    version='1.0',
    secret="abc123")


class ControllerManager:
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        self.conn.send(HANDSHAKE.json())

    async def connect_and_listen(self):
        await self.conn.send("hello")
        logging.info("[ControllerManager]" + await self.conn.recv())
        await self.conn.send(HANDSHAKE.json())
        result = await self.conn.recv()
        return result

    async def listen_forever(self):
        await self.conn.send(HANDSHAKE.json())
        while True:
            raw = await self.conn.recv()
            logging.info(f"[ControllerManager] {raw}")

    async def start(self, bots: List[BotAddress]):
        packet = StartGame(
            gameSetup=STANDARD,
            botAddresses=bots
        )
        await self.conn.send(packet.json())
        logging.info(f"Game setup is: \n{await self.conn.recv()}")

    async def step(self):
        packet = NextTurn()
        await self.conn.send(packet.json())
        res = await self.conn.recv()
        return res
