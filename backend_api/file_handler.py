"""
Multi-Format File Handler
File: backend_api/file_handler.py

Supports PDF, DOCX, TXT file uploads and extracts text
"""

import PyPDF2
from docx import Document
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def extract_text_from_file(file_obj, filename: str) -> Tuple[str, str]:
    """
    Extract text from various file formats
    
    Args:
        file_obj: File object from request
        filename: Original filename
    
    Returns:
        Tuple: (extracted_text, file_type)
    
    Supported formats:
        - .txt (plain text)
        - .pdf (PDF documents)
        - .docx (Word documents)
    """
    
    try:
        file_extension = filename.lower().split('.')[-1]
        
        # TXT Files
        if file_extension == 'txt':
            logger.info(f"Processing TXT file: {filename}")
            content = file_obj.read().decode('utf-8')
            return content, 'txt'
        
        # PDF Files
        elif file_extension == 'pdf':
            logger.info(f"Processing PDF file: {filename}")
            pdf_reader = PyPDF2.PdfReader(file_obj)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()
                logger.info(f"  Extracted page {page_num + 1}/{len(pdf_reader.pages)}")
            
            logger.info(f"✅ PDF extraction complete: {len(text_content)} characters")
            return text_content, 'pdf'
        
        # DOCX Files
        elif file_extension == 'docx':
            logger.info(f"Processing DOCX file: {filename}")
            doc = Document(file_obj)
            text_content = ""
            
            for para in doc.paragraphs:
                text_content += para.text + "\n"
            
            logger.info(f"✅ DOCX extraction complete: {len(text_content)} characters")
            return text_content, 'docx'
        
        # Unsupported format
        else:
            logger.error(f"❌ Unsupported file format: {file_extension}")
            raise ValueError(f"Unsupported file format: .{file_extension}\nSupported: .txt, .pdf, .docx")
    
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise


def validate_file(file_obj, filename: str, max_size_mb: int = 16) -> bool:
    """
    Validate uploaded file
    
    Args:
        file_obj: File object
        filename: Filename
        max_size_mb: Maximum file size in MB
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If file is invalid
    """
    
    # Check filename not empty
    if not filename or filename == '':
        raise ValueError("Filename cannot be empty")
    
    # Check file extension
    valid_extensions = ['.txt', '.pdf', '.docx']
    file_ext = '.' + filename.lower().split('.')[-1]
    
    if file_ext not in valid_extensions:
        raise ValueError(f"Invalid file format. Supported: {', '.join(valid_extensions)}")
    
    # Check file size
    file_obj.seek(0, 2)  # Seek to end
    file_size = file_obj.tell()
    file_obj.seek(0)  # Reset to start
    
    file_size_mb = file_size / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        raise ValueError(f"File size ({file_size_mb:.2f}MB) exceeds maximum ({max_size_mb}MB)")
    
    # Check not empty
    if file_size == 0:
        raise ValueError("File is empty")
    
    logger.info(f"✅ File validation passed: {filename} ({file_size_mb:.2f}MB)")
    return True


def get_file_type_from_name(filename: str) -> str:
    """
    Get file type from filename
    
    Args:
        filename: Original filename
    
    Returns:
        str: File type (txt, pdf, docx)
    """
    return filename.lower().split('.')[-1]