# generated by datamodel-codegen:
#   filename:  pause_game.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel

from tank_royal_manager.robocode_event_models import MessageType


class PauseGame(BaseModel):
    type: MessageType = MessageType.PauseGame