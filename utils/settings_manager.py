"""
Settings manager for persistent application configuration.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Determine user-writable settings path (macOS convention)
def get_default_settings_path() -> str:
    base_dir = os.path.expanduser('~/Library/Application Support/FileCompressor')
    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir, exist_ok=True)
            logger.info(f"Created settings directory: {base_dir}")
        except Exception as e:
            logger.error(f"Could not create settings directory: {e}")
    return os.path.join(base_dir, 'settings.json')

class SettingsManager:
    """Manages persistent application settings."""
    
    def __init__(self, config_file: Optional[str] = None):
        try:
            if config_file is None:
                config_file = get_default_settings_path()
            self.config_file = config_file
            logger.info(f"SettingsManager using config file: {os.path.abspath(self.config_file)}")
            self.settings = self.load_settings()
        except Exception as e:
            logger.error(f"Exception in SettingsManager: {e}")
            self.settings = self.get_default_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults."""
        try:
            if os.path.exists(self.config_file):
                logger.info(f"Loading settings from: {os.path.abspath(self.config_file)}")
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Exception loading settings: {e}")
        # Return default settings if anything fails
        return self.get_default_settings()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file."""
        try:
            logger.info(f"Saving settings to: {os.path.abspath(self.config_file)}")
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            logger.error(f"Error saving settings to {os.path.abspath(self.config_file)}: {e}")
            return False
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default application settings."""
        return {
            'jpeg_quality': Config.DEFAULT_JPEG_QUALITY,
            'pdf_quality': Config.DEFAULT_PDF_QUALITY,
            'auto_overwrite': Config.DEFAULT_AUTO_OVERWRITE,
            'show_progress': Config.DEFAULT_SHOW_PROGRESS,
            'play_sound': Config.DEFAULT_PLAY_SOUND,
            'output_directory': None,
            'language': 'en'
        }
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting value."""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Set a specific setting value."""
        self.settings[key] = value
        return self.save_settings(self.settings)
    
    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Update multiple settings at once."""
        self.settings.update(new_settings)
        return self.save_settings(self.settings)
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults."""
        self.settings = self.get_default_settings()
        return self.save_settings(self.settings)
    
    def get_jpeg_quality(self) -> int:
        """Get JPEG quality setting."""
        return self.get_setting('jpeg_quality', Config.DEFAULT_JPEG_QUALITY)
    
    def get_pdf_quality(self) -> str:
        """Get PDF quality setting."""
        return self.get_setting('pdf_quality', Config.DEFAULT_PDF_QUALITY)
    
    def get_auto_overwrite(self) -> bool:
        """Get auto overwrite setting."""
        return self.get_setting('auto_overwrite', Config.DEFAULT_AUTO_OVERWRITE)
    
    def get_show_progress(self) -> bool:
        """Get show progress setting."""
        return self.get_setting('show_progress', Config.DEFAULT_SHOW_PROGRESS)
    
    def get_play_sound(self) -> bool:
        """Get play sound setting."""
        return self.get_setting('play_sound', Config.DEFAULT_PLAY_SOUND)
    
    def get_output_directory(self) -> Optional[str]:
        """Get output directory setting."""
        return self.get_setting('output_directory')
    
    def get_language(self) -> str:
        """Get language setting."""
        return self.get_setting('language', 'en')

# Global settings manager instance
settings_manager = SettingsManager() 