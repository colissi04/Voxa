import sounddevice as sd
import numpy as np
from queue import Queue
from typing import Optional, List, Dict
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import psutil
import win32gui
import win32process

class AudioService:
    def __init__(self, audio_queue: Queue, sample_rate: int = 16000):
        self.audio_queue = audio_queue
        self.sample_rate = sample_rate
        self.recording = False
        self.stream: Optional[sd.InputStream] = None
        self.selected_app: Optional[Dict] = None
        
        # Find CABLE Output device
        self.cable_device = None
        for idx, device in enumerate(sd.query_devices()):
            if "CABLE Output" in device['name']:
                self.cable_device = idx
                break
    
    @staticmethod
    def list_applications() -> List[Dict]:
        """List all applications with audio sessions."""
        apps = []
        sessions = AudioUtilities.GetAllSessions()
        
        def get_app_name(pid):
            try:
                process = psutil.Process(pid)
                return process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None
        
        for session in sessions:
            if session.Process and session.Process.name() != "System":
                app_name = session.Process.name()
                pid = session.ProcessId
                
                apps.append({
                    'id': pid,
                    'name': app_name,
                    'session': session
                })
        
        return apps
    
    def select_application(self, app_id: int) -> None:
        """Select an application by its process ID."""
        apps = self.list_applications()
        for app in apps:
            if app['id'] == app_id:
                self.selected_app = app
                break
    
    def audio_callback(self, indata: np.ndarray, frames: int, time, status: sd.CallbackFlags) -> None:
        """Callback function for the audio stream."""
        if status:
            print(f"Audio callback status: {status}")
        if self.recording:
            # Convert to mono if stereo
            if len(indata.shape) > 1:
                audio_data = indata.mean(axis=1)
            else:
                audio_data = indata.copy()
            
            self.audio_queue.put(audio_data)
    
    def start_recording(self) -> None:
        """Start recording audio from VB-Cable Output."""
        if self.cable_device is None:
            raise ValueError("VB-Cable not found. Please install VB-Cable from https://vb-audio.com/Cable/")
        
        self.recording = True
        self.stream = sd.InputStream(
            device=self.cable_device,
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            callback=self.audio_callback,
            blocksize=4096
        )
        self.stream.start()
    
    def stop_recording(self) -> None:
        """Stop recording audio."""
        self.recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def get_status(self) -> str:
        """Get the current status of the audio service."""
        if self.cable_device is None:
            return "VB-Cable not found. Please install VB-Cable from https://vb-audio.com/Cable/"
        return "Ready to record" 