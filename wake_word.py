"""Wake-word detection logic."""

from pathlib import Path

from speech_to_text import SpeechToText

import config


class WakeWordDetector:
    """Detects the configured wake word in transcribed audio."""

    def __init__(self, wake_word: str = config.WAKE_WORD) -> None:
        self.wake_word = wake_word.lower()
        self.stt = SpeechToText()

    def detect_from_audio(self, audio_file: Path) -> bool:
        """Transcribe a short audio chunk and detect wake word."""
        text = self.stt.transcribe_file(audio_file).lower()
        return self.wake_word in text
