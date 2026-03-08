# Luvi - Local AI Assistant

Luvi is a modular local desktop AI assistant for laptops. It continuously listens for the wake word **"Luvi"** (also supports **"Луви"**), captures voice commands, routes them by intent, and responds via both a GUI and spoken output.

## Features

- Wake-word workflow: `Luvi/Луви` → record command → transcribe with **faster-whisper**.
- Local LLM reasoning through **Ollama**.
- Voice output with **Piper TTS**.
- Command routing:
  - system actions (open browser/app, search files)
  - AI Q&A
  - web search + LLM summarization
  - screen reading with OCR
- Tkinter desktop UI (dark themed):
  - modern header + command cards
  - conversation history
  - recognized command/intent display
  - text-input fallback
- Runtime safeguards:
  - temporary audio files are cleaned automatically
  - graceful user-facing errors when Ollama/TTS/search fail

## Project structure

- `main.py` - App entrypoint, UI + voice listener bootstrap.
- `voice_listener.py` - Continuous mic listening loop.
- `wake_word.py` - Wake-word detection.
- `speech_to_text.py` - faster-whisper transcription.
- `assistant_brain.py` - Core orchestration + Ollama calls.
- `command_router.py` - Intent detection + local command execution.
- `screen_reader.py` - Screen capture + OCR.
- `web_search.py` - Web search and result formatting.
- `text_to_speech.py` - Piper synthesis + playback.
- `ui_window.py` - Tkinter desktop interface.
- `config.py` - Central configuration.

## Local setup

1. Install Python 3.10+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Install Ollama

> If PowerShell says `ollama : The term 'ollama' is not recognized`, Ollama is not installed or not on PATH.

- **Windows**
  1. Download installer: https://ollama.com/download/windows
  2. Install and reopen PowerShell.
  3. Verify:
     ```powershell
     ollama --version
     ```
  4. Pull model and start server:
     ```powershell
     ollama pull llama3.1
     ollama serve
     ```

- **macOS / Linux**
  ```bash
  ollama pull llama3.1
  ollama serve
  ```

### Install TTS + OCR prerequisites

- Piper: install Piper binary and download a voice model such as `en_US-lessac-medium.onnx`.
- Tesseract OCR:
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - macOS (Homebrew): `brew install tesseract`
  - Windows: install Tesseract OCR and set `TESSERACT_CMD` in `config.py` if needed.

### Configure `config.py`

Set these values for your machine:
- `OLLAMA_MODEL`
- `PIPER_MODEL_PATH`
- `TESSERACT_CMD`

## Run

```bash
python main.py
```

## Quick troubleshooting

- `ollama` command not found on Windows:
  - reinstall Ollama from the official installer
  - close/reopen terminal (to refresh PATH)
  - run `ollama --version`
- Ollama installed but app says it cannot reach Ollama:
  - ensure `ollama serve` is running
  - run `ollama list` to verify model exists
  - confirm `config.py` points to `http://localhost:11434/api/generate`

## Example voice workflow

User: "Luvi, search information about black holes."

Flow:
1. Wake-word detector catches "Luvi".
2. Command audio is recorded and transcribed.
3. Router selects `web_search` intent.
4. Search results are fetched and summarized with Ollama.
5. Answer is shown in the UI and spoken aloud with Piper.

## Notes

- This project is intentionally modular for easy extension.
- You can swap intent detection heuristics with an LLM classifier later.
- For best wake-word experience, use a clean microphone setup.
