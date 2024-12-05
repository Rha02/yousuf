from datetime import datetime
from pydantic import BaseModel

class Chat(BaseModel):
    id: str
    user_id: str
    title: str
    last_messaged_at: datetime
