from pydantic import BaseModel

from app.models.action import SaarthiAction


class ActionPlan(BaseModel):
    actions: list[SaarthiAction]