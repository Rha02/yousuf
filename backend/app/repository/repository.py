from abc import ABC, abstractmethod
from app.models.user import User

class DatabaseRepository(ABC):
    """Abstract class for database repository"""

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass