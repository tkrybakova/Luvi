"""Configuration values for the Luvi assistant."""

from pathlib import Path

# Wake-word and audio settings
WAKE_WORD = "luvi"
WAKE_WORD_ALIASES = ("luvi", "луви")
SAMPLE_RATE = 16_000
CHANNELS = 1
WAKE_LISTEN_SECONDS = 2.5
COMMAND_RECORD_SECONDS = 7
COMMAND_CHUNK_SECONDS = 0.5
COMMAND_MIN_SECONDS = 1.5
COMMAND_MAX_SECONDS = 12.0
COMMAND_SILENCE_SECONDS = 1.2
MIN_AUDIO_RMS = 0.0015  # Lower threshold: catches quieter voice segments better
WAKE_AUDIO_GAIN = 2.2
COMMAND_AUDIO_GAIN = 2.8
INPUT_DEVICE_HINT = ""  # Optional substring of microphone name, e.g. "microphone"
AUDIO_MAX_RETRIES = 3
AUDIO_RETRY_SECONDS = 1.0
AUDIO_SAMPLE_RATE_FALLBACKS = (16000, 44100, 48000)

# Models and local services
WHISPER_MODEL_SIZE = "base"
OLLAMA_MODEL = "llama3.1"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Text-to-speech (Piper)
PIPER_BINARY = "piper"
PIPER_MODEL_PATH = "en_US-lessac-medium.onnx"
PIPER_OUTPUT_DIR = Path(".luvi_audio")

# OCR and screenshot
TESSERACT_CMD = "tesseract"

# Web search
SEARCH_RESULTS_LIMIT = 5

# UI
WINDOW_TITLE = "Luvi - Local AI Assistant"

# Purple theme colors
UI_BG = "#130a2a"
UI_PANEL = "#1d1140"
UI_SURFACE = "#2a1759"
UI_ACCENT = "#9f5cff"
UI_ACCENT_ALT = "#7c3aed"
UI_TEXT = "#f3e8ff"
UI_TEXT_MUTED = "#c4b5fd"
