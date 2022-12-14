# generated by datamodel-codegen:
#   filename:  tick_event_for_observer.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from . import bot_state_with_id, bullet_state, event, MessageType


class TickEventForObserver(BaseModel):
    type: MessageType = MessageType.TickEventForObserver
    roundNumber: int = Field(
        ..., description='The current round number in the battle when event occurred'
    )
    botStates: List[bot_state_with_id.BotStateWithID] = Field(
        ..., description='Current state of all bots'
    )
    bulletStates: List[bullet_state.BulletState] = Field(
        ..., description='Current state of all bullets'
    )
    events: List[event.Event] = Field(
        ..., description='All events occurring at this tick'
    )
