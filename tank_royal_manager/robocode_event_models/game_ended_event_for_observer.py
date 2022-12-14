# generated by datamodel-codegen:
#   filename:  game_ended_event_for_observer.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from . import bot_results_for_observer, MessageType


class GameEndedEventForObserver(BaseModel):
    type: MessageType = MessageType.GameEndedEventForObserver
    numberOfRounds: int = Field(..., description='Number of rounds played')
    results: List[bot_results_for_observer.BotResultsForObserver] = Field(
        ..., description='Results of the battle'
    )
