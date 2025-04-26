import sys
from pathlib import Path
import json

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.vectorstore.vector_store import PolicyVectorStore
from src.utils import logger

def main():
    try:
        # Load processed chunks
        with open('data/processed/policy_chunks.json', 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        # Create vector store
        vector_store = PolicyVectorStore()
        vector_store.create_vector_store(chunks)
        
    except Exception as e:
        logger.error(f"Error building vector store: {str(e)}")

if __name__ == "__main__":
    main()