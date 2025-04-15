from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import json
import os

@dataclass
class ConversationEntry:
    timestamp: datetime
    original_text: str
    translated_text: str

class ConversationManager:
    def __init__(self, save_dir: Optional[str] = None):
        self.entries: List[ConversationEntry] = []
        self.save_dir = save_dir or os.path.join(os.path.expanduser("~"), "voxa_history")
        os.makedirs(self.save_dir, exist_ok=True)
    
    def add_entry(self, original_text: str, translated_text: str) -> None:
        """Add a new conversation entry."""
        entry = ConversationEntry(
            timestamp=datetime.now(),
            original_text=original_text,
            translated_text=translated_text
        )
        self.entries.append(entry)
        self._auto_save()
    
    def get_history(self) -> List[ConversationEntry]:
        """Get all conversation entries."""
        return self.entries
    
    def clear_history(self) -> None:
        """Clear all conversation entries."""
        self.entries = []
        self._auto_save()
    
    def _auto_save(self) -> None:
        """Automatically save the conversation history to a file."""
        filename = datetime.now().strftime("%Y%m%d") + ".json"
        filepath = os.path.join(self.save_dir, filename)
        
        history_data = [
            {
                "timestamp": entry.timestamp.isoformat(),
                "original_text": entry.original_text,
                "translated_text": entry.translated_text
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
            ConversationEntry(
                timestamp=datetime.fromisoformat(entry["timestamp"]),
                original_text=entry["original_text"],
                translated_text=entry["translated_text"]
            )
            for entry in history_data
        ] 