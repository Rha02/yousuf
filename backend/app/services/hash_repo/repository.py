from abc import ABC, abstractmethod

class HashFunctionRepository(ABC):
    """Abstract class for hashing functions"""

    @abstractmethod
    def hash(self, value: str) -> str:
        """Take a string value and return its hashed value"""
        pass

    @abstractmethod
    def compare(self, value: str, hashed_value: str) -> bool:
        """Take a string value and its hashed value and return True if they match"""
        pass