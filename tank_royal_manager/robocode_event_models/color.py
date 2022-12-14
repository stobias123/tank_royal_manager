# generated by datamodel-codegen:
#   filename:  color.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from pydantic import BaseModel, Field, constr


class Color(BaseModel):
    __root__: str = Field(
        ...,
        description='Represents a color using hexadecimal format for web colors. Note that colors must have a leading number sign (#).\nSee https://en.wikipedia.org/wiki/Web_colors\n',
        examples=[
            '#000',
            '// black "#FFF"',
            '// white "#0F0"',
            '// lime "#000000"',
            '// black "#FFFFFF"',
            '// white "#00FF00"',
            '// lime "#FFA07A"',
            '// light salmon "#9932CC"  // dark orchid',
        ],
        title='Color',
    )
