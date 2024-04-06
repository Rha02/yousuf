from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    password: str
    first_name: str
    last_name: str
