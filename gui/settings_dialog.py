import tkinter as tk
from tkinter import ttk, messagebox
import logging
from utils.i18n import i18n
from utils.settings_manager import settings_manager
import os
import json

logger = logging.getLogger(__name__)

def _add_debug_style():
    # Add a red border style for debugging
    style = ttk.Style()
    style.configure('Red.TFrame', borderwidth=2, relief='solid', background='#ffcccc')

class SettingsDialog:
    """Settings dialog for the application."""
    
    def __init__(self, parent):
        self.parent = parent
        _add_debug_style()  # <-- moved here
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.geometry("500x650")  # Default initial width 500px
        self.dialog.resizable(True, True)
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (650 // 2)
        self.dialog.geometry(f"500x650+{x}+{y}")
        
        # Settings variables - load from settings manager
        self.jpeg_quality_var = tk.IntVar(value=settings_manager.get_jpeg_quality())
        self.auto_overwrite_var = tk.BooleanVar(value=settings_manager.get_auto_overwrite())
        self.show_progress_var = tk.BooleanVar(value=settings_manager.get_show_progress())
        self.play_sound_var = tk.BooleanVar(value=settings_manager.get_play_sound())
        
        self.setup_ui()
        
        # Dynamically resize to fit all widgets after layout
        self.dialog.update_idletasks()
        self.dialog.geometry(f"500x{self.dialog.winfo_reqheight()}")
        
        # Bind Enter and Esc keys
        self.dialog.bind('<Return>', lambda event: self.save_and_close())
        self.dialog.bind('<Escape>', lambda event: self.dialog.destroy())
        
        # Bind Cmd+W to close the dialog
        self.dialog.bind('<Command-w>', lambda event: self.dialog.destroy())
        self.dialog.bind('<Command-W>', lambda event: self.dialog.destroy())
        
        # Log loaded settings
        logger.info(f"Settings dialog opened with JPEG quality: {self.jpeg_quality_var.get()}")
        logger.info(f"Current settings manager JPEG quality: {settings_manager.get_jpeg_quality()}")
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=i18n.get_text("settings_title"), 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # JPEG Quality Setting
        jpeg_frame = ttk.LabelFrame(main_frame, text=i18n.get_text("jpeg_quality_setting"), padding="10")
        jpeg_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(jpeg_frame, text=i18n.get_text("jpeg_quality_description")).pack(anchor=tk.W)
        
        # Quality control frame
        quality_frame = ttk.Frame(jpeg_frame)
        quality_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Slider
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                      variable=self.jpeg_quality_var, orient=tk.HORIZONTAL)
        self.quality_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Input box for exact value
        self.quality_entry = ttk.Entry(quality_frame, width=8, textvariable=self.jpeg_quality_var)
        self.quality_entry.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Label for units
        ttk.Label(quality_frame, text="%").pack(side=tk.RIGHT)
        
        # Bind events for synchronization
        self.quality_scale.config(command=self.update_quality_from_scale)
        self.quality_entry.bind('<KeyRelease>', self.update_quality_from_entry)
        self.quality_entry.bind('<FocusOut>', self.validate_quality_entry)
        
        # Bind auto-save events for checkboxes
        self._auto_overwrite_trace = self.auto_overwrite_var.trace_add('write', self.on_setting_changed)
        self._show_progress_trace = self.show_progress_var.trace_add('write', self.on_setting_changed)
        self._play_sound_trace = self.play_sound_var.trace_add('write', self.on_setting_changed)
        
        # Set initial value
        self.update_quality_display()
        
        # Auto Overwrite Setting
        overwrite_frame = ttk.LabelFrame(main_frame, text=i18n.get_text("auto_overwrite_setting"), padding="10")
        overwrite_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(overwrite_frame, text=i18n.get_text("auto_overwrite_description")).pack(anchor=tk.W)
        ttk.Checkbutton(overwrite_frame, variable=self.auto_overwrite_var).pack(anchor=tk.W, pady=(5, 0))
        
        # Show Progress Setting
        progress_frame = ttk.LabelFrame(main_frame, text=i18n.get_text("show_progress_setting"), padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(progress_frame, text=i18n.get_text("show_progress_description")).pack(anchor=tk.W)
        ttk.Checkbutton(progress_frame, variable=self.show_progress_var).pack(anchor=tk.W, pady=(5, 0))
        
        # Play Sound Setting
        sound_frame = ttk.LabelFrame(main_frame, text=i18n.get_text("play_sound_setting"), padding="10")
        sound_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(sound_frame, text=i18n.get_text("play_sound_description")).pack(anchor=tk.W)
        ttk.Checkbutton(sound_frame, variable=self.play_sound_var).pack(anchor=tk.W, pady=(5, 0))
        
        # Status label for save feedback
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.pack(pady=(10, 0))
        
        # --- BUTTONS AT THE BOTTOM ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0), anchor='e')
        
        # Reset to Defaults (♻️) - left side
        reset_button = ttk.Button(button_frame, text="♻️ " + i18n.get_text("reset_defaults_button"), command=self.reset_to_defaults)
        reset_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel (❌) - right side
        cancel_button = ttk.Button(button_frame, text="❌ " + i18n.get_text("cancel_button"), command=self.dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Save (💾) - right side
        self.save_button = ttk.Button(button_frame, text="💾 " + i18n.get_text("save_button"), command=self.save_and_close)
        self.save_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def update_quality_from_scale(self, value):
        """Update quality from slider changes."""
        try:
            quality = int(float(value))
            self.jpeg_quality_var.set(quality)
            self.update_quality_display()
        except ValueError:
            pass
    
    def update_quality_from_entry(self, event=None):
        """Update quality from entry box changes."""
        try:
            value = self.quality_entry.get()
            if value.strip():
                quality = int(value)
                if 1 <= quality <= 100:
                    self.jpeg_quality_var.set(quality)
                    self.update_quality_display()
        except ValueError:
            pass
    
    def validate_quality_entry(self, event=None):
        """Validate and correct quality entry value."""
        try:
            value = self.quality_entry.get()
            if value.strip():
                quality = int(value)
                if quality < 1:
                    quality = 1
                elif quality > 100:
                    quality = 100
                self.jpeg_quality_var.set(quality)
                self.update_quality_display()
        except ValueError:
            # If invalid, reset to current variable value
            self.update_quality_display()
    
    def update_quality_display(self):
        """Update the display of quality value."""
        quality = self.jpeg_quality_var.get()
        self.quality_entry.delete(0, tk.END)
        self.quality_entry.insert(0, str(quality))
    
    def save_settings(self):
        """Save the current settings."""
        try:
            # Get current settings from UI
            new_settings = {
                'jpeg_quality': self.jpeg_quality_var.get(),
                'auto_overwrite': self.auto_overwrite_var.get(),
                'show_progress': self.show_progress_var.get(),
                'play_sound': self.play_sound_var.get()
            }
            
            logger.info(f"Saving settings: {new_settings}")
            
            # Update settings manager
            success = settings_manager.update_settings(new_settings)
            
            if success:
                # Update parent application settings
                if hasattr(self.parent, 'update_settings'):
                    self.parent.update_settings(new_settings)
                
                # Show success feedback
                self.status_label.config(text="✓ Settings saved successfully!", foreground="green")
                self.save_button.config(state="disabled")  # Temporarily disable save button
                
                # Re-enable save button after 2 seconds
                self.dialog.after(2000, lambda: self.save_button.config(state="normal"))
                self.dialog.after(3000, lambda: self.status_label.config(text=""))
                
                print(f"Settings saved successfully. JPEG quality: {new_settings['jpeg_quality']}")
                
                # Verify settings were actually saved
                saved_quality = settings_manager.get_jpeg_quality()
                print(f"Verified saved JPEG quality: {saved_quality}")
                if saved_quality != new_settings['jpeg_quality']:
                    print(f"WARNING: Saved quality ({saved_quality}) doesn't match requested quality ({new_settings['jpeg_quality']})")
            else:
                self.status_label.config(text="✗ Failed to save settings!", foreground="red")
                print("Failed to save settings")
            
        except Exception as e:
            error_msg = f"Failed to save settings: {e}"
            self.status_label.config(text=f"✗ {error_msg}", foreground="red")
            print(error_msg)
    
    def save_and_close(self):
        """Save settings and close the dialog immediately after saving."""
        self.save_settings()
        self.dialog.destroy()
    
    def on_setting_changed(self, *args):
        """Called when a setting is changed - enables save button."""
        self.save_button.config(state="normal")
        self.status_label.config(text="Settings changed - click 'Save Settings' to save", foreground="blue")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        # Remove traces to avoid triggering during reset
        try:
            self.auto_overwrite_var.trace_remove('write', self._auto_overwrite_trace)
            self.show_progress_var.trace_remove('write', self._show_progress_trace)
            self.play_sound_var.trace_remove('write', self._play_sound_trace)
        except Exception:
            pass
        # Reset values
        self.jpeg_quality_var.set(settings_manager.get_default_settings()['jpeg_quality'])
        self.auto_overwrite_var.set(settings_manager.get_default_settings()['auto_overwrite'])
        self.show_progress_var.set(settings_manager.get_default_settings()['show_progress'])
        self.play_sound_var.set(settings_manager.get_default_settings()['play_sound'])
        self.update_quality_display()
        # Re-bind traces
        self._auto_overwrite_trace = self.auto_overwrite_var.trace_add('write', self.on_setting_changed)
        self._show_progress_trace = self.show_progress_var.trace_add('write', self.on_setting_changed)
        self._play_sound_trace = self.play_sound_var.trace_add('write', self.on_setting_changed)
        self.status_label.config(text=i18n.get_text("settings_saved")) 