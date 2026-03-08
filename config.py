"""Configuration values for the Luvi assistant."""

from pathlib import Path

# Wake-word and audio settings
WAKE_WORD = "luvi"
SAMPLE_RATE = 16_000
CHANNELS = 1
WAKE_LISTEN_SECONDS = 2.5
COMMAND_RECORD_SECONDS = 7

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
