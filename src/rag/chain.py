from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from src.config.settings import OPENAI_API_KEY, CHAT_MODEL
from src.utils.helpers import logger, timer_decorator

class InsuranceChatbot:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=0,
            model_name=CHAT_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = self._create_chain()