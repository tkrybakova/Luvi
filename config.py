"""Configuration values for the Luvi assistant."""

from pathlib import Path

# Wake-word and audio settings
WAKE_WORD = "luvi"
WAKE_WORD_ALIASES = ("luvi", "луви")
SAMPLE_RATE = 16_000
CHANNELS = 1
WAKE_LISTEN_SECONDS = 2.5
COMMAND_RECORD_SECONDS = 7
MIN_AUDIO_RMS = 0.005  # Lower threshold: easier activation for quieter speech

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

# Dark theme colors
UI_BG = "#0f172a"
UI_PANEL = "#111827"
UI_SURFACE = "#1f2937"
UI_ACCENT = "#7c3aed"
UI_TEXT = "#e5e7eb"
UI_TEXT_MUTED = "#94a3b8"
