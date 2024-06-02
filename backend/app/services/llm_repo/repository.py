from abc import ABC, abstractmethod

class LLMRepository(ABC):
    """Abstract class for LLM"""

    @abstractmethod
    def messageLLM(self, chat_id: str, prompt: str) -> str:
        """Take a string message from a user and return a string message from the LLM"""
        pass

