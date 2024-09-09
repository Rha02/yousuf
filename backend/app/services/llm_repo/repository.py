from abc import ABC, abstractmethod
from langchain_core.documents import Document

class LLMRepository(ABC):
    """Abstract class for LLM"""

    @abstractmethod
    def messageLLM(self, chat_id: str, prompt: str) -> str:
        """Take a string message from a user and return a string message from the LLM"""
        pass

    @abstractmethod
    def add_document(self, document: Document, chat_id: str) -> None:
        """Add a document to the LLM"""
        pass

