from pydantic import BaseModel

class State(BaseModel):
    query: str
    