from langchain_core.documents import Document
from .repository import LLMRepository

class TestLLMRepository(LLMRepository):
    """Mock implementation of LLMRepository"""

    def add_document(self, document: Document, chat_id: str) -> None:
        pass

    def messageLLM(self, chat_id: str, prompt: str) -> str:
        return "dummy_response"
    
    def simple_query(self, query: str) -> str:
        return "dummy_query_response"