import os
import zipfile
import tempfile
import shutil
from typing import Optional, List
from PIL import Image

class DOCXCompressor:
    """Handles DOCX compression by optimizing embedded images."""
    
    def __init__(self, jpeg_quality: int = 60):
        self.jpeg_quality = jpeg_quality
    
    def compress(self, docx_path: str, error_list: Optional[List[str]] = None, out_dir: Optional[str] = None) -> Optional[str]:
        """
        Compress DOCX file by optimizing embedded images.
        
        Args:
            docx_path: Path to input DOCX file
            error_list: List to append errors to
            out_dir: Output directory
            
        Returns:
            Path to compressed DOCX or None if failed
        """
        temp_dir = tempfile.mkdtemp()
        base_name = os.path.basename(docx_path).replace(".docx", "_compressed.docx")
        
        if out_dir:
            output_path = os.path.join(out_dir, base_name)
        else:
            output_path = docx_path.replace(".docx", "_compressed.docx")

        try:
            # Step 1: Unzip .docx (it's just a zip file)
            with zipfile.ZipFile(docx_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Step 2: Compress images in the media folder
            media_path = os.path.join(temp_dir, "word", "media")
            if os.path.exists(media_path):
                for file in os.listdir(media_path):
                    full_path = os.path.join(media_path, file)
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        try:
                            img = Image.open(full_path)
                            if file.lower().endswith((".jpg", ".jpeg")):
                                img = img.convert("RGB")
                                img.save(full_path, optimize=True, quality=self.jpeg_quality)
                            elif file.lower().endswith(".png"):
                                img.save(full_path, optimize=True)
                        except Exception as e:
                            msg = f"Failed to compress {file}: {e}"
                            print(msg)
                            if error_list is not None:
                                error_list.append(msg)

            # Step 3: Repackage the .docx
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_zip:
                for foldername, subfolders, filenames in os.walk(temp_dir):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, temp_dir)
                        docx_zip.write(file_path, arcname)

            return output_path
            
        except Exception as e:
            msg = f"Failed to compress DOCX {docx_path}: {e}"
            print(msg)
            if error_list is not None:
                error_list.append(msg)
            return None
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir) 