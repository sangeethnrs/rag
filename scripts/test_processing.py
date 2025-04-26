import sys
from pathlib import Path
import json
from typing import List, Dict  # Add this import for type hints

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.processing import InsurancePolicyProcessor, PolicyDocumentSplitter
from src.utils import logger

def save_processed_data(chunks: List[Dict], output_file: str) -> None:
    """Save processed chunks to a JSON file."""
    output_path = Path(output_file)
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved processed data to {output_file}")

def main() -> None:
    try:
        # Initialize processors
        doc_processor = InsurancePolicyProcessor()
        doc_splitter = PolicyDocumentSplitter()

        # Process documents
        logger.info("Starting document processing...")
        processed_docs = doc_processor.process_documents()

        # Count processed documents
        total_docs = sum(len(docs) for docs in processed_docs.values())
        logger.info(f"Processed {total_docs} documents")

        # Split documents
        logger.info("Splitting documents into chunks...")
        chunks = doc_splitter.split_documents(processed_docs)
        
        # Save processed data
        save_processed_data(chunks, 'data/processed/policy_chunks.json')

        # Print statistics
        sections_count = {}
        for chunk in chunks:
            section = chunk['metadata']['section']
            sections_count[section] = sections_count.get(section, 0) + 1

        logger.info("Chunks by section:")
        for section, count in sections_count.items():
            logger.info(f"- {section}: {count} chunks")

    except Exception as e:
        logger.error(f"Error in processing: {str(e)}")

if __name__ == "__main__":
    main()