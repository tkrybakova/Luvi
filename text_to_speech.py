"""Text-to-speech playback using Piper."""

from __future__ import annotations

import shutil
import subprocess
import uuid
from pathlib import Path

import simpleaudio as sa

import config


class TTSUnavailableError(RuntimeError):
    """Raised when local TTS prerequisites are missing."""


class TextToSpeech:
    """Synthesizes and plays speech with local Piper models."""

    def __init__(self) -> None:
        config.PIPER_OUTPUT_DIR.mkdir(exist_ok=True)
        self.enabled = True
        self.unavailable_reason = ""
        self._validate_runtime()

    def _validate_runtime(self) -> None:
        """Validate local Piper binary and model path once at startup."""
        binary_path = shutil.which(config.PIPER_BINARY)
        if binary_path is None:
            self.enabled = False
            self.unavailable_reason = (
                f"Piper binary '{config.PIPER_BINARY}' was not found in PATH. "
                "Install Piper or set PIPER_BINARY in config.py."
            )
            return

        model_path = Path(config.PIPER_MODEL_PATH)
        if not model_path.exists():
            self.enabled = False
            self.unavailable_reason = (
                f"Piper model file '{config.PIPER_MODEL_PATH}' was not found. "
                "Download a voice model and set PIPER_MODEL_PATH in config.py."
            )

    def speak(self, text: str) -> None:
        if not self.enabled:
            raise TTSUnavailableError(self.unavailable_reason)

        wav_path = config.PIPER_OUTPUT_DIR / f"{uuid.uuid4().hex}.wav"

        process = subprocess.run(
            [
                config.PIPER_BINARY,
                "--model",
                config.PIPER_MODEL_PATH,
                "--output_file",
                str(wav_path),
            ],
            input=text.encode("utf-8"),
            capture_output=True,
            check=False,
        )

        if process.returncode != 0:
            raise RuntimeError(f"Piper synthesis failed: {process.stderr.decode('utf-8', errors='ignore')}")

        wave_obj = sa.WaveObject.from_wave_file(str(wav_path))
        play_obj = wave_obj.play()
        play_obj.wait_done()
