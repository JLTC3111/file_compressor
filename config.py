"""
Configuration settings for the File Compressor application.
"""

import os
from typing import List

class Config:
    """Application configuration constants."""
    
    # Application info
    APP_NAME = "FileCompressor"
    APP_VERSION = "1.1.5"
    
    # Default settings
    DEFAULT_JPEG_QUALITY = 60
    DEFAULT_PDF_QUALITY = '/screen'
    DEFAULT_AUTO_OVERWRITE = True
    DEFAULT_SHOW_PROGRESS = True
    DEFAULT_PLAY_SOUND = True
    
    # Supported file formats
    SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.heic']
    SUPPORTED_OFFICE_FORMATS = ['.docx', '.xlsx', '.xls', '.pptx', '.ppt']
    SUPPORTED_PDF_FORMATS = ['.pdf']
    
    # PDF quality options
    PDF_QUALITY_OPTIONS = ['/screen', '/ebook', '/printer', '/prepress']
    
    # File size limits (in bytes)
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    
    # Temporary directory
    TEMP_DIR = os.path.join(os.path.expanduser("~"), ".file_compressor_temp")
    
    # Logging
    LOG_FILE = os.path.join(os.path.expanduser("~"), "filecompressor.log")
    ERROR_LOG_FILE = os.path.join(os.path.expanduser("~"), "filecompressor_error.log")
    
    # GUI settings
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 380
    SETTINGS_DIALOG_WIDTH = 400
    SETTINGS_DIALOG_HEIGHT = 500
    
    # Compression settings
    COMPRESSION_SUFFIX = "_compressed"
    
    @classmethod
    def get_all_supported_extensions(cls) -> List[str]:
        """Get all supported file extensions."""
        return (cls.SUPPORTED_IMAGE_FORMATS + 
                cls.SUPPORTED_OFFICE_FORMATS + 
                cls.SUPPORTED_PDF_FORMATS)
    
    @classmethod
    def get_file_type(cls, file_path: str) -> str:
        """Get file type based on extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in cls.SUPPORTED_IMAGE_FORMATS:
            return 'image'
        elif ext in cls.SUPPORTED_OFFICE_FORMATS:
            if ext == '.docx':
                return 'docx'
            elif ext in ['.xlsx', '.xls']:
                return 'excel'
            elif ext in ['.pptx', '.ppt']:
                return 'ppt'
        elif ext in cls.SUPPORTED_PDF_FORMATS:
            return 'pdf'
        
        return 'unknown'
    
    @classmethod
    def ensure_temp_dir(cls):
        """Ensure temporary directory exists."""
        if not os.path.exists(cls.TEMP_DIR):
            os.makedirs(cls.TEMP_DIR)
    
    @classmethod
    def cleanup_temp_dir(cls):
        """Clean up temporary directory."""
        import shutil
        if os.path.exists(cls.TEMP_DIR):
            shutil.rmtree(cls.TEMP_DIR, ignore_errors=True) 