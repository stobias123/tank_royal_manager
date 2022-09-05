# generated by datamodel-codegen:
#   filename:  controller_handshake.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from .message import MessageType


class ControllerHandshake(BaseModel):
    type: MessageType = MessageType.ControllerHandshake
    name: str = Field(
        ..., description='Name of controller, e.g. Fancy Robocode Controller'
    )
    version: str = Field(..., description='Controller version, e.g. 1.0')
    author: Optional[str] = Field(
        None, description='Author name, e.g. John Doe (john_doe@somewhere.net)'
    )
    secret: Optional[str] = Field(
        None, description='Secret used for access control with the server'
    )