"""
Logging configuration for the File Compressor application.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    # Only create logs directory if log_file has a directory part
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create formatter
    formatter = logging.Formatter(log_format, date_format)
        
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
        
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
    
    # Error log handler
    try:
        from config import Config
        error_handler = logging.FileHandler(Config.ERROR_LOG_FILE, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    except Exception as e:
        print(f"Warning: Could not setup error logging: {e}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
    
def log_compression_result(file_path: str, success: bool, output_path: Optional[str] = None, error: Optional[str] = None):
    """
    Log compression result with consistent format.
    
    Args:
        file_path: Input file path
        success: Whether compression was successful
        output_path: Output file path (if successful)
        error: Error message (if failed)
    """
    logger = get_logger(__name__)
    
    if success:
        logger.info(f"Compression successful: {file_path} -> {output_path}")
    else:
        logger.error(f"Compression failed: {file_path} - {error}")
    
def log_file_validation(file_path: str, is_valid: bool, reason: Optional[str] = None):
    """
    Log file validation result.
    
    Args:
        file_path: File path being validated
        is_valid: Whether file is valid
        reason: Reason for validation failure (if any)
    """
    logger = get_logger(__name__)
    
    if is_valid:
        logger.debug(f"File validation passed: {file_path}")
    else:
        logger.warning(f"File validation failed: {file_path} - {reason}")

# Initialize default logging
setup_logging() 