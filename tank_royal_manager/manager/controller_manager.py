import json
import threading
import time
from time import sleep

import rel as rel
from pydantic import BaseModel

from tank_royal_manager.robocode_event_models import *
from tank_royal_manager.manager.game_types import *
from typing import List, Optional
import logging
import websocket


class BaseControllerManager:
    def __init__(self, ws_address: str):
        self.session_id = ''
        self.conn = None
        self.turn_count = 0
        self.roundNumber = 0
        self.bot_list: List[BotAddress] = []
        self.step_ready = True
        self.game_over = False
        self.reset_turn = False
        # logging.info("[ControllerManager] Connected: " + self.conn.recv())
        logging.info("[ControllerManager] Connected")

    def start_thread(self):
        self.conn.run_forever(dispatcher=rel, reconnect=True)
        rel.signal(2, rel.abort)
        thread = threading.Thread(target=rel.dispatch)
        thread.start()

    def handshake(self):
        HANDSHAKE = ControllerHandshake(
            name='gym_server',
            sessionId=self.session_id,
            version='1.0',
            secret="abc123")
        self.conn.send(HANDSHAKE.json())
        # logging.info("[ControllerManager] Handshake " + self.conn.recv())
        logging.info("[ControllerManager] Handshake")

    def start(self):
        self.game_over = False
        self.reset_turn = True
        packet = StartGame(
            gameSetup=STANDARD,
            botAddresses=self.bot_list
        )
        self.conn.send(packet.json())

    def handle_message(self, ws, str_message: str):
        print("Not Implemented")

    def error(self, ws, e):
        if type(e) == websocket.WebSocketConnectionClosedException:
            logging.warning("Websocket errored out. Retrying connection.")
            rel.abort()
            self.conn.run_forever(dispatcher=rel, reconnect=True)
            rel.signal(2, rel.abort)
            rel.dispatch()
            return
        else:
            logging.warning(f"Websocket Error {e}")

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        rel.abort()
        self.conn.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def pause(self):
        self.conn.send(PauseGame().json())

    def stop(self):
        self.conn.send(StopGame().json())

    def end_round(self):
        self.conn.send(RoundEndedEvent(
            roundNumber=self.roundNumber,
            turnNumber=self.turn_count,
        ).json())
        self.roundNumber += 1

    def step(self):
        packet = NextTurn()
        self.conn.send(packet.json())
        # res = self.conn.recv()
        # return res


class ControllerManager(BaseControllerManager):
    def __init__(self, ws_address: str):
        super().__init__(ws_address)
        self.conn = websocket.WebSocketApp(
            url=ws_address,
            on_message=self.handle_message
        )
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
            MessageType.GameEndedEventForObserver: self.handle_game_ended,
            MessageType.GamePausedEventForObserver: self.handle_pause,
            MessageType.GameResumedEventForObserver: self.handle_pause,
            MessageType.PauseGame: self.handle_pause,
            MessageType.ServerHandshake: self.handle_server_handshake
        }

    def log_open(self, ws, message):
        logging.debug("[ControllerManager] Connected")

    def log_error(self, ws, message):
        logging.debug("[ControllerManager] Error")

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
        self.bot_list = []
        for bot in bot_list.bots:
            self.bot_list.append(BotAddress(host=bot.host, port=bot.port))
        if len(self.bot_list) > 1:
            self.start()

    def handle_round_start(self, round_start_event: RoundStartedEvent):
        logging.debug(f"[ControllerManager] Round Started!")
        self.pause()
        ##self.conn.send(PauseGame().json())

    def handle_game_start(self, round_start_event: GameStartedEventForObserver):
        """
        handle_game_start starts the round as soon as we get a round start event.
        :param round_start_event:
        :return:
        """
        logging.debug(f"[ControllerManager] Game Started!")

    def handle_server_handshake(self, handshake: ServerHandshake):
        self.session_id = handshake.sessionId
        logging.debug(f"[ControllerManager] Handshake received")
        self.handshake()

    def handle_game_aborted(self, game_aborted_event: GameAbortedEvent):
        if not self.reset_turn:
            self.game_over = True
            logging.info(f"[ControllerManager] Game Aborted!")
        else:
            self.reset_turn = False
            logging.info("[ControllerManager] Game Aborted Event - Were in a reset turn..")
        # exit(0)

    def handle_game_ended(self, game_aborted_event: GameEndedEventForObserver):
        if (not self.reset_turn):
            self.game_over = True
            logging.info(f"[ControllerManager] Round Ended!")
        else:
            logging.info("[ControllerManager] Game Ended event - Were in a reset turn..")
            self.reset_turn = False
        # exit(0)

    def handle_tick(self, tick_event: TickEventForObserver):
        self.turn_count = self.turn_count + 1
        if self.turn_count % 50 == 0:
            logging.info(f"[ControllerManager] Tick {self.turn_count}\n {tick_event.json()}")
