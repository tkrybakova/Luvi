"""Web-search utilities for Luvi."""

from __future__ import annotations

import config

try:
    from ddgs import DDGS
except Exception:  # noqa: BLE001
    # Backward compatibility for environments where old package is still installed.
    from duckduckgo_search import DDGS  # type: ignore[no-redef]


class WebSearch:
    """Performs web search and returns digestible results."""

    def search(self, query: str, limit: int = config.SEARCH_RESULTS_LIMIT) -> list[dict]:
        """Return DuckDuckGo text results, or an empty list on failure."""
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=limit))
        except Exception:
            return []

    def format_results(self, results: list[dict]) -> str:
        lines = []
        for idx, item in enumerate(results, start=1):
            lines.append(
                f"{idx}. {item.get('title', 'No title')}\n"
                f"   URL: {item.get('href', '')}\n"
                f"   Snippet: {item.get('body', '')}"
            )
        return "\n\n".join(lines)
