import os
from typing import Optional, List
from PIL import Image

try:
    import pillow_heif
except ImportError:
    pillow_heif = None

class ImageCompressor:
    """Handles image compression for various formats."""
    
    def __init__(self, jpeg_quality: int = 60):
        self.jpeg_quality = jpeg_quality
    
    def compress(self, image_path: str, error_list: Optional[List[str]] = None, out_dir: Optional[str] = None) -> Optional[str]:
        """
        Compress image file.
        
        Args:
            image_path: Path to input image file
            error_list: List to append errors to
            out_dir: Output directory
            
        Returns:
            Path to compressed image or None if failed
        """
        try:
            ext = os.path.splitext(image_path)[1].lower()
            base_name = os.path.basename(image_path)
            
            if out_dir:
                if ext in ['.jpg', '.jpeg', '.heic']:
                    output_path = os.path.join(out_dir, base_name.rsplit('.', 1)[0] + '_compressed.jpg')
                else:
                    output_path = os.path.join(out_dir, base_name.rsplit('.', 1)[0] + '_compressed.png')
            else:
                if ext in ['.jpg', '.jpeg', '.heic']:
                    output_path = image_path.rsplit('.', 1)[0] + '_compressed.jpg'
                else:
                    output_path = image_path.rsplit('.', 1)[0] + '_compressed.png'

            if ext in ['.jpg', '.jpeg']:
                img = Image.open(image_path)
                img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=self.jpeg_quality, optimize=True)
            elif ext == '.png':
                img = Image.open(image_path)
                img.save(output_path, 'PNG', optimize=True)
            elif ext == '.heic' and pillow_heif:
                img = Image.open(image_path)
                img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=self.jpeg_quality, optimize=True)
            else:
                raise Exception('Unsupported image format or missing HEIC support')
                
            return output_path
            
        except Exception as e:
            msg = f"Failed to compress image {image_path}: {e}"
            print(msg)
            if error_list is not None:
                error_list.append(msg)
            return None 