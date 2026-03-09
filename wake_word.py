"""Wake-word detection logic."""

from __future__ import annotations

import re
from pathlib import Path

from speech_to_text import SpeechToText

import config


class WakeWordDetector:
    """Detects wake words (e.g. Luvi / Луви) in transcribed audio."""

    def __init__(self, wake_words: tuple[str, ...] = config.WAKE_WORD_ALIASES) -> None:
        self.wake_words = tuple(word.lower() for word in wake_words)
        self.stt = SpeechToText()

    def detect_from_audio(self, audio_file: Path) -> bool:
        """Transcribe a short audio chunk and detect wake word."""
        text = self.stt.transcribe_file(audio_file)
        return self.detect_in_text(text)

    def detect_in_text(self, text: str) -> bool:
        """Return True when any configured wake word appears in text."""
        normalized = self._normalize(text)
        return any(word in normalized for word in self.wake_words)

    def remove_wake_word(self, text: str) -> str:
        """Strip wake word from command text so router gets clean command."""
        cleaned = self._normalize(text)
        for word in self.wake_words:
            cleaned = re.sub(rf"\b{re.escape(word)}\b[,:!\-\s]*", "", cleaned, count=1)
        return cleaned.strip()

    def _normalize(self, text: str) -> str:
        return text.lower().replace("ё", "е").strip()
