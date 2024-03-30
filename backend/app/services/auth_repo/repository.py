from abc import ABC, abstractmethod

class AuthTokenRepository(ABC):
    """Abstract class for authentication token service"""

    @abstractmethod
    def create_token(self, payload: dict) -> str:
        pass

    @abstractmethod
    def parse_token(self, token: str) -> dict:
        pass