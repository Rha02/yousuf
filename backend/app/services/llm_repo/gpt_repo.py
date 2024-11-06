from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .repository import LLMRepository
from langchain_openai.chat_models import ChatOpenAI
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage

class GPTRepository(LLMRepository):
    """GPT implementation of LLMRepository"""
    def __init__(self, api_key: str, db_conn: str, db_name: str) -> None:
        self.llm = ChatOpenAI(api_key=api_key, verbose=True)

        embeddingFunc = OpenAIEmbeddings(api_key=api_key, model="text-embedding-3-small")

        self.vectorstore = Chroma(
            collection_name="vectorstore",
            embedding_function=embeddingFunc,
            persist_directory="./chromadb"
        )

        self.fine_tuned_llm = lambda llm: RunnableWithMessageHistory(
            runnable=llm,
            get_session_history=lambda session_id: MongoDBChatMessageHistory(
                connection_string=db_conn,
                database_name=db_name,
                collection_name="message_histories",
                session_id=session_id
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
    
    def add_document(self, document: Document, chat_id: str) -> None:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750, chunk_overlap=150, add_start_index=True
        )
        all_splits = text_splitter.split_documents([document])

        for split_text in all_splits:
            split_text.metadata["session_id"] = chat_id
        
        self.vectorstore.add_documents(all_splits)

    def messageLLM(self, chat_id: str, prompt: str) -> str:
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "filter": {"session_id": chat_id}}
        )

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, contextualize_q_prompt
        )

        ### Answer question ###
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question if possible. If the context is not useful, "
            "you can ignore it. If the context is useful, you can use it "
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        config = { "configurable": {"session_id": chat_id}}

        return self.fine_tuned_llm(rag_chain).invoke(
           {"input": prompt},
            config=config
        )["answer"]
    
    def simple_query(self, query: str) -> str:
        return self.llm.invoke(query).content
