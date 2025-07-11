import os
import shutil
import platform
import pathlib
from typing import List, Optional

def get_ghostscript_path() -> str:
    """Get the path to Ghostscript executable."""
    gs_path = shutil.which('gs') or '/opt/homebrew/bin/gs'
    if platform.system() == "Windows":
        gs_path = shutil.which('gswin64c') or shutil.which('gswin32c') or gs_path
    return gs_path

def get_supported_extensions() -> List[str]:
    """Get list of supported file extensions."""
    return ['.docx', '.pdf', '.png', '.jpg', '.jpeg', '.heic', '.xlsx', '.xls', '.pptx', '.ppt']

def is_supported_file(file_path: str) -> bool:
    """Check if file is supported for compression."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in get_supported_extensions()

def validate_file_path(file_path: str) -> bool:
    """Validate file path for security and existence."""
    try:
        path = pathlib.Path(file_path).resolve()
        return path.exists() and path.is_file() and path.is_absolute()
    except (OSError, ValueError, RuntimeError):
        return False

def get_output_path(input_path: str, output_dir: Optional[str] = None, suffix: str = '_compressed') -> str:
    """Generate output path for compressed file."""
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    
    if output_dir:
        return os.path.join(output_dir, f"{name}{suffix}{ext}")
    else:
        return input_path.replace(ext, f"{suffix}{ext}")

def ensure_directory_exists(directory: str) -> bool:
    """Ensure directory exists, create if it doesn't."""
    try:
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False

def get_file_type(path: str) -> Optional[str]:
    """Get file type based on extension."""
    ext = os.path.splitext(path)[1].lower().replace('.', '')
    if ext == 'docx':
        return 'docx'
    elif ext == 'pdf':
        return 'pdf'
    elif ext in ['jpg', 'jpeg', 'png', 'heic']:
        return 'image'
    elif ext in ['xlsx', 'xls']:
        return 'excel'
    elif ext in ['pptx', 'ppt']:
        return 'ppt'
    return None 

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks."""
    # Remove any path separators and dangerous characters
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes."""
    try:
        return os.path.getsize(file_path) / (1024 * 1024)
    except (OSError, FileNotFoundError):
        return 0.0 