# generated by datamodel-codegen:
#   filename:  bullet_hit_wall_event.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel, Field

from . import bullet_state


class BulletHitWallEvent(BaseModel):
    bullet: bullet_state.BulletState = Field(
        ..., description='Bullet that has hit a wall'
    )
