"""Intent routing and local command execution."""

from __future__ import annotations

import platform
import re
import subprocess
import webbrowser
from pathlib import Path


class CommandRouter:
    """Routes user requests into system, web, screen, or AI intents."""

    SYSTEM_KEYWORDS = ("open browser", "open app", "launch", "search file")
    SCREEN_KEYWORDS = ("what is on my screen", "summarize this page", "on my screen")
    WEB_SEARCH_KEYWORDS = ("search", "look up", "find on web", "google")

    _SEARCH_FILE_RE = re.compile(r"\bsearch\s+file\b", re.IGNORECASE)
    _OPEN_APP_RE = re.compile(r"\bopen\s+app\b", re.IGNORECASE)
    _LAUNCH_RE = re.compile(r"^\s*launch\b", re.IGNORECASE)

    def route(self, text: str) -> str:
        """Return the best matching intent for an input sentence."""
        low = text.lower().strip()

        # Keep more specific intents before generic web-search matching.
        if any(k in low for k in self.SCREEN_KEYWORDS):
            return "screen"
        if any(k in low for k in self.SYSTEM_KEYWORDS):
            return "system"
        if any(k in low for k in self.WEB_SEARCH_KEYWORDS):
            return "web_search"
        return "ai_answer"

    def execute_system_command(self, text: str) -> str:
        """Execute supported local system actions."""
        low = text.lower().strip()

        if "open browser" in low:
            webbrowser.open("https://duckduckgo.com")
            return "Opened the browser."

        if "open app" in low or low.startswith("launch"):
            app_name = self._extract_app_name(text)
            if not app_name:
                return "Please say the app name after 'open app' or 'launch'."
            return self._open_app(app_name)

        if "search file" in low:
            query = self._extract_search_query(text)
            return self._search_file(query)

        return "I could not map that to a local system action."

    def _extract_app_name(self, text: str) -> str:
        open_app_match = self._OPEN_APP_RE.search(text)
        if open_app_match:
            return text[open_app_match.end() :].strip()

        launch_match = self._LAUNCH_RE.search(text)
        if launch_match:
            return text[launch_match.end() :].strip()

        return ""

    def _extract_search_query(self, text: str) -> str:
        match = self._SEARCH_FILE_RE.search(text)
        if not match:
            return ""
        return text[match.end() :].strip()

    def _open_app(self, app_name: str) -> str:
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            elif system == "Windows":
                subprocess.Popen(["start", "", app_name], shell=True)
            else:
                subprocess.Popen([app_name])
            return f"Attempted to open app: {app_name}."
        except Exception as exc:  # noqa: BLE001 - user facing runtime message
            return f"Failed to open {app_name}: {exc}"

    def _search_file(self, query: str) -> str:
        if not query:
            return "Please provide a filename pattern after 'search file'."

        home = Path.home()
        matches = list(home.rglob(f"*{query}*"))[:10]

        if not matches:
            return f"No files found matching '{query}'."

        lines = [f"Found {len(matches)} files:"]
        lines.extend(str(path) for path in matches)
        return "\n".join(lines)
