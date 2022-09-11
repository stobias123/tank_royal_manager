# generated by datamodel-codegen:
#   filename:  game_started_event_for_observer.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from . import game_setup, participant, MessageType


class GameStartedEventForObserver(BaseModel):
    type: MessageType = MessageType.GameStartedEventForObserver
    gameSetup: game_setup.GameSetup = Field(..., description='Game setup')
    participants: List[participant.Participant] = Field(
        ..., description='List of bots participating in this battle'
    )