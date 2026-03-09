"""Configuration values for the Luvi assistant."""

from pathlib import Path

# Wake-word and audio settings
WAKE_WORD = "luvi"
WAKE_WORD_ALIASES = ("luvi", "луви")
SAMPLE_RATE = 48000
CHANNELS = 2
WAKE_LISTEN_SECONDS = 4
COMMAND_RECORD_SECONDS = 7
MIN_AUDIO_RMS = 0.0007
WAKE_AUDIO_GAIN = 2.2
COMMAND_AUDIO_GAIN = 2.8

# Models and local services
WHISPER_MODEL_SIZE = "base"
OLLAMA_MODEL = "llama3.1"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Text-to-speech (Piper)
PIPER_BINARY = r"D:\Luvi\piper\piper.exe"
PIPER_MODEL_PATH = r"D:\Luvi\piper\espeak-ng-data\voices\ru_RU-irina-medium.onnx"
PIPER_OUTPUT_DIR = Path(".luvi_audio")

# OCR and screenshot
TESSERACT_CMD = r"D:\Luvi\tesseract\tesseract.exe"

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