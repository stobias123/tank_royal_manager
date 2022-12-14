# generated by datamodel-codegen:
#   filename:  initial_position.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class InitialPosition(BaseModel):
    x: Optional[float] = Field(
        None,
        description='The x coordinate. When it is not set, a random value will be used.',
    )
    y: Optional[float] = Field(
        None,
        description='The y coordinate. When it is not set, a random value will be used.',
    )
    angle: Optional[float] = Field(
        None, description='The angle. When it is not set, a random value will be used.'
    )
