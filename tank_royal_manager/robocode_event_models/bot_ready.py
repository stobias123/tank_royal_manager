# generated by datamodel-codegen:
#   filename:  bot_ready.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel

from tank_royal_manager.robocode_event_models import MessageType


class BotReady(BaseModel):
    type: MessageType = MessageType.BotReady
