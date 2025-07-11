#!/usr/bin/env python3
"""
Build script for File Compressor application.
Automates the packaging process for different platforms.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec', '*.log']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            if file_path.name != 'FileCompressor.spec':
                file_path.unlink()
                print(f"✓ Removed {file_path}")

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ('Pillow', 'PIL'),
        ('tkinterdnd2', 'tkinterdnd2'), 
        ('docx2pdf', 'docx2pdf'),
        ('pillow-heif', 'pillow_heif'),
        ('pyinstaller', 'PyInstaller')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def build_application():
    """Build the application using PyInstaller."""
    print("\n🔨 Building application...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        return build_macos()
    elif system == "windows":
        return build_windows()
    elif system == "linux":
        return build_linux()
    else:
        print(f"❌ Unsupported platform: {system}")
        return False

def build_macos():
    """Build for macOS."""
    print("📱 Building for macOS...")
    
    # Build with PyInstaller
    command = "pyinstaller FileCompressor.spec --clean"
    if not run_command(command, "Building macOS application"):
        return False
    
    # Create DMG if hdiutil is available
    if shutil.which('hdiutil'):
        print("\n📦 Creating DMG package...")
        dmg_command = (
            'hdiutil create -volname "File Compressor" -srcfolder dist/ '
            '-ov -format UDZO "File Compressor.dmg"'
        )
        run_command(dmg_command, "Creating DMG package")
    
    return True

def build_windows():
    """Build for Windows."""
    print("🪟 Building for Windows...")
    
    # Build with PyInstaller
    command = "pyinstaller FileCompressor.spec --clean"
    if not run_command(command, "Building Windows application"):
        return False
    
    # Create installer if NSIS is available
    if shutil.which('makensis'):
        print("\n📦 Creating Windows installer...")
        nsis_command = 'makensis installer.nsi'
        run_command(nsis_command, "Creating Windows installer")
    
    return True

def build_linux():
    """Build for Linux."""
    print("🐧 Building for Linux...")
    
    # Build with PyInstaller
    command = "pyinstaller FileCompressor.spec --clean"
    if not run_command(command, "Building Linux application"):
        return False
    
    # Create AppImage if appimagetool is available
    if shutil.which('appimagetool'):
        print("\n📦 Creating AppImage...")
        appimage_command = 'appimagetool dist/FileCompressor FileCompressor.AppImage'
        run_command(appimage_command, "Creating AppImage")
    
    return True

def main():
    """Main build process."""
    print("🚀 File Compressor Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this script from the source_compressor directory.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Build application
    if not build_application():
        print("❌ Build failed!")
        sys.exit(1)
    
    print("\n🎉 Build completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test the application in the dist/ directory")
    print("2. Distribute the built application")
    print("3. Consider code signing for production releases")

if __name__ == "__main__":
    main() 