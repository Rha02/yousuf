from abc import ABC, abstractmethod
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message

class DatabaseRepository(ABC):
    """Abstract class for database repository"""

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User | None:
        pass

    @abstractmethod
    def get_chats(self, user_id: str) -> list[Chat]:
        pass

    @abstractmethod
    def get_chat_by_id(self, chat_id: str) -> Chat | None:
        pass

    @abstractmethod
    def create_chat(self, chat: Chat) -> Chat | None:
        pass

    @abstractmethod
    def get_messages(self, chat_id: str, limit: int, offset: int) -> list[Message]:
        pass