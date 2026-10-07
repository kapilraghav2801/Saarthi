from pydantic import BaseModel

class ACStatus(BaseModel):

    power: str
    mode: str
    target_temperature: int
    room_temperature: int
    fan_speed: str