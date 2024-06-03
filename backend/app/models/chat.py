from pydantic import BaseModel

class Chat(BaseModel):
    id: str
    user_id: str
    title: str
