from pydantic import BaseModel

class BrowserCommand(BaseModel):
    type: str
    url: str | None = None
    query: str | None = None