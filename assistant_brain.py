"""Core orchestration for Luvi's reasoning and action flow."""

from __future__ import annotations

import requests

import config
from command_router import CommandRouter
from screen_reader import ScreenReader
from web_search import WebSearch


class AssistantBrain:
    """Routes commands and coordinates system actions + LLM reasoning."""

    def __init__(self) -> None:
        self.router = CommandRouter()
        self.screen_reader = ScreenReader()
        self.web_search = WebSearch()

    def generate_llm_response(self, prompt: str) -> str:
        """Generate a non-streaming response from local Ollama."""
        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(config.OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "No response from LLM.").strip()

    def generate_vision_response(self, prompt: str, image_b64: str) -> str:
        """Generate response from multimodal model using screenshot image."""
        payload = {
            "model": config.OLLAMA_VISION_MODEL,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }
        response = requests.post(config.OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "No response from vision model.").strip()

    def handle(self, user_text: str) -> tuple[str, str]:
        """Handle a user prompt and return (intent, response)."""
        intent = self.router.route(user_text)

        if intent == "system":
            return intent, self.router.execute_system_command(user_text)

        if intent == "screen":
            ocr_text = self.screen_reader.read_screen_text()
            if ocr_text:
                prompt = (
                    "You are helping the user understand current screen contents. "
                    f"OCR text from screen:\n{ocr_text}\n\nUser request: {user_text}"
                )
                return intent, self._safe_llm(prompt)

            if config.OLLAMA_VISION_MODEL:
                image_b64 = self.screen_reader.capture_screen_base64()
                prompt = (
                    "Analyze the screenshot and answer the user's question in a concise helpful way. "
                    f"User request: {user_text}"
                )
                return intent, self._safe_vision(prompt, image_b64)

            return intent, (
                "I could not read text from the screen. "
                "Set OLLAMA_VISION_MODEL in config.py (for example `llava`) to enable image-based analysis."
            )

        if intent == "web_search":
            results = self.web_search.search(user_text)
            if not results:
                return intent, "I could not find web results right now."

            formatted = self.web_search.format_results(results)
            prompt = (
                "Summarize these web search findings for the user and provide a concise answer.\n\n"
                f"User query: {user_text}\n\nResults:\n{formatted}"
            )
            summary = self._safe_llm(prompt)
            combined = f"{summary}\n\nTop results:\n{formatted}"
            return intent, combined

        return intent, self._safe_llm(user_text)

    def _safe_llm(self, prompt: str) -> str:
        """Wrap LLM errors into readable user messages."""
        try:
            return self.generate_llm_response(prompt)
        except Exception as exc:  # noqa: BLE001 - report runtime API failure
            return (
                "I could not reach Ollama right now. "
                "Please install Ollama, run `ollama serve`, and verify model availability "
                f"with `ollama list`. Details: {exc}"
            )

    def _safe_vision(self, prompt: str, image_b64: str) -> str:
        """Wrap vision-model errors into readable user messages."""
        try:
            return self.generate_vision_response(prompt, image_b64)
        except Exception as exc:  # noqa: BLE001
            return (
                "Screen OCR found no text and vision analysis is unavailable. "
                "Install/pull a vision model (e.g. `ollama pull llava`) and set OLLAMA_VISION_MODEL. "
                f"Details: {exc}"
            )
