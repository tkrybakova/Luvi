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

    def handle(self, user_text: str) -> tuple[str, str]:
        """Handle a user prompt and return (intent, response)."""
        intent = self.router.route(user_text)

        if intent == "system":
            return intent, self.router.execute_system_command(user_text)

        if intent == "screen":
            text = self.screen_reader.read_screen_text()
            if not text:
                return intent, "I could not read any text from the screen."
            prompt = (
                "You are helping the user understand current screen contents. "
                f"Screen text:\n{text}\n\nUser request: {user_text}"
            )
            return intent, self._safe_llm(prompt)

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
            return f"I could not reach Ollama right now: {exc}"
