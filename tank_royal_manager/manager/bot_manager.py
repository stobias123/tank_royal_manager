import json
import threading

import websocket
from pydantic import BaseModel
import rel

from tank_royal_manager.robocode_event_models import *
import logging


class BotManager:
    def __init__(self, name: str, ws_addr: str):
        self.session_id = ''
        self.bot_name = name
        self.conn = None
        self.bots: List[ScannedBotEvent] = []
        self.bot_state: BotState = None
        rel.signal(2, rel.abort)
        self.thread = threading.Thread(target=rel.dispatch)

    def start_thread(self):
        self.conn.run_forever(dispatcher=rel, reconnect=True)
        self.thread.start()

    def stop_thread(self):
        rel.abort()

    def connect(self):
        handshake = bot_handshake.BotHandshake(
            name=self.bot_name,
            sessionId=self.session_id,
            version='1.0',
            secret="abc123",
            authors=["stobias"],
            countryCodes=["US"],
            gameTypes=["1v1", "melee", "classic"]
        )
        self.conn.send(handshake.json())

    def handle_message(self):
        print("Not Implemented")


class BaseBotMessageHandler(BotManager):
    def __init__(self, name: str, ws_addr: str):
        super().__init__(name, ws_addr)
        self.intent = BotIntent()
        logging.info(f"[BotManager] Trying to connect to {ws_addr}")
        self.conn = websocket.WebSocketApp(
            url=ws_addr,
            on_message=self.handle_message
        )
        self.last_tick = None
        self.queued_intent = None
        self.BOT_MESSAGE_MAP = {
            MessageType.BotListUpdate: BotListUpdate,
            MessageType.GameStartedEventForBot: GameStartedEventForBot,
            MessageType.RoundStartedEvent: RoundStartedEvent,
            MessageType.TickEventForBot: TickEventForBot,
            MessageType.SkippedTurnEvent: SkippedTurnEvent,
            MessageType.GameAbortedEvent: GameAbortedEvent,
            MessageType.GameEndedEventForBot: GameEndedEventForBot,
            MessageType.ServerHandshake: ServerHandshake
        }

        self.BOT_FUNC_MAP = {
            MessageType.GameStartedEventForBot: self.handle_game_started,
            MessageType.RoundStartedEvent: self.handle_round_started,
            MessageType.TickEventForBot: self.handle_tick,
            MessageType.SkippedTurnEvent: self.handle_skip,
            MessageType.GameAbortedEvent: self.handle_game_aborted,
            MessageType.ServerHandshake: self.server_handshake,
            MessageType.GameEndedEventForBot: self.handle_game_ended
        }

    def log_open(self, ws, message):
        logging.debug(f"[BotManager] Connected")

    def log_error(self, ws, message):
        logging.debug(f"[BotManager] Error")
    # parse_message parses the message type so that we can construct an object,
    # then returns the correct (python) type for that message.
    def deserialize_message(self, str_message: str) -> BaseModel:
        m = json.loads(str_message)
        try:
            return self.BOT_MESSAGE_MAP[MessageType[m['type']]](**m)
        except KeyError as e:
            logging.error(f"Key error, incoming message did not match a message type. \n {str_message}")

    def handle_message(self, ws, str_message: str):
        logging.debug(f"[Bot] - {str_message}")
        m = self.deserialize_message(str_message)
        if m is None:
            logging.error(f"Problem with the message deserialization")
        return self.BOT_FUNC_MAP[m.type](m)

    # handle game ended
    def handle_game_ended(self, game_ended_event: GameEndedEventForBot):
        logging.info(f"[{self.bot_name}]  -- GameEnd Event -- {game_ended_event}")

    def handle_game_started(self, event: GameStartedEventForBot):
        logging.debug(f"[{self.bot_name}] Received game started event!")
        self.conn.send(BotReady().json())

    def handle_game_aborted(self, game_aborted_event: GameAbortedEvent):
        logging.info(f"[ControllerManager] Round Aborted!")
        #exit(0)

    def handle_round_started(self, event: RoundStartedEvent):
        logging.debug(f"[{self.bot_name}] Received round started event!")
        self.conn.send(BotReady().json())

    def handle_tick(self, tick: TickEventForBot):
        logging.debug(f"[{self.bot_name}] BotTick {tick.json()}")

    def handle_skip(self, skip_event: SkippedTurnEvent):
        # logging.warn(f"[{self.bot_name}] Warning - Skipped a turn")
        pass

    def server_handshake(self, handshake: ServerHandshake):
        self.session_id = handshake.sessionId
        logging.debug(f"[{self.bot_name}] Server Handshake received.")
        self.connect()


class ScanAndFireBot(BaseBotMessageHandler):
    def handle_tick(self, tick: TickEventForBot):
        self.conn.send(BotIntent(firepower=1).json())


class DriveAndScanBot(BaseBotMessageHandler):
    def __init__(self, man: BotManager):
        super().__init__(man)
        self.bot_map = {}

    def handle_tick(self, tick: TickEventForBot):
        intent = BotIntent(targetSpeed=1, radarTurnRate=999)
        self.conn.send(intent.json())
        if len(tick.events) > 0:
            self.parse_events(tick.events)

    def parse_events(self, events: List[dict]):
        for event in events:
            if event['type'] == 'ScannedBotEvent':
                botEvent = ScannedBotEvent(**event)
                self.bot_map[botEvent.scannedBotId] = botEvent
