from deep_translator import GoogleTranslator
from typing import Optional

class TranslationService:
    def __init__(self, source_lang: str = "en", target_lang: str = "pt"):
        """Initialize the translation service.
        
        Args:
            source_lang: Source language code (default: "en" for English)
            target_lang: Target language code (default: "pt" for Portuguese)
        """
        self.translator = GoogleTranslator(
            source=source_lang,
            target=target_lang
        )
        self._last_text: Optional[str] = None
        self._last_translation: Optional[str] = None
    
    def translate(self, text: str) -> str:
        """Translate the given text.
        
        Args:
            text: Text to translate
        
        Returns:
            Translated text
        """
        # Skip if text is empty or only whitespace
        if not text.strip():
            return ""
        
        # Skip if text is the same as last time
        if text == self._last_text:
            return self._last_translation or ""
        
        try:
            translation = self.translator.translate(text)
            self._last_text = text
            self._last_translation = translation
            return translation
        except Exception as e:
            print(f"Translation error: {e}")
            return f"[Translation Error: {str(e)}]" 