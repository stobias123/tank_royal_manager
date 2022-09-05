# generated by datamodel-codegen:
#   filename:  bullet_fired_event.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from . import bullet_state


class BulletFiredEvent(BaseModel):
    bullet: Optional[bullet_state.BulletState] = Field(
        None, description='Bullet that was fired'
    )
