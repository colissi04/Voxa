import customtkinter as ctk
from typing import Optional
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
        
        # Create control buttons
        self.record_button = ctk.CTkButton(
            self.sidebar,
            text="Start Recording",
            command=self._toggle_recording,
            state="normal" if self.audio_service.cable_device is not None else "disabled"
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
            text="English Transcription",
            font=("Segoe UI", 14, "bold")
        )
        self.translation_label = ctk.CTkLabel(
            self.main_content,
            text="Portuguese Translation",
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
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.status_label.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.record_button.grid(row=1, column=0, padx=10, pady=10)
        self.help_text.grid(row=2, column=0, padx=10, pady=(10, 5))
        
        # Configure main content
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_rowconfigure(3, weight=1)
        
        # Place widgets in main content
        self.transcription_label.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.transcription_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.translation_label.grid(row=2, column=0, padx=10, pady=(10, 5))
        self.translation_text.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
    
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
                        translation = self.translation_service.translate(text)
                        self.update_ui(text, translation)
                except queue.Empty:
                    continue
        
        self.processing_thread = threading.Thread(target=process_text, daemon=True)
        self.processing_thread.start()
    
    def update_ui(self, transcription: str, translation: str):
        self.transcription_text.insert("end", transcription + "\n")
        self.transcription_text.see("end")
        self.translation_text.insert("end", translation + "\n")
        self.translation_text.see("end")
        self.conversation_manager.add_entry(transcription, translation)
    
    def run(self):
        self.mainloop() 