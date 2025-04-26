import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.utils.helpers import logger, timer_decorator, validate_file_type
from src.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

class InsurancePolicyProcessor:
    """Process insurance policy documents with specific handling for policy wordings."""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        self.processed_data_dir = PROCESSED_DATA_DIR
        # Define sections commonly found in policy documents
        self.policy_sections = {
            'definitions': ['definitions', 'defined terms', 'meaning of words'],
            'coverage': ['what is covered', 'benefits', 'coverage', 'scope of cover'],
            'exclusions': ['what is not covered', 'exclusions', 'exceptions'],
            'conditions': ['terms and conditions', 'general conditions'],
            'claims': ['claims', 'claim procedure', 'how to claim']
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        # Remove multiple spaces and normalize newlines
        cleaned = ' '.join(text.split())
        # Remove common PDF artifacts
        cleaned = cleaned.replace('•', '')
        return cleaned

    def _identify_section(self, text: str) -> str:
        """Identify which section of the policy document this text belongs to."""
        text_lower = text.lower()
        for section, keywords in self.policy_sections.items():
            if any(keyword in text_lower for keyword in keywords):
                return section
        return 'general'

    @timer_decorator
    def extract_text_from_pdf(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract text from PDF with section identification."""
        if not validate_file_type(str(file_path)):
            logger.error(f"Invalid file type: {file_path}")
            return None

        try:
            sections_data = {
                'definitions': [],
                'coverage': [],
                'exclusions': [],
                'conditions': [],
                'claims': [],
                'general': []
            }
            
            with pdfplumber.open(file_path) as pdf:
                current_section = 'general'
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        cleaned_text = self._clean_text(text)
                        # Try to identify section from the text
                        detected_section = self._identify_section(cleaned_text)
                        if detected_section != 'general':
                            current_section = detected_section
                        
                        sections_data[current_section].append({
                            'page': page_num,
                            'content': cleaned_text
                        })
            
            return sections_data

        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    @timer_decorator
    def process_documents(self) -> Dict[str, List[Dict]]:
        """Process all insurance policy documents."""
        processed_docs = {
            'auto': [],
            'health': []
        }

        for category in processed_docs.keys():
            category_path = self.raw_data_dir / category
            if not category_path.exists():
                logger.warning(f"Category directory not found: {category_path}")
                continue

            for company_dir in category_path.iterdir():
                if company_dir.is_dir():
                    company = company_dir.name
                    for file_path in company_dir.glob('*.pdf'):
                        sections_data = self.extract_text_from_pdf(file_path)
                        if sections_data:
                            doc_info = {
                                'company': company,
                                'category': category,
                                'filename': file_path.name,
                                'sections': sections_data,
                                'source': str(file_path)
                            }
                            processed_docs[category].append(doc_info)
                            logger.info(f"Processed {file_path}")

        return processed_docs