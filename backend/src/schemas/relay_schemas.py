from typing import Literal

from pydantic import BaseModel, Field


class StatusQuery(BaseModel):
    node_id: int = Field(default=1, gt=0, description="Node ID")
    status: Literal["on", "off"]
