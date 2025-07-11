import os
import threading
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from typing import List

from compressors.docx_compressor import DOCXCompressor
from compressors.pdf_compressor import PDFCompressor
from compressors.image_compressor import ImageCompressor
from compressors.office_generic import compress_office_images
from utils.file_utils import get_supported_extensions, get_output_path, get_file_type, validate_file_path
from utils.sound import play_success_sound
from utils.i18n import i18n
from utils.settings_manager import settings_manager
from .settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)

class CompressorApp:
    """Main GUI application for file compression with internationalization support."""
    
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.output_dir = settings_manager.get_output_directory()
        
        # Load settings from settings manager
        self.jpeg_quality = settings_manager.get_jpeg_quality()
        self.auto_overwrite = settings_manager.get_auto_overwrite()
        self.show_progress = settings_manager.get_show_progress()
        self.play_sound_enabled = settings_manager.get_play_sound()
        
        # Initialize compressors with loaded settings
        self.docx_compressor = DOCXCompressor(jpeg_quality=self.jpeg_quality)
        self.pdf_compressor = PDFCompressor()
        self.image_compressor = ImageCompressor(jpeg_quality=self.jpeg_quality)
        
        # Set initial language based on settings or system
        saved_language = settings_manager.get_language()
        if saved_language:
            i18n.set_language(saved_language)
        else:
            system_lang = i18n.get_system_language()
            i18n.set_language(system_lang)
        
        self.setup_ui()
        self.setup_drag_drop()
        self.setup_keyboard_shortcuts()
        self.update_ui_texts()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.root.title(i18n.get_text("app_title"))
        self.root.geometry("518x500")  # Increased height to accommodate debug label
        
        # Create menu bar
        self.create_menu()
        
        # Main label
        self.main_label = tk.Label(self.root, pady=10, wraplength=400, text=i18n.get_text("main_label"))
        self.main_label.pack()
        
        # PDF Quality Dropdown
        self.pdf_quality_label = tk.Label(self.root, text=i18n.get_text("pdf_quality_label"))
        self.pdf_quality_label.pack()
        
        self.pdf_quality_var = tk.StringVar(value='/screen')
        self.pdf_quality_menu = ttk.OptionMenu(
            self.root, 
            self.pdf_quality_var, 
            '/screen', 
            '/screen', 
            '/ebook', 
            '/printer', 
            '/prepress'
        )
        self.pdf_quality_menu.pack()
        
        # Progress section
        self.progress_label = tk.Label(self.root, pady=5, text=i18n.get_text("progress_idle"))
        self.progress_label.pack()
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root, 
            variable=self.progress_var, 
            maximum=100, 
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        # Buttons
        self.select_files_button = tk.Button(
            self.root, 
            text=i18n.get_text("select_files_button"),
            command=self.select_files, 
            padx=10, 
            pady=5
        )
        self.select_files_button.pack()
        
        self.output_dir_button = tk.Button(
            self.root, 
            text=i18n.get_text("select_output_dir_button"),
            command=self.select_output_dir, 
            padx=10, 
            pady=5
        )
        self.output_dir_button.pack()
        
        self.output_dir_label = tk.Label(self.root, pady=5, text=i18n.get_text("output_dir_label"))
        self.output_dir_label.pack()
    
    def create_menu(self):
        """Create the menu bar with language selection."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.get_text("language_menu"), menu=language_menu)
        
        # Add language options
        for lang_code, lang_name in i18n.get_available_languages().items():
            language_menu.add_command(
                label=lang_name,
                command=lambda code=lang_code: self.change_language(code)
            )
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.get_text("settings_menu"), menu=settings_menu)
        settings_menu.add_command(label=i18n.get_text("settings_title"), command=self.open_settings)
        
        # About menu
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.get_text("about_menu"), menu=about_menu)
        about_menu.add_command(label="DOCX/PDF Compressor v1.0", command=self.show_about)
    
    def open_settings(self):
        """Open the settings dialog."""
        SettingsDialog(self)
    
    def update_settings(self, settings):
        """Update application settings."""
        # Save settings to persistent storage first
        settings_manager.update_settings(settings)
        
        # Reload settings from settings manager to ensure consistency
        self.jpeg_quality = settings_manager.get_jpeg_quality()
        self.auto_overwrite = settings_manager.get_auto_overwrite()
        self.show_progress = settings_manager.get_show_progress()
        self.play_sound_enabled = settings_manager.get_play_sound()
        
        # Update compressors with new JPEG quality
        self.docx_compressor = DOCXCompressor(jpeg_quality=self.jpeg_quality)
        self.image_compressor = ImageCompressor(jpeg_quality=self.jpeg_quality)
    
    def change_language(self, language_code):
        """Change the application language."""
        i18n.set_language(language_code)
        # Save language setting
        settings_manager.set_setting('language', language_code)
        self.update_ui_texts()
        self.recreate_menu()
    
    def recreate_menu(self):
        """Recreate the entire menu bar with updated language."""
        # Remove existing menu
        self.root.config(menu=None)
        
        # Create new menu
        self.create_menu()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        # Get flag emoji based on current language
        flag_emoji = self.get_flag_emoji()
        self.root.title(f"{flag_emoji} File Compressor by LD✨")
        self.main_label.config(text=i18n.get_text("main_label"))
        self.pdf_quality_label.config(text=i18n.get_text("pdf_quality_label"))
        self.select_files_button.config(text=i18n.get_text("select_files_button"))
        self.output_dir_button.config(text=i18n.get_text("select_output_dir_button"))
        
        if self.output_dir:
            self.output_dir_label.config(text=i18n.get_text("output_dir_selected", directory=self.output_dir))
        else:
            self.output_dir_label.config(text=i18n.get_text("output_dir_label"))
        
        self.progress_label.config(text=i18n.get_text("progress_idle"))
    
    def get_flag_emoji(self):
        """Get flag emoji based on current language."""
        flag_map = {
            'en': '🇺🇸',
            'de': '🇩🇪', 
            'fr': '🇫🇷',
            'zh': '🇨🇳',
            'ja': '🇯🇵',
            'vi': '🇻🇳',
            'th': '🇹🇭'
        }
        return flag_map.get(i18n.current_language, '🇺🇸')
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About", 
            "DOCX/PDF Compressor v1.0\n\nA tool for compressing DOCX, PDF, and image files.\n\nSupports multiple languages."
        )
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality."""
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for the application."""
        # Cmd+W to close the main window
        self.root.bind('<Command-w>', lambda event: self.root.quit())
        self.root.bind('<Command-W>', lambda event: self.root.quit())
        
        # Also bind to all child windows that might be created
        self.root.bind_class('Toplevel', '<Command-w>', lambda event: event.widget.destroy())
        self.root.bind_class('Toplevel', '<Command-W>', lambda event: event.widget.destroy())
    
    def select_output_dir(self):
        """Select output directory for compressed files."""
        dir_selected = filedialog.askdirectory()
        if dir_selected:
            self.output_dir = dir_selected
            # Save output directory setting
            settings_manager.set_setting('output_directory', dir_selected)
            self.output_dir_label.config(text=i18n.get_text("output_dir_selected", directory=self.output_dir))
        else:
            self.output_dir = None
            settings_manager.set_setting('output_directory', None)
            self.output_dir_label.config(text=i18n.get_text("output_dir_label"))
    
    def select_files(self):
        """Open file dialog to select files for compression."""
        files = filedialog.askopenfilenames(filetypes=[
            (i18n.get_text("supported_files"), i18n.get_text("file_types")),
            (i18n.get_text("word_documents"), i18n.get_text("word_types")),
            (i18n.get_text("pdf_files"), i18n.get_text("pdf_types")),
            (i18n.get_text("image_files"), i18n.get_text("image_types")),
            (i18n.get_text("excel_files"), i18n.get_text("excel_types")),
            (i18n.get_text("powerpoint_files"), i18n.get_text("powerpoint_types"))
        ])
        if files:
            self.compress_files(files)
    
    def handle_drop(self, event):
        """Handle file drop events."""
        exts = tuple(get_supported_extensions())
        files = self.root.tk.splitlist(event.data)
        files = [f.strip('{}') for f in files]
        all_files = []
        
        for f in files:
            if os.path.isdir(f):
                # Recursively add all supported files in the folder
                for dirpath, _, filenames in os.walk(f):
                    for name in filenames:
                        if name.lower().endswith(exts):
                            all_files.append(os.path.join(dirpath, name))
            elif f.lower().endswith(exts):
                all_files.append(f)
        
        if all_files:
            self.compress_files(all_files)
        else:
            messagebox.showwarning(
                i18n.get_text("invalid_file_title"), 
                i18n.get_text("invalid_file_message")
            )
    
    def update_progress(self, current, total):
        """Update progress bar and label."""
        def do_update():
            if total > 0 and self.show_progress:
                percent = (current / total) * 100
                self.progress_var.set(percent)
                self.progress_label.config(text=i18n.get_text("progress_compressing", current=current, total=total))
                self.root.update_idletasks()
            else:
                self.progress_var.set(0)
                self.progress_label.config(text=i18n.get_text("progress_idle"))
                self.root.update_idletasks()
        # Always schedule UI updates on the main thread
        self.root.after(0, do_update)
    
    def compress_files(self, files: List[str]):
        """Compress multiple files in a separate thread."""
        def compress_worker():
            success = 0
            errors = []
            total = len(files)
            error_log_path = os.path.join(os.getcwd(), 'error_log.txt')
            
            def log_error(msg):
                logger.error(msg)
                errors.append(msg)
                try:
                    with open(error_log_path, 'a', encoding='utf-8') as f:
                        f.write(msg + '\n')
                except Exception as log_e:
                    logger.error(i18n.get_text("failed_write_log", error=str(log_e)))
            
            for idx, file_path in enumerate(files, 1):
                self.update_progress(idx, total)
                
                # Validate file path for security
                if not validate_file_path(file_path):
                    log_error(f"Invalid or inaccessible file path: {file_path}")
                    continue
                
                ftype = get_file_type(file_path)
                try:
                    if ftype == 'docx':
                        output_path = get_output_path(file_path, self.output_dir, '_compressed')
                        if os.path.exists(output_path) and not self.auto_overwrite:
                            overwrite = messagebox.askyesno(
                                i18n.get_text("overwrite_question"), 
                                i18n.get_text("overwrite_message", file_path=output_path)
                            )
                            if not overwrite:
                                continue
                        compressed_path = self.docx_compressor.compress(
                            file_path, 
                            error_list=errors, 
                            out_dir=self.output_dir
                        )
                        if compressed_path:
                            logger.info(i18n.get_text("compressed_docx", path=compressed_path))
                            success += 1
                        else:
                            log_error(i18n.get_text("failed_compress_docx", path=file_path))
                    elif ftype == 'pdf':
                        output_path = get_output_path(file_path, self.output_dir, '_compressed')
                        if os.path.exists(output_path) and not self.auto_overwrite:
                            overwrite = messagebox.askyesno(
                                i18n.get_text("overwrite_question"), 
                                i18n.get_text("overwrite_message", file_path=output_path)
                            )
                            if not overwrite:
                                continue
                        compressed_pdf = self.pdf_compressor.compress(
                            file_path, 
                            error_list=errors, 
                            out_dir=self.output_dir, 
                            quality=self.pdf_quality_var.get()
                        )
                        if compressed_pdf:
                            logger.info(i18n.get_text("compressed_pdf", path=compressed_pdf))
                            success += 1
                        else:
                            log_error(i18n.get_text("failed_compress_pdf", path=file_path))
                    elif ftype == 'image':
                        output_path = get_output_path(file_path, self.output_dir, '_compressed')
                        if os.path.exists(output_path) and not self.auto_overwrite:
                            overwrite = messagebox.askyesno(
                                i18n.get_text("overwrite_question"), 
                                i18n.get_text("overwrite_message", file_path=output_path)
                            )
                            if not overwrite:
                                continue
                        compressed_img = self.image_compressor.compress(
                            file_path, 
                            error_list=errors, 
                            out_dir=self.output_dir
                        )
                        if compressed_img:
                            logger.info(i18n.get_text("compressed_image", path=compressed_img))
                            success += 1
                        else:
                            log_error(i18n.get_text("failed_compress_image", path=file_path))
                    elif ftype == 'excel':
                        output_path = get_output_path(file_path, self.output_dir, '_compressed')
                        if os.path.exists(output_path) and not self.auto_overwrite:
                            overwrite = messagebox.askyesno(
                                i18n.get_text("overwrite_question"), 
                                i18n.get_text("overwrite_message", file_path=output_path)
                            )
                            if not overwrite:
                                continue
                        compressed = compress_office_images(file_path, "xl/media", quality=self.jpeg_quality)
                        if compressed:
                            logger.info(i18n.get_text("compressed_excel", path=compressed))
                            success += 1
                        else:
                            log_error(i18n.get_text("failed_compress_excel", path=file_path))
                    elif ftype == 'ppt':
                        output_path = get_output_path(file_path, self.output_dir, '_compressed')
                        if os.path.exists(output_path) and not self.auto_overwrite:
                            overwrite = messagebox.askyesno(
                                i18n.get_text("overwrite_question"), 
                                i18n.get_text("overwrite_message", file_path=output_path)
                            )
                            if not overwrite:
                                continue
                        compressed = compress_office_images(file_path, "ppt/media", quality=self.jpeg_quality)
                        if compressed:
                            logger.info(i18n.get_text("compressed_powerpoint", path=compressed))
                            success += 1
                        else:
                            log_error(i18n.get_text("failed_compress_powerpoint", path=file_path))
                    else:
                        msg = i18n.get_text("unsupported_file_type", path=file_path)
                        log_error(msg)
                except Exception as e:
                    msg = i18n.get_text("error_compressing", path=file_path, error=str(e))
                    log_error(msg)
            self.update_progress(0, 0)
            if self.play_sound_enabled:
                play_success_sound()
            msg = i18n.get_text("success_message", count=success)
            if errors:
                # Limit the number of errors shown to prevent overwhelming the user
                max_errors_to_show = 10
                if len(errors) > max_errors_to_show:
                    shown_errors = errors[:max_errors_to_show]
                    remaining_count = len(errors) - max_errors_to_show
                    msg += f"\n\n{i18n.get_text('error_message', errors='\n'.join(shown_errors))}"
                    msg += f"\n\n... and {remaining_count} more errors. Check error_log.txt for full details."
                else:
                    msg += f"\n\n{i18n.get_text('error_message', errors='\n'.join(errors))}"
            # Show messagebox on the main thread
            self.root.after(0, lambda: messagebox.showinfo(i18n.get_text("done_title"), msg))
        
        threading.Thread(target=compress_worker).start()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop() 