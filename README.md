# File Compressor by LD✨

A powerful, multi-language GUI application for compressing DOCX, PDF, and image files with drag-and-drop support.

## 🌟 Features

- **Multi-format Support**: DOCX, PDF, PNG, JPG, JPEG, HEIC, Excel, PowerPoint
- **Internationalization**: 7 languages (English, German, French, Chinese, Japanese, Vietnamese, Thai)
- **Drag & Drop**: Easy file processing with drag-and-drop interface
- **Progress Tracking**: Real-time progress updates during compression
- **Settings Management**: Persistent settings with quality controls
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Performance Monitoring**: Built-in performance tracking and system resource monitoring

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- macOS 10.14+, Windows 10+, or Linux
- At least 100MB free memory
- At least 1GB free disk space

### Dependencies
- Pillow (PIL) - Image processing
- tkinterdnd2 - Drag and drop support
- docx2pdf - DOCX to PDF conversion
- pillow-heif - HEIC image support
- psutil - System monitoring
- typing-extensions - Type hints support

## 🚀 Installation

### Option 1: From Source (Recommended)

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd file_compressor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Option 2: Using PyInstaller (Standalone Executable)

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the application**
```bash
python build.py
```

3. **Find the executable**
   - macOS: `dist/FileCompressor.app`
   - Windows: `dist/FileCompressor.exe`
   - Linux: `dist/FileCompressor`

## 🎯 Usage

### Basic Usage

1. **Launch the application**
   - Double-click the executable or run `python main.py`

2. **Select files**
   - Click "Select DOCX/PDF Files" button, or
   - Drag and drop files directly onto the application window

3. **Configure settings** (optional)
   - Click "Settings" in the menu bar
   - Adjust JPEG quality (1-100)
   - Set PDF quality (/screen, /ebook, /printer, /prepress)
   - Configure auto-overwrite and progress display

4. **Start compression**
   - Files will be processed automatically
   - Progress is shown in real-time
   - Compressed files are saved with "_compressed" suffix

### Advanced Features

#### Language Selection
- Click "Language" in the menu bar
- Choose from 7 supported languages
- Language preference is saved automatically

#### Output Directory
- Click "Select Output Directory" to specify custom output location
- If not specified, compressed files are saved in the same directory as originals

#### Batch Processing
- Select multiple files at once
- Drag entire folders for recursive processing
- All supported files in folders are automatically detected

## 🔧 Configuration

### Settings File Location
- **macOS**: `~/Library/Application Support/FileCompressor/settings.json`
- **Windows**: `%APPDATA%\FileCompressor\settings.json`
- **Linux**: `~/.config/FileCompressor/settings.json`

### Available Settings
```json
{
  "jpeg_quality": 60,
  "pdf_quality": "/screen",
  "auto_overwrite": true,
  "show_progress": true,
  "play_sound": true,
  "output_directory": null,
  "language": "en"
}
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_compressors.py
```

Tests cover:
- File utilities and validation
- All compressor classes
- Internationalization
- Settings management
- Error handling

## 🛠️ Development

### Project Structure
```
source_compressor/
├── main.py                 # Application entry point
├── config.py              # Configuration constants
├── build.py               # Build script for PyInstaller
├── test_compressors.py    # Test suite
├── compressors/           # Compression modules
│   ├── docx_compressor.py
│   ├── pdf_compressor.py
│   ├── image_compressor.py
│   └── office_generic.py
├── gui/                   # GUI components
│   ├── app_window.py
│   └── settings_dialog.py
├── utils/                 # Utility modules
│   ├── file_utils.py
│   ├── i18n.py
│   ├── logger.py
│   ├── performance.py
│   └── settings_manager.py
└── locales/              # Translation files
    ├── en/
    ├── de/
    ├── fr/
    ├── zh/
    ├── ja/
    ├── vi/
    └── th/
```

### Adding New Features

1. **New File Format Support**
   - Add format to `config.py` supported formats
   - Create compressor in `compressors/` directory
   - Update `utils/file_utils.py` file type detection
   - Add tests in `test_compressors.py`

2. **New Language Support**
   - Create new directory in `locales/`
   - Add `translations.json` with all required keys
   - Update `utils/i18n.py` available languages

3. **Performance Improvements**
   - Use `@monitor_performance` decorator
   - Check system resources with `check_system_resources()`
   - Monitor memory usage with `get_system_info()`

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Add comprehensive docstrings
- Use logging instead of print statements
- Write unit tests for new features

## 🐛 Troubleshooting

### Common Issues

1. **"Ghostscript not found" error**
   - Install Ghostscript: `brew install ghostscript` (macOS)
   - Or download from: https://ghostscript.com/

2. **"PIL/Pillow import error"**
   - Reinstall Pillow: `pip install --upgrade Pillow`

3. **"tkinterdnd2 import error"**
   - Install tkinterdnd2: `pip install tkinterdnd2`

4. **Permission errors**
   - Check file permissions
   - Run as administrator (Windows)
   - Use sudo (Linux/macOS) if needed

### Log Files
- Application log: `app.log`
- Error log: `error_log.txt`
- Check these files for detailed error information

### Performance Issues
- Monitor system resources with built-in performance tools
- Check available disk space
- Ensure sufficient memory (100MB+ recommended)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Create an issue with detailed information
4. Include system information and error messages

## 🎉 Acknowledgments

- Pillow team for image processing capabilities
- Ghostscript team for PDF compression
- tkinterdnd2 developers for drag-and-drop functionality
- All contributors and translators

---

**Made with ❤️ by LD✨** 