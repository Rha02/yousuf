from .repository import LLMRepository
from langchain_openai.chat_models import ChatOpenAI

class GPTRepository(LLMRepository):
    """GPT implementation of LLMRepository"""
    def __init__(self, api_key: str) -> None:
        self.llm = ChatOpenAI(api_key=api_key, verbose=True)


    def messageLLM(self, chat_id: str, prompt: str) -> str:
        res = self.llm.invoke(prompt)
        
        return res