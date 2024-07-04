from .repository import LLMRepository
from langchain_openai.chat_models import ChatOpenAI
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage

class GPTRepository(LLMRepository):
    """GPT implementation of LLMRepository"""
    def __init__(self, api_key: str, db_conn: str, db_name: str) -> None:
        self.llm = ChatOpenAI(api_key=api_key, verbose=True)

        self.llm_with_memory = RunnableWithMessageHistory(
            self.llm,
            get_session_history=lambda session_id: MongoDBChatMessageHistory(
                connection_string=db_conn,
                database_name=db_name,
                collection_name="message_histories",
                session_id=session_id
            )
        )

    def messageLLM(self, chat_id: str, prompt: str) -> str:
        config = { "configurable": {"session_id": chat_id}}

        return self.llm_with_memory.invoke(
            [HumanMessage(content=prompt)],
            config=config
        ).content
        

