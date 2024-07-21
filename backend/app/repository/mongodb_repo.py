import json
from app.models.message import History, Message, MessageData
from .repository import DatabaseRepository
from app.models.user import User
from app.models.chat import Chat
from driver.driver import MongoDB
from bson import ObjectId

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
        res = self.db.users.find_one({"_id": ObjectId(user_id)})
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
    
    def get_chat_by_id(self, chat_id: str) -> Chat | None:
        res = self.db.chats.find_one({"_id": ObjectId(chat_id)})
        if not res:
            return None
        
        chat = Chat(
            id=str(res["_id"]),
            user_id=res["user_id"],
            title=res["title"]
        )
        return chat
    
    def create_chat(self, chat: Chat) -> Chat | None:
        res = self.db.chats.insert_one(chat.model_dump())
        chat.id = str(res.inserted_id)
        return chat
    
    def get_messages(self, chat_id: str, limit: int, offset: int) -> list[Message]:
        res = self.db.message_histories.find({"SessionId": chat_id}).sort("_id", -1).skip(offset).limit(limit)

        print(limit, offset)

        messages = []
        for message in res:
            history_json = json.loads(message["History"])
            history = History(**history_json)
            messages.append(Message(
                id=str(message["_id"]),
                session_id=message["SessionId"],
                history=history
            ))

        return messages