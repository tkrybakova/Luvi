"""Speech-to-text support using faster-whisper."""

from pathlib import Path

from faster_whisper import WhisperModel

import config


class SpeechToText:
    """Converts spoken audio files to text with faster-whisper."""

    def __init__(self, model_size: str = config.WHISPER_MODEL_SIZE) -> None:
        self.model = WhisperModel(model_size, device="auto", compute_type="int8")

    def transcribe_file(self, audio_file: Path) -> str:
        """Return transcribed text from an audio file path."""
        segments, _ = self.model.transcribe(str(audio_file), language="en")
        return " ".join(segment.text.strip() for segment in segments).strip()
