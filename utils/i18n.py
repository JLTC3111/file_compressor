import json
import os
import locale
from typing import Dict, Any

class I18nManager:
    """Internationalization manager for the application."""
    
    def __init__(self, default_language='en'):
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        self.locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')
        self.load_translations()
    
    def get_system_language(self) -> str:
        """Get the system's default language."""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # Extract language code (e.g., 'en_US' -> 'en')
                return system_locale.split('_')[0]
        except:
            pass
        return self.default_language
    
    def load_translations(self):
        """Load all translation files."""
        if not os.path.exists(self.locales_dir):
            return
        
        for lang_dir in os.listdir(self.locales_dir):
            lang_path = os.path.join(self.locales_dir, lang_dir)
            if os.path.isdir(lang_path):
                translation_file = os.path.join(lang_path, 'translations.json')
                if os.path.exists(translation_file):
                    try:
                        with open(translation_file, 'r', encoding='utf-8') as f:
                            self.translations[lang_dir] = json.load(f)
                    except Exception as e:
                        print(f"Error loading translations for {lang_dir}: {e}")
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Language '{language}' not found, using default")
            self.current_language = self.default_language
    
    def get_text(self, key: str, **kwargs) -> str:
        """Get translated text for a given key."""
        try:
            # Try current language first
            if self.current_language in self.translations:
                text = self.translations[self.current_language].get(key, key)
            else:
                # Fallback to default language
                text = self.translations.get(self.default_language, {}).get(key, key)
            
            # Replace placeholders if any
            if kwargs:
                text = text.format(**kwargs)
            
            return text
        except Exception:
            return key
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages with their display names."""
        return {
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'zh': '中文',
            'ja': '日本語',
            'vi': 'Tiếng Việt',
            'th': 'ไทย'
        }
    
    def get_current_language_name(self) -> str:
        """Get the display name of the current language."""
        languages = self.get_available_languages()
        return languages.get(self.current_language, 'English')

# Global instance
i18n = I18nManager() 