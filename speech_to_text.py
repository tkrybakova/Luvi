"""Speech-to-text support using faster-whisper."""

from __future__ import annotations

from pathlib import Path

from faster_whisper import WhisperModel

import config


class SpeechToText:
    """Converts spoken audio files to text with faster-whisper."""

    def __init__(
        self,
        model_size: str = config.WHISPER_MODEL_SIZE,
        language: str | None = config.WHISPER_LANGUAGE,
    ) -> None:
        self.model_size = model_size
        self.language = language
        self.model: WhisperModel | None = None

    def _ensure_model(self) -> WhisperModel:
        """Load whisper model lazily to avoid blocking app startup."""
        if self.model is None:
            self.model = WhisperModel(self.model_size, device="auto", compute_type="int8")
        return self.model

    def transcribe_file(self, audio_file: Path) -> str:
        """Return transcribed text from an audio file path."""
        model = self._ensure_model()
        segments, _ = model.transcribe(
            str(audio_file),
            language=self.language,
            beam_size=config.WHISPER_BEAM_SIZE,
            best_of=config.WHISPER_BEST_OF,
            temperature=config.WHISPER_TEMPERATURE,
            vad_filter=config.WHISPER_VAD_FILTER,
            condition_on_previous_text=False,
            initial_prompt=config.WHISPER_INITIAL_PROMPT,
        )
        return " ".join(segment.text.strip() for segment in segments).strip()
