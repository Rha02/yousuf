from langchain_core.documents import Document
from .repository import LLMRepository

class TestLLMRepository(LLMRepository):
    """Mock implementation of LLMRepository"""

    def add_document(self, document: Document, chat_id: str) -> None:
        pass

    def messageLLM(self, chat_id: str, prompt: str) -> str:
        return "dummy_response"
    
    def simple_query(self, query: str) -> str:
        errorQuery = "Create a short chat title based on the following prompt:\nsimple_query_error"

        if query == errorQuery:
            return "error"

        return "dummy_query_response"