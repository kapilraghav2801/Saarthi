from pydantic import BaseModel


class ExecutionResult(BaseModel):

    success: bool
    message: str
    reason: str | None = None