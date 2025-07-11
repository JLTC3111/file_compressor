import os, zipfile, tempfile, shutil
from typing import Optional
from PIL import Image

def compress_office_images(filepath: str, media_folder_name: str, quality: int = 60) -> Optional[str]:
    """
    Compress images in Office documents (Excel, PowerPoint).
    
    Args:
        filepath: Path to the Office file
        media_folder_name: Name of the media folder ('xl/media' for Excel, 'ppt/media' for PowerPoint)
        quality: JPEG quality setting (1-100)
        
    Returns:
        Path to compressed file or None if failed
    """
    temp_dir = tempfile.mkdtemp()
    try:
        ext = os.path.splitext(filepath)[1].lower()
        output_path = filepath.replace(ext, f"_compressed{ext}")

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        media_dir = os.path.join(temp_dir, media_folder_name)
        if os.path.exists(media_dir):
            for file in os.listdir(media_dir):
                full_path = os.path.join(media_dir, file)
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    try:
                        img = Image.open(full_path)
                        if file.lower().endswith((".jpg", ".jpeg")):
                            img = img.convert("RGB")
                            img.save(full_path, "JPEG", quality=quality, optimize=True)
                        elif file.lower().endswith(".png"):
                            img.save(full_path, "PNG", optimize=True)
                    except Exception as e:
                        print(f"Failed to compress image in {filepath}: {file} -> {e}")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    abs_path = os.path.join(foldername, filename)
                    rel_path = os.path.relpath(abs_path, temp_dir)
                    new_zip.write(abs_path, rel_path)

        return output_path
        
    except Exception as e:
        print(f"Failed to compress {filepath}: {e}")
        return None
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True) 