import logging
import sys
import time
from functools import wraps
from pathlib import Path

# Configure logging with UTF-8 encoding
def setup_logger():
    logger = logging.getLogger('src.utils.helpers')
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Simple formatter without emojis
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} took {execution_time:.2f} seconds to execute")
        return result
    return wrapper

# File validation functions
def validate_file_type(file_path: str) -> bool:
    """Validate if file type is supported."""
    allowed_extensions = {'.pdf', '.txt', '.docx'}
    return Path(file_path).suffix.lower() in allowed_extensions