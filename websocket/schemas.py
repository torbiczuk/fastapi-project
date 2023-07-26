from typing import Optional

from pydantic import BaseModel


class MicrowaveState(BaseModel):
    on: bool = False
    power: int = 0
    counter: int = 0


class ClientMessage(MicrowaveState):
    action: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
