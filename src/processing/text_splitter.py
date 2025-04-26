from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.helpers import logger, timer_decorator

class PolicyDocumentSplitter:
    """Split insurance policy documents while maintaining context."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def _create_chunk_metadata(self, 
                             section: str, 
                             doc_info: Dict[str, Any], 
                             page: int) -> Dict[str, Any]:
        """Create metadata for each chunk."""
        return {
            'category': doc_info['category'],
            'company': doc_info['company'],
            'source': doc_info['source'],
            'section': section,
            'page': page
        }

    @timer_decorator
    def split_documents(self, processed_docs: Dict[str, List[Dict]]) -> List[Dict]:
        """Split documents into chunks while preserving section information."""
        all_chunks = []
        
        for category, docs in processed_docs.items():
            for doc in docs:
                try:
                    # Process each section separately
                    for section, content_list in doc['sections'].items():
                        for content_item in content_list:
                            chunks = self.text_splitter.split_text(content_item['content'])
                            
                            for chunk in chunks:
                                if len(chunk.strip()) > 50:  # Minimum chunk size
                                    chunk_doc = {
                                        'content': chunk,
                                        'metadata': self._create_chunk_metadata(
                                            section=section,
                                            doc_info=doc,
                                            page=content_item['page']
                                        )
                                    }
                                    all_chunks.append(chunk_doc)
                
                except Exception as e:
                    logger.error(f"Error splitting document {doc['filename']}: {str(e)}")
                    continue

        logger.info(f"Created {len(all_chunks)} chunks from documents")
        return all_chunks