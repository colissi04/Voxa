from deep_translator import GoogleTranslator
from typing import Optional

class TranslationService:
    SUPPORTED_LANGUAGES = {
        "Português": "pt",
        "English": "en",
        "Español": "es"
    }
    
    def __init__(self):
        self.source_lang = "en"
        self.target_lang = "pt"
        self._update_translator()
        self._last_text: Optional[str] = None
        self._last_translation: Optional[str] = None
    
    def set_languages(self, source_lang_name: str, target_lang_name: str) -> None:
        """Set the source and target languages for translation."""
        if source_lang_name in self.SUPPORTED_LANGUAGES and target_lang_name in self.SUPPORTED_LANGUAGES:
            self.source_lang = self.SUPPORTED_LANGUAGES[source_lang_name]
            self.target_lang = self.SUPPORTED_LANGUAGES[target_lang_name]
            self._update_translator()
    
    def _update_translator(self) -> None:
        """Update the translator with current language settings."""
        self.translator = GoogleTranslator(
            source=self.source_lang,
            target=self.target_lang
        )
    
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