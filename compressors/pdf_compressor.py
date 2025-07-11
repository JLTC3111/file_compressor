import os
import subprocess
from typing import Optional, List
from utils.file_utils import get_ghostscript_path

class PDFCompressor:
    """Handles PDF compression using Ghostscript."""
    
    def __init__(self):
        self.gs_path = get_ghostscript_path()
    
    def compress(self, pdf_path: str, error_list: Optional[List[str]] = None, out_dir: Optional[str] = None, quality: str = '/screen') -> Optional[str]:
        """
        Compress PDF using Ghostscript.
        
        Args:
            pdf_path: Path to input PDF file
            error_list: List to append errors to
            out_dir: Output directory
            quality: PDF quality setting ('/screen', '/ebook', '/printer', '/prepress')
            
        Returns:
            Path to compressed PDF or None if failed
        """
        try:
            base_name = os.path.basename(pdf_path).replace('.pdf', '_compressed.pdf')
            if out_dir:
                output_path = os.path.join(out_dir, base_name)
            else:
                output_path = pdf_path.replace('.pdf', '_compressed.pdf')
                
            result = subprocess.run([
                self.gs_path,
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={quality}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={output_path}',
                pdf_path
            ], check=True, capture_output=True, text=True)
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            msg = f"Failed to compress PDF {pdf_path} with Ghostscript: {e}"
            if e.stderr:
                msg += f"\nGhostscript error: {e.stderr}"
            print(msg)
            if error_list is not None:
                error_list.append(msg)
            return None
        except Exception as e:
            msg = f"Failed to compress PDF {pdf_path}: {e}"
            print(msg)
            if error_list is not None:
                error_list.append(msg)
            return None 