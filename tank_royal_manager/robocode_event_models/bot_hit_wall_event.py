# generated by datamodel-codegen:
#   filename:  bot_hit_wall_event.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class BotHitwallEvent(BaseModel):
    victimId: int = Field(..., description='ID of the victim bot that hit the wall')
