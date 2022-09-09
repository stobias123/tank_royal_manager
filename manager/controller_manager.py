import json
import time
from time import sleep

from pydantic import BaseModel

from robocode_event_models import *
from manager.game_types import *
from typing import List, Optional
import logging
import websocket


class ControllerManager:
    def __init__(self, ws_address: str, turn_limit: int = 500):
        self.message_handler = ControllerMessageHandler(self)
        self.session_id = ''
        self.conn = websocket.WebSocketApp(
            url=ws_address,
            on_message=self.message_handler.handle_message,
            on_close=self.close,
            on_error=self.error
        )
        self.turn_count = 0
        self.turn_limit = turn_limit
        self.bot_list: List[BotAddress] = []
        self.step_ready = True
        #logging.info("[ControllerManager] Connected: " + self.conn.recv())
        logging.info("[ControllerManager] Connected")

    def handshake(self):
        HANDSHAKE = ControllerHandshake(
            name='gym_server',
            sessionId=self.session_id,
            version='1.0',
            secret="abc123")
        self.conn.send(HANDSHAKE.json())
        #logging.info("[ControllerManager] Handshake " + self.conn.recv())
        logging.info("[ControllerManager] Handshake")

    def start(self):
        packet = StartGame(
            gameSetup=STANDARD,
            botAddresses=self.bot_list
        )
        self.conn.send(packet.json())
    def error(self, ws , e):
        logging.info("Websocket Error")
        exit(0)
    def close(self, ws, close_status_code, close_msg):
        logging.info("Websocket Lost")
        exit(0)

    def pause(self):
        self.conn.send(PauseGame().json())

    def stop(self):
        self.conn.send(StopGame().json())

    def step(self):
        packet = NextTurn()
        self.conn.send(packet.json())
        # res = self.conn.recv()
        # return res


class ControllerMessageHandler:
    def __init__(self, man: ControllerManager):
        self.man = man
        self.CONTROLLER_MESSAGE_MAP = {
            MessageType.BotListUpdate: BotListUpdate,
            MessageType.RoundStartedEvent: RoundStartedEvent,
            MessageType.TickEventForObserver: TickEventForObserver,
            MessageType.GameStartedEventForObserver: GameStartedEventForObserver,
            MessageType.GameAbortedEvent: GameAbortedEvent,
            MessageType.GameEndedEventForObserver: GameEndedEventForObserver,
            MessageType.GamePausedEventForObserver: GamePausedEventForObserver,
            MessageType.GameResumedEventForObserver: GameResumedEventForObserver,
            MessageType.ServerHandshake: ServerHandshake,
            MessageType.PauseGame: PauseGame
        }

        self.BOT_FUNC_MAP = {
            MessageType.BotListUpdate: self.handle_bot_list_update,
            MessageType.RoundStartedEvent: self.handle_round_start,
            MessageType.TickEventForObserver: self.handle_tick,
            MessageType.GameStartedEventForObserver: self.handle_game_start,
            MessageType.GameAbortedEvent: self.handle_game_aborted,
            MessageType.GameEndedEventForObserver: self.handle_game_aborted,
            MessageType.GamePausedEventForObserver: self.handle_pause,
            MessageType.GameResumedEventForObserver: self.handle_pause,
            MessageType.PauseGame: self.handle_pause,
            MessageType.ServerHandshake: self.handle_server_handshake
        }

    # parse_message parses the message type so that we can construct an object,
    # then returns the correct (python) type for that message.
    def deserialize_message(self, str_message: str) -> BaseModel:
        m = json.loads(str_message)
        try:
            type = m['type']
            return self.CONTROLLER_MESSAGE_MAP[MessageType[m['type']]](**m)
        except KeyError as e:
            logging.error(f"Key error, incoming message did not match a message type. \n {str_message}")

    def handle_message(self, ws, str_message: str):
        m = self.deserialize_message(str_message)
        return self.BOT_FUNC_MAP[m.type](m)

    def handle_pause(self, event: Event):
        logging.debug(f"[ControllerManager] Paused")

    def handle_bot_list_update(self, bot_list: BotListUpdate):
        # Clear it b/c we get a whole new array every time.
        self.man.bot_list = []
        for bot in bot_list.bots:
            self.man.bot_list.append(BotAddress(host=bot.host, port=bot.port))
        if len(self.man.bot_list) > 1:
            self.man.start()

    def handle_round_start(self, round_start_event: RoundStartedEvent):
        logging.debug(f"[ControllerManager] Round Started!")
        self.man.pause()
        ##self.man.conn.send(PauseGame().json())

    def handle_game_start(self, round_start_event: GameStartedEventForObserver):
        """
        handle_game_start starts the round as soon as we get a round start event.
        :param round_start_event:
        :return:
        """
        logging.debug(f"[ControllerManager] Game Started!")
    def handle_server_handshake(self, handshake: ServerHandshake):
        self.man.session_id = handshake.sessionId
        logging.debug(f"[ControllerManager] Handshake received")
        self.man.handshake()

    def handle_game_aborted(self, game_aborted_event: GameAbortedEvent):
        logging.info(f"[ControllerManager] Round Aborted! Exiting!")
        exit(0)

    def handle_game_ended(self, game_aborted_event: GameEndedEventForObserver):
        logging.info(f"[ControllerManager] Round Ended! Exiting!")
        exit(0)

    def handle_tick(self, tick_event: TickEventForObserver):
        if self.man.turn_count >= self.man.turn_limit:
            self.man.conn.send(StopGame().json())
        self.man.turn_count = self.man.turn_count + 1
        if self.man.turn_count % 50 == 0:
            logging.info(f"[ControllerManager] Tick {self.man.turn_count}\n {tick_event.json()}")
