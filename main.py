#!/usr/bin/env python3
"""
File Compressor - Main Entry Point

A native application for compressing documents, images and other files with drag-and-drop support.
"""

import sys
import os
import traceback
import logging
from typing import Optional

# Path setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logging
from gui.app_window import CompressorApp

DEBUG_LOG_PATH = "/tmp/fc_debug.log"
CRASH_LOG_PATH = "/tmp/fc_crash_gui.log"

def write_debug_log():
    """Write basic debug info to temp log."""
    try:
        with open(DEBUG_LOG_PATH, "w") as log:
            log.write("✅ File Compressor launched from GUI!\n")
            log.write(f"🧠 Python version: {sys.version}\n")
            log.write(f"📁 Working dir: {os.getcwd()}\n")
            log.write(f"📄 __file__: {__file__}\n")
    except Exception as e:
        # If we can't even write to /tmp, then this is truly cursed
        print(f"❌ Failed to write debug log: {e}")

def write_crash_log(e: Exception):
    """Write crash traceback to temp file for GUI debugging."""
    try:
        with open(CRASH_LOG_PATH, "w") as f:
            f.write("💥 App crashed!\n")
            f.write(f"Error: {e}\n")
            f.write("Traceback:\n")
            f.write(traceback.format_exc())
    except Exception as log_e:
        print(f"❌ Failed to write crash log: {log_e}")

def main() -> None:
    """Main launcher for the File Compressor app."""
    write_debug_log()
    
    try:
        # Setup real logging
        from config import Config
        logger = setup_logging(log_level="INFO", log_file=Config.LOG_FILE)
        logger.info("🚀 Starting File Compressor application")

        app = CompressorApp()
        logger.info("🎨 GUI created, starting mainloop")
        app.run()
        logger.info("✅ GUI exited normally")
        
    except KeyboardInterrupt:
        print("⚠️ Application interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error starting application: {e}")
        traceback.print_exc()

        # Write crash info to file
        write_crash_log(e)

        # Also write to main crash log file
        try:
            crash_log_path = os.path.join(os.path.expanduser("~"), "filecompressor_crash.log")
            with open(crash_log_path, "a", encoding="utf-8") as f:
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Crash at: {__import__('datetime').datetime.now()}\n")
                f.write(f"Error: {e}\n")
                traceback.print_exc(file=f)
        except Exception as log_e:
            print(f"Failed to write persistent crash log: {log_e}")
        
        sys.exit(1)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn')  # Ensures compatibility on macOS
    main()
