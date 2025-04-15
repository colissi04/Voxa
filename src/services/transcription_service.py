from faster_whisper import WhisperModel
import numpy as np
from queue import Queue, Empty
import threading
from typing import Optional
import torch

class TranscriptionService:
    def __init__(self, audio_queue: Queue, text_queue: Queue, model_size: str = "base"):
        self.audio_queue = audio_queue
        self.text_queue = text_queue
        self.running = False
        self.processing_thread: Optional[threading.Thread] = None
        
        # Initialize Whisper model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
    
    def process_audio(self) -> None:
        """Process audio chunks and transcribe them."""
        audio_buffer = []
        
        while self.running:
            try:
                audio_chunk = self.audio_queue.get(timeout=0.1)
                audio_buffer.extend(audio_chunk)
                
                # Process when buffer reaches ~2 seconds of audio
                if len(audio_buffer) >= 32000:  # 2 seconds at 16kHz
                    audio_data = np.array(audio_buffer)
                    segments, _ = self.model.transcribe(
                        audio_data,
                        language="en",
                        vad_filter=True
                    )
                    
                    text = " ".join(segment.text for segment in segments)
                    if text.strip():
                        self.text_queue.put(text)
                    
                    # Clear buffer but keep a small overlap
                    audio_buffer = audio_buffer[-4000:]  # Keep last 0.25 seconds
            
            except Empty:
                continue
    
    def start(self) -> None:
        """Start the transcription service."""
        self.running = True
        self.processing_thread = threading.Thread(target=self.process_audio)
        self.processing_thread.start()
    
    def stop(self) -> None:
        """Stop the transcription service."""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join()
            self.processing_thread = None 