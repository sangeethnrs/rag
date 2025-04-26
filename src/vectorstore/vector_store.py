from typing import List, Dict, Tuple
import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.config.settings import (
    OPENAI_API_KEY,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL,
)
from src.utils.helpers import logger, timer_decorator

class PolicyVectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        self.vector_store = None
        
    def load_vector_store(self) -> None:
        """Load existing vector store from disk."""
        try:
            store_path = str(VECTOR_STORE_PATH)
            if not os.path.exists(store_path):
                raise FileNotFoundError(f"Vector store not found at {store_path}")
                
            self.vector_store = FAISS.load_local(
                store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
            
    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """Perform similarity search on loaded vector store."""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized. Call load_vector_store first.")
                
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return [(doc.page_content, score) for doc, score in results]
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise