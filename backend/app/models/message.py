from pydantic import BaseModel

class MessageData(BaseModel):
    content: str

class History(BaseModel):
    type: str
    data: MessageData

class Message(BaseModel):
    id: str
    session_id: str
    history: History
