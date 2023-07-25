from pydantic import BaseModel


class MicrowaveState(BaseModel):
    on: bool = False
    power: int = 0
    counter: int = 0
