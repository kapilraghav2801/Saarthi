from pydantic import BaseModel

class SaarthiAction(BaseModel):
    domain: str    
    action: str
    target: str
    action_confidence: float
    target_confidence: float
    query: str | None = None
    value: str | int | float | None = None




