from .repository import DatabaseRepository
from app.models.user import User
from app.models.chat import Chat
from driver.driver import MongoDB

class MongoDBRepository(DatabaseRepository):
    """MongoDB implementation of a database repository"""

    def __init__(self, client: MongoDB):
        self.db = client.db

    def get_user_by_email(self, email: str) -> User | None:
        res = self.db.users.find_one({"email": email})
        if not res:
            return None
        
        user = User(
            id=str(res["_id"]),
            email=res["email"],
            password=res["password"],
            first_name=res["first_name"],
            last_name=res["last_name"]
        )
        return user
    
    def get_user_by_id(self, user_id: str) -> User | None:
        res = self.db.users.find_one({"_id": user_id})
        if not res:
            return None
        
        user = User(
            id=str(res["_id"]),
            email=res["email"],
            password=res["password"],
            first_name=res["first_name"],
            last_name=res["last_name"]
        )
        return user
    
    def create_user(self, user: User) -> User | None:
        res = self.db.users.insert_one(user.model_dump())
        user.id = str(res.inserted_id)
        return user
    
    def get_chats(self, user_id: str) -> list[Chat]:
        res = self.db.chats.find({"user_id": user_id})
        chats = []

        for chat in res:
            chats.append(Chat(
                id=str(chat["_id"]),
                user_id=chat["user_id"],
                title=chat["title"]
            ))
        
        return chats
    
    def create_chat(self, chat: Chat) -> Chat | None:
        res = self.db.chats.insert_one(chat.model_dump())
        chat.id = str(res.inserted_id)
        return chat