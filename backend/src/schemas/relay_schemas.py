from typing import Literal

from pydantic import BaseModel, Field


class StatusQuery(BaseModel):
    device_id: str = Field(default="node1", description="Device ID")
    relay_id: int = Field(default=1, gt=0, description="Relay ID")
    state: Literal["on", "off"]
