import websocket

class EventManager:
    def __init__(self, conn: websocket.WebSocket):
        self.conn = conn

