from __future__ import annotations

import queue
import tempfile
import threading
from pathlib import Path
from typing import Callable

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

import config
from speech_to_text import SpeechToText
from wake_word import WakeWordDetector


class VoiceListener:
    """Continuously listens for wake-word then transcribes user commands."""

    def __init__(self, on_command: Callable[[str], None], on_status: Callable[[str], None]) -> None:
        self.on_command = on_command
        self.on_status = on_status
        self._stop_event = threading.Event()

        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()

        self.wake_detector = WakeWordDetector()
        self.stt = SpeechToText()

    def start(self) -> None:
        """Start listener loop on a daemon thread."""
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def stop(self) -> None:
        """Request background loop stop."""
        self._stop_event.set()

    def _record_audio(self, seconds: float) -> np.ndarray:
        frames = int(seconds * config.SAMPLE_RATE)
        audio = sd.rec(frames, samplerate=config.SAMPLE_RATE, channels=config.CHANNELS, dtype="int16")
        sd.wait()
        return audio

    def _save_temp_wav(self, audio: np.ndarray) -> Path:
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        write(temp.name, config.SAMPLE_RATE, audio)
        return Path(temp.name)

    def _listen_loop(self) -> None:
        self.on_status("Listening for wake word...")
        while not self._stop_event.is_set():
            wake_path: Path | None = None
            cmd_path: Path | None = None
            try:
                wake_audio = self._record_audio(config.WAKE_LISTEN_SECONDS)
                wake_path = self._save_temp_wav(wake_audio)

                if not self.wake_detector.detect_from_audio(wake_path):
                    continue

                self.on_status("Wake word detected. Listening for command...")
                cmd_audio = self._record_audio(config.COMMAND_RECORD_SECONDS)
                cmd_path = self._save_temp_wav(cmd_audio)
                command_text = self.stt.transcribe_file(cmd_path)

                if command_text:
                    self.on_command(command_text)
            except Exception as exc:  # noqa: BLE001 - runtime device/model failures
                self.on_status(f"Voice listener error: {exc}")
            finally:
                if wake_path and wake_path.exists():
                    wake_path.unlink(missing_ok=True)

                    self.on_status("Wake word detected")

                    self.on_status("Listening for command...")

                    cmd_audio = sd.rec(
                        int(config.COMMAND_RECORD_SECONDS * config.SAMPLE_RATE),
                        samplerate=config.SAMPLE_RATE,
                        channels=config.CHANNELS,
                        dtype="int16",
                        device=9
                    )

                    sd.wait()

                    cmd_path = self._save_temp_wav(cmd_audio)

                    command = self.stt.transcribe_file(cmd_path)

                    cmd_path.unlink(missing_ok=True)

            self.on_status("Listening for wake word...")
