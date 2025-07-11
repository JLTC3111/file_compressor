#!/usr/bin/env python3
"""
Translation Manager Tool

A utility to help manage and update translations for the DOCX/PDF Compressor application.
"""

import json
import os
import sys

def load_translations(lang_code):
    """Load translations for a specific language."""
    translation_file = f"../locales/{lang_code}/translations.json"
    if os.path.exists(translation_file):
        with open(translation_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_translations(lang_code, translations):
    """Save translations for a specific language."""
    translation_file = f"../locales/{lang_code}/translations.json"
    os.makedirs(os.path.dirname(translation_file), exist_ok=True)
    with open(translation_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

def get_missing_keys(base_translations, target_translations):
    """Get keys that are missing from target translations."""
    return set(base_translations.keys()) - set(target_translations.keys())

def get_extra_keys(base_translations, target_translations):
    """Get keys that are extra in target translations."""
    return set(target_translations.keys()) - set(base_translations.keys())

def main():
    """Main function for translation management."""
    print("DOCX/PDF Compressor - Translation Manager")
    print("=" * 50)
    
    # Load base translations (English)
    base_translations = load_translations('en')
    if not base_translations:
        print("Error: Could not load base translations (en)")
        return
    
    print(f"Base translations loaded: {len(base_translations)} keys")
    
    # Check all languages
    languages = ['de', 'fr', 'zh', 'ja', 'vi', 'th']
    
    for lang in languages:
        print(f"\n--- {lang.upper()} ---")
        target_translations = load_translations(lang)
        
        missing_keys = get_missing_keys(base_translations, target_translations)
        extra_keys = get_extra_keys(base_translations, target_translations)
        
        if missing_keys:
            print(f"Missing keys: {len(missing_keys)}")
            for key in sorted(missing_keys):
                print(f"  - {key}")
        
        if extra_keys:
            print(f"Extra keys: {len(extra_keys)}")
            for key in sorted(extra_keys):
                print(f"  - {key}")
        
        if not missing_keys and not extra_keys:
            print("✓ All keys are synchronized")
        
        # Add missing keys with English text as placeholder
        if missing_keys:
            print(f"\nAdding {len(missing_keys)} missing keys...")
            for key in missing_keys:
                target_translations[key] = f"[{base_translations[key]}]"
            save_translations(lang, target_translations)
            print("✓ Updated translation file")

if __name__ == "__main__":
    main() 