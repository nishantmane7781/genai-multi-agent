from pydantic import BaseModel
from typing import List


class AgentResponse(BaseModel):
    summary: str
    key_points: List[str]
    sources: List[str]