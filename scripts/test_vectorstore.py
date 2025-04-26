import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.vectorstore.vector_store import PolicyVectorStore
from src.utils.helpers import logger

def test_vector_store():
    try:
        # Initialize vector store
        vector_store = PolicyVectorStore()
        
        # Load the saved vector store
        vector_store.load_vector_store()
        
        # Test queries
        test_queries = [
            "What are the exclusions in car insurance?",
            "How do I make a claim?",
            "What is covered under health insurance?"
        ]
        
        # Run tests
        logger.info("=== Vector Store Test Results ===")
        for query in test_queries:
            logger.info(f"\nQuery: {query}")
            results = vector_store.similarity_search(query, k=2)
            
            for idx, (content, score) in enumerate(results, 1):
                logger.info(f"\nResult {idx}:")
                logger.info(f"Similarity Score: {score:.4f}")
                logger.info(f"Content Preview: {content[:200]}...")
                logger.info("-" * 80)
            
    except Exception as e:
        logger.error(f"Error testing vector store: {str(e)}")

if __name__ == "__main__":
    test_vector_store()