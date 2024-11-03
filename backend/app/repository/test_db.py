from app.models.chat import Chat
from app.models.message import History, Message, MessageData
from app.models.user import User
from .repository import DatabaseRepository

class TestDBRepository(DatabaseRepository):
    """Mock class for database repository"""
    
    def get_user_by_email(self, email: str) -> User | None:
        if email == "error":
            return None
        
        return User(
            id="1",
            first_name="John",
            last_name="Doe",
            email=email,
            password="hashed_password"
        )

    
    def get_user_by_id(self, user_id: str) -> User | None:
        if user_id == "error":
            return None
        
        return User(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@test.loc",
            password="hashed_password"
        )

    
    def create_user(self, user: User) -> User | None:
        if user.email == "error":
            return None
        
        return User(
            id="1",
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )

    
    def get_chats(self, user_id: str) -> list[Chat]:
        return [
            Chat(
                id="1",
                title="Chat 1",
                user_id=user_id
            ),
            Chat(
                id="2",
                title="Chat 2",
                user_id=user_id
            )
        ]

    
    def get_chat_by_id(self, chat_id: str) -> Chat | None:
        if chat_id == "error":
            return None
        
        return Chat(
            id=chat_id,
            title="Chat",
            user_id="1"
        )

    
    def create_chat(self, chat: Chat) -> Chat | None:
        if chat.title == "error":
            return None
        
        return Chat(
            id="1",
            title=chat.title,
            user_id=chat.user_id
        )

    
    def get_messages(self, chat_id: str, limit: int, offset: int) -> list[Message]:
        if chat_id == "error":
            return []
        
        return [
            Message(
                id="1",
                session_id=chat_id,
                history=History(
                    type="Human",
                    data=MessageData(
                        content="Human message"
                    )
                )
            ),
            Message(
                id="2",
                session_id=chat_id,
                history=History(
                    type="Bot",
                    data=MessageData(
                        content="Bot message"
                    )
                )
            )
        ]