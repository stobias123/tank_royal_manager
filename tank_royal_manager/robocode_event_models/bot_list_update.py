# generated by datamodel-codegen:
#   filename:  bot_list_update.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from . import bot_info, MessageType


class BotListUpdate(BaseModel):
    type: MessageType = MessageType.BotListUpdate
    bots: List[bot_info.BotInfo] = Field(..., description='List of bots')