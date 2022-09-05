# generated by datamodel-codegen:
#   filename:  change_tps.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ChangeTPS(BaseModel):
    tps: Optional[int] = Field(
        None,
        description='Turns per second (TPS). Typically a value from 0 to 999. -1 means maximum possible TPS speed.',
    )