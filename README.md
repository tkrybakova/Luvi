# Luvi - Local AI Assistant

Luvi is a modular local desktop AI assistant for laptops. It continuously listens for the wake word **"Luvi"** (also supports **"Луви"**), captures voice commands, routes them by intent, and responds via both a GUI and spoken output.

## Features

- Wake-word workflow: `Luvi/Луви` → continuous command capture-until-silence → transcribe with **faster-whisper**.
- Local LLM reasoning through **Ollama**.
- Voice output with **Piper TTS**.
- Command routing:
  - system actions (open browser/app, search files)
  - AI Q&A
  - web search + LLM summarization
  - screen reading with OCR
- Tkinter desktop UI (purple themed, interactive):
  - modern purple header + cards
  - live voice level meter
  - start/stop listening microphone toggle
  - quick action buttons + conversation history
  - recognized command/intent display + text-input fallback
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
- `MIN_AUDIO_RMS` (microphone sensitivity; lower value = easier wake-word triggering)
- `WAKE_AUDIO_GAIN` and `COMMAND_AUDIO_GAIN` (boost quiet speech before STT)
- `COMMAND_CHUNK_SECONDS`, `COMMAND_MIN_SECONDS`, `COMMAND_MAX_SECONDS`, `COMMAND_SILENCE_SECONDS` (continuous command listening behavior)
- `INPUT_DEVICE_HINT`, `AUDIO_MAX_RETRIES`, `AUDIO_RETRY_SECONDS` (microphone recovery/fallback on Windows)

## Run

```bash
python main.py
```

## Quick troubleshooting

- Wake word triggers only when speaking loudly:
  - lower `MIN_AUDIO_RMS` in `config.py` (e.g., `0.0015` -> `0.0010`)
  - increase `WAKE_AUDIO_GAIN` / `COMMAND_AUDIO_GAIN` (e.g., `2.2` -> `3.0`)
  - verify microphone input level in OS settings

- `sounddevice.PortAudioError` / `WdmSyncIoctl` / `Error starting stream` on Windows:
  - close apps that can lock microphone (Zoom/Teams/Discord/browser tabs)
  - in Windows Settings -> Privacy & security -> Microphone, allow access for desktop apps
  - set `INPUT_DEVICE_HINT` in `config.py` (example: `"microphone"`) to pick a stable input device
  - listener now retries automatically (`AUDIO_MAX_RETRIES`) before failing

- First launch hangs/crashes around `huggingface_hub` / `WhisperModel`:
  - this is usually first-time model download or a broken virtualenv package cache
  - wait for download to complete once; if interrupted, recreate venv and reinstall deps
  - recommended reset (Windows): remove `.venv`, then `python -m venv .venv` and `pip install -r requirements.txt`

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
