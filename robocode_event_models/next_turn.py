# generated by datamodel-codegen:
#   filename:  next_turn.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel

from robocode_event_models import MessageType


class NextTurn(BaseModel):
    type: MessageType = MessageType.NextTurn
