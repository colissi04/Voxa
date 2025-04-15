import customtkinter as ctk
from typing import Optional, List
from ..services.audio_service import AudioService
from ..services.transcription_service import TranscriptionService
from ..services.translation_service import TranslationService
from ..core.conversation_manager import ConversationManager
import queue
import threading

class VoxaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Voxa - Real-time Translation")
        self.geometry("800x600")
        
        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize services
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.audio_service = AudioService(self.audio_queue)
        self.transcription_service = TranscriptionService(self.audio_queue, self.text_queue)
        self.translation_service = TranslationService()
        self.conversation_manager = ConversationManager()
        
        # Initialize UI state
        self.is_recording = False
        self.recording_thread: Optional[threading.Thread] = None
        self.should_translate = False
        self.languages = list(TranscriptionService.SUPPORTED_LANGUAGES.keys())
        
        self._create_widgets()
        self._create_layout()
        self._start_processing_thread()
    
    def _create_widgets(self):
        # Create main containers
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.main_content = ctk.CTkFrame(self)
        
        # Create status label
        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text=self.audio_service.get_status(),
            font=("Segoe UI", 12),
            wraplength=180
        )
        
        # Create language selection frame
        self.lang_frame = ctk.CTkFrame(self.sidebar)
        
        # Source language selection
        self.source_lang_label = ctk.CTkLabel(
            self.lang_frame,
            text="Idioma origem:",
            font=("Segoe UI", 12)
        )
        
        self.source_lang_var = ctk.StringVar(value="English")
        self.source_lang_menu = ctk.CTkOptionMenu(
            self.lang_frame,
            values=self.languages,
            variable=self.source_lang_var,
            command=self._on_language_change,
            width=140
        )
        
        # Target language selection (only visible when translation is enabled)
        self.target_lang_label = ctk.CTkLabel(
            self.lang_frame,
            text="Idioma destino:",
            font=("Segoe UI", 12)
        )
        
        self.target_lang_var = ctk.StringVar(value="Português")
        self.target_lang_menu = ctk.CTkOptionMenu(
            self.lang_frame,
            values=self.languages,
            variable=self.target_lang_var,
            command=self._on_language_change,
            width=140
        )
        
        # Create control buttons
        self.record_button = ctk.CTkButton(
            self.sidebar,
            text="Start Recording",
            command=self._toggle_recording,
            state="normal" if self.audio_service.cable_device is not None else "disabled"
        )
        
        # Create translation checkbox
        self.translate_var = ctk.BooleanVar(value=False)
        self.translate_checkbox = ctk.CTkCheckBox(
            self.sidebar,
            text="Traduzir",
            variable=self.translate_var,
            command=self._on_translate_toggle,
            font=("Segoe UI", 12),
            width=20,
            height=20,
            checkbox_width=16,
            checkbox_height=16,
            corner_radius=4
        )
        
        # Create text areas
        self.transcription_text = ctk.CTkTextbox(
            self.main_content,
            height=250,
            font=("Segoe UI", 12)
        )
        self.translation_text = ctk.CTkTextbox(
            self.main_content,
            height=250,
            font=("Segoe UI", 12)
        )
        
        # Create labels
        self.transcription_label = ctk.CTkLabel(
            self.main_content,
            text="Transcription",
            font=("Segoe UI", 14, "bold")
        )
        self.translation_label = ctk.CTkLabel(
            self.main_content,
            text="Translation",
            font=("Segoe UI", 14, "bold")
        )
        
        # Create help text
        self.help_text = ctk.CTkLabel(
            self.sidebar,
            text="1. Install VB-Cable\n2. Set your app's audio output to CABLE Input\n3. Click Start Recording",
            font=("Segoe UI", 12),
            wraplength=180,
            justify="left"
        )
    
    def _create_layout(self):
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Place main containers
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Configure sidebar
        self.sidebar.grid_rowconfigure(6, weight=1)
        self.status_label.grid(row=0, column=0, padx=10, pady=(10, 5))
        
        # Language selection frame
        self.lang_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.source_lang_label.grid(row=0, column=0, padx=5, pady=(5,0), sticky="w")
        self.source_lang_menu.grid(row=1, column=0, padx=5, pady=(0,5))
        self.target_lang_label.grid(row=2, column=0, padx=5, pady=(5,0), sticky="w")
        self.target_lang_menu.grid(row=3, column=0, padx=5, pady=(0,5))
        
        self.record_button.grid(row=2, column=0, padx=10, pady=10)
        self.translate_checkbox.grid(row=3, column=0, padx=10, pady=10)
        self.help_text.grid(row=4, column=0, padx=10, pady=(10, 5))
        
        # Configure main content
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_rowconfigure(3, weight=1)
        
        # Place widgets in main content
        self.transcription_label.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.transcription_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Initially hide translation widgets and update language visibility
        self._update_translation_visibility()
        self._update_language_labels()
    
    def _on_language_change(self, _: str = None) -> None:
        """Handle language selection change."""
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        
        # Update services
        self.transcription_service.set_language(source_lang)
        if self.should_translate:
            self.translation_service.set_languages(source_lang, target_lang)
        
        # Update labels
        self._update_language_labels()
    
    def _update_language_labels(self) -> None:
        """Update the labels to show the selected languages."""
        source_lang = self.source_lang_var.get()
        self.transcription_label.configure(text=f"Transcrição ({source_lang})")
        
        if self.should_translate:
            target_lang = self.target_lang_var.get()
            self.translation_label.configure(text=f"Tradução ({target_lang})")
    
    def _on_translate_toggle(self):
        """Handle translation checkbox toggle."""
        self.should_translate = self.translate_var.get()
        self._update_translation_visibility()
        
        if self.should_translate:
            # Update translation service with current languages
            self.translation_service.set_languages(
                self.source_lang_var.get(),
                self.target_lang_var.get()
            )
    
    def _update_translation_visibility(self):
        """Update visibility of translation widgets based on checkbox state."""
        if self.should_translate:
            self.target_lang_label.grid()
            self.target_lang_menu.grid()
            self.translation_label.grid(row=2, column=0, padx=10, pady=(10, 5))
            self.translation_text.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
            # Adjust transcription height
            self.transcription_text.configure(height=250)
            self.translation_text.configure(height=250)
        else:
            self.target_lang_label.grid_remove()
            self.target_lang_menu.grid_remove()
            self.translation_label.grid_remove()
            self.translation_text.grid_remove()
            # Make transcription use full height
            self.transcription_text.configure(height=520)
        
        self._update_language_labels()
    
    def _toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        try:
            self.is_recording = True
            self.record_button.configure(text="Stop Recording", fg_color="red")
            self.recording_thread = threading.Thread(target=self.audio_service.start_recording)
            self.recording_thread.start()
            self.transcription_service.start()
        except ValueError as e:
            self.is_recording = False
            print(f"Error starting recording: {e}")
            self.record_button.configure(text="Start Recording", fg_color=["#3B8ED0", "#1F6AA5"])
            self.status_label.configure(text=str(e))
    
    def stop_recording(self):
        self.is_recording = False
        self.record_button.configure(text="Start Recording", fg_color=["#3B8ED0", "#1F6AA5"])
        self.audio_service.stop_recording()
        self.transcription_service.stop()
        if self.recording_thread:
            self.recording_thread.join()
    
    def _start_processing_thread(self):
        def process_text():
            while True:
                try:
                    text = self.text_queue.get(timeout=0.1)
                    if text:
                        if self.should_translate:
                            translation = self.translation_service.translate(text)
                            self.update_ui(text, translation)
                        else:
                            self.update_ui(text, None)
                except queue.Empty:
                    continue
        
        self.processing_thread = threading.Thread(target=process_text, daemon=True)
        self.processing_thread.start()
    
    def update_ui(self, transcription: str, translation: Optional[str] = None):
        self.transcription_text.insert("end", transcription + "\n")
        self.transcription_text.see("end")
        
        if translation and self.should_translate:
            self.translation_text.insert("end", translation + "\n")
            self.translation_text.see("end")
            self.conversation_manager.add_entry(transcription, translation)
        else:
            self.conversation_manager.add_entry(transcription, None)
    
    def run(self):
        self.mainloop() 