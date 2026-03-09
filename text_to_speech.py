"""Text-to-speech playback using Piper."""

from __future__ import annotations

import subprocess
import uuid
from pathlib import Path

import simpleaudio as sa

import config


class TextToSpeech:
    """Synthesizes and plays speech with local Piper models."""

    def __init__(self) -> None:
        config.PIPER_OUTPUT_DIR.mkdir(exist_ok=True)

    def speak(self, text: str) -> None:
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
