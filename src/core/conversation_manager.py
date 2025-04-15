from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class ConversationManager:
    def __init__(self, save_dir: Optional[str] = None):
        self.entries: List[Dict] = []
        self.save_dir = save_dir or os.path.join(os.path.expanduser("~"), "voxa_history")
        os.makedirs(self.save_dir, exist_ok=True)
    
    def add_entry(self, transcription: str, translation: Optional[str] = None) -> None:
        """Add a new conversation entry."""
        entry = {
            'timestamp': datetime.now(),
            'transcription': transcription,
            'translation': translation
        }
        self.entries.append(entry)
        self._auto_save()
    
    def get_entries(self) -> List[Dict]:
        """Get all conversation entries."""
        return self.entries
    
    def clear(self) -> None:
        """Clear all conversation entries."""
        self.entries = []
        self._auto_save()
    
    def _auto_save(self) -> None:
        """Automatically save the conversation history to a file."""
        filename = datetime.now().strftime("%Y%m%d") + ".json"
        filepath = os.path.join(self.save_dir, filename)
        
        history_data = [
            {
                "timestamp": entry['timestamp'].isoformat(),
                "transcription": entry['transcription'],
                "translation": entry['translation']
            }
            for entry in self.entries
        ]
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    
    def load_history(self, date: Optional[datetime] = None) -> None:
        """Load conversation history from a file."""
        if date is None:
            date = datetime.now()
        
        filename = date.strftime("%Y%m%d") + ".json"
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            return
        
        with open(filepath, "r", encoding="utf-8") as f:
            history_data = json.load(f)
        
        self.entries = [
            {
                'timestamp': datetime.fromisoformat(entry["timestamp"]),
                'transcription': entry["transcription"],
                'translation': entry["translation"]
            }
            for entry in history_data
        ]
    
    def save_to_file(self, filename: str) -> None:
        """Save conversation to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(f"[{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}]\n")
                f.write(f"Transcription: {entry['transcription']}\n")
                if entry['translation']:
                    f.write(f"Translation: {entry['translation']}\n")
                f.write("\n") 