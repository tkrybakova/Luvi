"""Microphone listening loop for wake-word activation and command capture."""

from __future__ import annotations

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

    def __init__(
        self,
        on_command: Callable[[str], None],
        on_status: Callable[[str], None],
        on_level: Callable[[float], None] | None = None,
    ) -> None:
        self.on_command = on_command
        self.on_status = on_status
        self.on_level = on_level
        self._stop_event = threading.Event()
        self._running = False
        self.wake_detector = WakeWordDetector()
        self.stt = SpeechToText()

    def start(self) -> None:
        """Start listener loop on a daemon thread."""
        if self._running:
            return
        self._stop_event.clear()
        self._running = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def stop(self) -> None:
        """Request background loop stop."""
        self._running = False
        self._stop_event.set()

    def is_running(self) -> bool:
        return self._running and not self._stop_event.is_set()

    def _record_audio(self, seconds: float) -> np.ndarray:
        frames = int(seconds * config.SAMPLE_RATE)
        audio = sd.rec(frames, samplerate=config.SAMPLE_RATE, channels=config.CHANNELS, dtype="int16")
        sd.wait()
        return audio

    def _save_temp_wav(self, audio: np.ndarray) -> Path:
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        write(temp.name, config.SAMPLE_RATE, audio)
        return Path(temp.name)

    def _apply_gain(self, audio: np.ndarray, gain: float) -> np.ndarray:
        """Amplify audio to improve quiet speech recognition while clipping safely."""
        boosted = audio.astype(np.float32) * gain
        clipped = np.clip(boosted, -32768, 32767)
        return clipped.astype(np.int16)

    def _audio_rms(self, audio: np.ndarray) -> float:
        normalized = audio.astype(np.float32) / 32768.0
        return float(np.sqrt(np.mean(np.square(normalized))))

    def _is_audio_loud_enough(self, audio: np.ndarray) -> bool:
        """Filter out extremely quiet segments before expensive STT calls."""
        return self._audio_rms(audio) >= config.MIN_AUDIO_RMS

    def _record_command_until_silence(self) -> np.ndarray:
        """Continuously record command audio until silence or max length."""
        chunks: list[np.ndarray] = []
        elapsed = 0.0
        silence = 0.0

        while elapsed < config.COMMAND_MAX_SECONDS and not self._stop_event.is_set():
            chunk = self._record_audio(config.COMMAND_CHUNK_SECONDS)
            chunks.append(chunk)
            elapsed += config.COMMAND_CHUNK_SECONDS

            rms = self._audio_rms(chunk)
            if self.on_level:
                self.on_level(rms)

            if rms >= config.MIN_AUDIO_RMS:
                silence = 0.0
            else:
                silence += config.COMMAND_CHUNK_SECONDS

            if elapsed >= config.COMMAND_MIN_SECONDS and silence >= config.COMMAND_SILENCE_SECONDS:
                break

        if not chunks:
            return np.zeros((1, config.CHANNELS), dtype=np.int16)

        return np.concatenate(chunks, axis=0)

    def _listen_loop(self) -> None:
        self.on_status("Listening for wake word: Luvi / Луви")
        while not self._stop_event.is_set():
            wake_path: Path | None = None
            cmd_path: Path | None = None
            try:
                wake_audio = self._record_audio(config.WAKE_LISTEN_SECONDS)
                wake_rms = self._audio_rms(wake_audio)
                if self.on_level:
                    self.on_level(wake_rms)

                if not self._is_audio_loud_enough(wake_audio):
                    continue

                wake_audio = self._apply_gain(wake_audio, config.WAKE_AUDIO_GAIN)
                wake_path = self._save_temp_wav(wake_audio)
                if not self.wake_detector.detect_from_audio(wake_path):
                    continue

                self.on_status("Wake word detected. Listening for command...")
                cmd_audio = self._record_command_until_silence()
                if not self._is_audio_loud_enough(cmd_audio):
                    self.on_status("Command too quiet. Please speak a little louder.")
                    continue

                cmd_audio = self._apply_gain(cmd_audio, config.COMMAND_AUDIO_GAIN)
                cmd_path = self._save_temp_wav(cmd_audio)
                command_text = self.stt.transcribe_file(cmd_path)
                command_text = self.wake_detector.remove_wake_word(command_text)

                if command_text:
                    self.on_command(command_text)
            except Exception as exc:  # noqa: BLE001 - runtime device/model failures
                self.on_status(f"Voice listener error: {exc}")
            finally:
                if wake_path and wake_path.exists():
                    wake_path.unlink(missing_ok=True)
                if cmd_path and cmd_path.exists():
                    cmd_path.unlink(missing_ok=True)

            self.on_status("Listening for wake word: Luvi / Луви")

        self._running = False
